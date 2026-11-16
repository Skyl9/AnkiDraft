"""Tour Guide & Onboarding interactif pour AnkiForge.

Fournit à la fois les bulles d'aide contextuelles par vue (``TourBubble``)
et le moteur compagnon non bloquant piloté par événements (``InteractiveTourController``
et ``TourCompanionCard``).
"""

from __future__ import annotations

import contextlib
import json
import logging
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any, Literal

from PySide6.QtCore import QEvent, QObject, QPoint, Qt, Signal
from PySide6.QtGui import QFont, QScreen
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from ankidraft.ui.components.buttons import ActionButton, PrimaryButton, SecondaryButton, apply_compact_style
from ankidraft.ui.theme import DesignTokens, apply_shadow
from ankidraft.utils.event_bus import (
    AppEvent,
    AppEventBus,
    BatchTaskReviewedEvent,
    CardPreviewToggledEvent,
    MCPDataMutatedEvent,
    MCPPatchRejectedEvent,
    PackageExportedEvent,
    ViewNavigatedEvent,
    WozniakAuditResolvedEvent,
    event_bus,
)
from ankidraft.utils.i18n import tr
from ankidraft.utils.icon_loader import load_on_accent_icon, load_phosphor_icon

logger = logging.getLogger(__name__)


@dataclass
class TourStep:
    """Étape individuelle de la bulle d'aide contextuelle par vue."""

    title: str
    text: str
    target_widget: QWidget | None = None
    target_widget_getter: Callable[[], QWidget | None] | None = None
    action: Callable[[], None] | None = None


@dataclass
class InteractiveTourStep:
    """Étape déclarative d'un parcours interactif piloté par événements."""

    step_id: str
    title_factory: Callable[[], str]
    text_factory: Callable[[], str]
    target_view_id: str | None = None
    on_enter: Callable[[], None] | None = None
    completion_event: type[AppEvent] | tuple[type[AppEvent], ...] | None = None
    completion_predicate: Callable[[AppEvent], bool] | None = None


class TourBubble(QWidget):
    """Bulle d'information flottante utilisée pour l'aide contextuelle des vues."""

    tour_finished = Signal()

    def __init__(self, main_window: QWidget, *, preserve_completion_flag: bool = False) -> None:
        super().__init__(main_window)
        self.main_window = main_window
        self.preserve_completion_flag = preserve_completion_flag

        self.setWindowFlags(Qt.WindowType.ToolTip | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMinimumWidth(380)
        self.setMaximumWidth(460)

        self.current_step: int = 0
        self.steps: list[TourStep] = []

        self._setup_ui()
        self.hide()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)

        self.bg_frame = QWidget()
        self.bg_frame.setObjectName("TourBubbleBg")
        self.bg_frame.setStyleSheet(f"""
            QWidget#TourBubbleBg {{
                background-color: {DesignTokens.BG_PANEL};
                border: 2px solid {DesignTokens.ACCENT_PRIMARY};
                border-radius: {DesignTokens.RADIUS_LG}px;
            }}
        """)
        apply_shadow(self.bg_frame, blur=24, offset_y=6, color=DesignTokens.ACCENT_GLOW)

        bg_layout = QVBoxLayout(self.bg_frame)
        bg_layout.setContentsMargins(20, 20, 20, 18)
        bg_layout.setSpacing(12)

        self.lbl_title = QLabel(self.tr("Titre"))
        self.lbl_title.setStyleSheet(f"""
            font-size: 16px;
            font-weight: bold;
            color: {DesignTokens.ACCENT_PRIMARY};
            border: none;
            background: transparent;
        """)
        bg_layout.addWidget(self.lbl_title)

        self.lbl_text = QLabel(self.tr("Description..."))
        self.lbl_text.setStyleSheet(f"""
            font-size: 13px;
            line-height: 1.4;
            color: {DesignTokens.TEXT_PRIMARY};
            border: none;
            background: transparent;
        """)
        self.lbl_text.setWordWrap(True)
        bg_layout.addWidget(self.lbl_text)
        bg_layout.addSpacing(6)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        self.btn_skip = ActionButton("x", "", parent=self)
        self.btn_skip.setText(self.tr("Quitter"))
        self.btn_skip.clicked.connect(self.end_tour)
        btn_layout.addWidget(self.btn_skip)

        btn_layout.addStretch()

        self.btn_prev = ActionButton("arrow-left", "", parent=self)
        self.btn_prev.setText(self.tr("Précédent"))
        self.btn_prev.clicked.connect(self.prev_step)
        btn_layout.addWidget(self.btn_prev)

        self.lbl_counter = QLabel(self.tr("1/x"))
        self.lbl_counter.setStyleSheet(f"""
            color: {DesignTokens.TEXT_MUTED};
            font-weight: 600;
            font-size: 12px;
            font-family: '{DesignTokens.FONT_CODE}';
            padding: 0 8px;
            border: none;
            background: transparent;
        """)
        self.lbl_counter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn_layout.addWidget(self.lbl_counter)

        self.btn_next = PrimaryButton(self.tr("Suivant"), parent=self)
        self.btn_next.setIcon(load_on_accent_icon("arrow-right"))
        self.btn_next.clicked.connect(self.next_step)
        btn_layout.addWidget(self.btn_next)

        bg_layout.addLayout(btn_layout)
        layout.addWidget(self.bg_frame)

    def set_scenario(self, steps: list[TourStep | dict[str, Any]]) -> None:
        """Définit la liste des étapes du tour (supporte objets TourStep ou dicts)."""
        normalized_steps: list[TourStep] = []
        for step in steps:
            if isinstance(step, TourStep):
                normalized_steps.append(step)
            elif isinstance(step, dict):
                normalized_steps.append(
                    TourStep(
                        title=step.get("title", ""),
                        text=step.get("text", ""),
                        target_widget=step.get("target_widget"),
                        target_widget_getter=step.get("target_widget_getter"),
                        action=step.get("action"),
                    )
                )
        self.steps = normalized_steps
        self.current_step = 0

    def start_tour(self) -> None:
        """Démarre le déroulement de la visite guidée."""
        if not self.steps:
            return
        self.current_step = 0
        self.show()
        self.raise_()
        self.play_step()

    def play_step(self) -> None:
        """Exécute et affiche l'étape active."""
        if self.current_step >= len(self.steps):
            self.end_tour()
            return

        step = self.steps[self.current_step]

        if step.action and callable(step.action):
            try:
                step.action()
            except Exception as e:
                logger.warning("Erreur durant l'action de l'étape de tour: %s", e)

        self.lbl_title.setText(step.title)
        self.lbl_text.setText(step.text)
        self.lbl_counter.setText(tr("%1/%2", self.current_step + 1, len(self.steps)))

        self.btn_prev.setVisible(self.current_step > 0)

        if self.current_step == len(self.steps) - 1:
            self.btn_next.setText(self.tr("Terminer"))
            self.btn_next.setIcon(load_on_accent_icon("check"))
        else:
            self.btn_next.setText(self.tr("Suivant"))
            self.btn_next.setIcon(load_on_accent_icon("arrow-right"))

        QApplication.processEvents()

        target = step.target_widget
        if step.target_widget_getter and callable(step.target_widget_getter):
            try:
                target = step.target_widget_getter()
            except Exception:
                target = None

        self._position_bubble(target)

    def _position_bubble(self, target_widget: QWidget | None) -> None:
        """Calcule le positionnement optimal de la bulle à côté du widget cible."""
        self.adjustSize()

        screen: QScreen | None = self.screen()
        screen_rect = screen.availableGeometry() if screen else self.main_window.geometry()

        if target_widget is None or not target_widget.isVisible():
            parent_geom = self.main_window.geometry()
            x = parent_geom.x() + (parent_geom.width() - self.width()) // 2
            y = parent_geom.y() + (parent_geom.height() - self.height()) // 2
            self.move(x, y)
            return

        target_pos = target_widget.mapToGlobal(QPoint(0, 0))

        if target_pos.x() + target_widget.width() + 16 + self.width() <= screen_rect.right():
            x = target_pos.x() + target_widget.width() + 16
            y = target_pos.y()
        elif target_pos.x() - self.width() - 16 >= screen_rect.left():
            x = target_pos.x() - self.width() - 16
            y = target_pos.y()
        else:
            x = max(screen_rect.left() + 10, target_pos.x())
            y = target_pos.y() + target_widget.height() + 16

        if y + self.height() > screen_rect.bottom() - 16:
            y = screen_rect.bottom() - self.height() - 16
        if y < screen_rect.top() + 16:
            y = screen_rect.top() + 16

        if x + self.width() > screen_rect.right() - 16:
            x = screen_rect.right() - self.width() - 16
        if x < screen_rect.left() + 16:
            x = screen_rect.left() + 16

        self.move(x, y)

    def prev_step(self) -> None:
        """Revient à l'étape précédente."""
        if self.current_step > 0:
            self.current_step -= 1
            self.play_step()

    def next_step(self) -> None:
        """Avance à l'étape suivante ou termine."""
        self.current_step += 1
        self.play_step()

    def end_tour(self) -> None:
        """Termine et enregistre la fin de la visite guidée."""
        self.hide()
        if not self.preserve_completion_flag:
            from ankidraft.utils.environment import get_app_qsettings

            settings = get_app_qsettings()
            settings.setValue("app/tour_completed", True)
            if hasattr(self.main_window, "settings") and hasattr(self.main_window.settings, "setValue"):
                try:
                    self.main_window.settings.setValue("app/tour_completed", True)
                except (RuntimeError, AttributeError, OSError) as e:
                    logger.debug("Échec enregistrement tour_completed : %s", e)
        self.tour_finished.emit()


class TourCompanionCard(QFrame):
    """Carte compagnon non bloquante ancrée en bas à droite de la fenêtre hôte."""

    prev_requested = Signal()
    skip_requested = Signal()
    next_requested = Signal()
    quit_requested = Signal()

    ANCHOR_MARGIN = 20

    def __init__(self, host_window: QWidget) -> None:
        super().__init__(host_window)
        self._host_window = host_window
        self._is_completed = False
        self._waiting_for_event = False
        self.setObjectName("TourCompanionCard")
        self.setMinimumWidth(420)
        self.setMaximumWidth(460)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self._build_ui()
        self.refresh_theme()
        self.hide()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 14, 16, 14)
        root.setSpacing(10)

        header = QHBoxLayout()
        header.setSpacing(8)

        self.lbl_icon = QLabel(self)
        self.lbl_icon.setFixedSize(20, 20)
        header.addWidget(self.lbl_icon)

        self.lbl_title = QLabel(self)
        self.lbl_title.setWordWrap(True)
        header.addWidget(self.lbl_title, 1)

        self.lbl_counter = QLabel(self)
        self.lbl_counter.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        header.addWidget(self.lbl_counter)
        root.addLayout(header)

        self.status_badge = QFrame(self)
        self.status_badge.setObjectName("TourStatusBadge")
        badge_layout = QHBoxLayout(self.status_badge)
        badge_layout.setContentsMargins(10, 5, 10, 5)
        badge_layout.setSpacing(6)
        self.lbl_status_icon = QLabel(self.status_badge)
        self.lbl_status_icon.setFixedSize(14, 14)
        badge_layout.addWidget(self.lbl_status_icon)
        self.lbl_status = QLabel(self.status_badge)
        self.lbl_status.setWordWrap(True)
        badge_layout.addWidget(self.lbl_status, 1)
        root.addWidget(self.status_badge)

        self.lbl_text = QLabel(self)
        self.lbl_text.setWordWrap(True)
        root.addWidget(self.lbl_text)

        controls = QHBoxLayout()
        controls.setSpacing(6)

        self.btn_quit = ActionButton("x", "", parent=self)
        self.btn_quit.setText(self.tr("Quitter"))
        apply_compact_style(self.btn_quit)
        self.btn_quit.clicked.connect(self.quit_requested.emit)
        controls.addWidget(self.btn_quit)

        controls.addStretch()

        self.btn_prev = ActionButton("arrow-left", "", parent=self)
        self.btn_prev.setText(self.tr("Précédent"))
        apply_compact_style(self.btn_prev)
        self.btn_prev.clicked.connect(self.prev_requested.emit)
        controls.addWidget(self.btn_prev)

        self.btn_skip = ActionButton("skip-forward", "", parent=self)
        self.btn_skip.setText(self.tr("Passer l'étape"))
        apply_compact_style(self.btn_skip)
        self.btn_skip.clicked.connect(self.skip_requested.emit)
        controls.addWidget(self.btn_skip)

        self.btn_next = PrimaryButton(self.tr("Suivant"), parent=self)
        apply_compact_style(self.btn_next)
        self.btn_next.setIcon(load_on_accent_icon("arrow-right"))
        self.btn_next.clicked.connect(self.next_requested.emit)
        controls.addWidget(self.btn_next)

        root.addLayout(controls)

    def refresh_theme(self, profile: Any = None) -> None:
        """Applique les jetons sémantiques du thème actif à la carte compagnon."""
        self._last_profile = profile
        bg_panel = (profile.bg_panel if profile else "") or DesignTokens.BG_PANEL
        accent = (profile.accent_primary if profile else "") or DesignTokens.ACCENT_PRIMARY
        text_primary = (profile.text_primary if profile else "") or DesignTokens.TEXT_PRIMARY
        text_secondary = (profile.text_secondary if profile else "") or DesignTokens.TEXT_SECONDARY
        text_muted = (profile.text_muted if profile else "") or DesignTokens.TEXT_MUTED
        accent_glow = (profile.accent_glow if profile else "") or DesignTokens.ACCENT_GLOW

        self.setStyleSheet(f"""
            QFrame#TourCompanionCard {{
                background-color: {bg_panel};
                border: 2px solid {accent};
                border-radius: {DesignTokens.RADIUS_LG}px;
            }}
        """)
        apply_shadow(self, blur=20, offset_y=4, color=accent_glow)
        self.lbl_title.setStyleSheet(f"color: {text_primary}; font-size: 14px; font-weight: 700; background: transparent; border: none;")
        self.lbl_text.setStyleSheet(f"color: {text_secondary}; font-size: 12px; line-height: 1.4; background: transparent; border: none;")
        self.lbl_counter.setStyleSheet(f"color: {text_muted}; font-size: 11px; font-weight: 600; font-family: '{DesignTokens.FONT_CODE}'; background: transparent; border: none;")
        self.lbl_icon.setPixmap(load_phosphor_icon("compass", color=accent).pixmap(18, 18))
        self.btn_quit.refresh_theme(profile)
        self.btn_prev.refresh_theme(profile)
        self.btn_skip.refresh_theme(profile)
        self.btn_next.refresh_theme(profile)
        self._apply_status_style(profile)

    def _apply_status_style(self, profile: Any = None) -> None:
        active_profile = profile if profile is not None else getattr(self, "_last_profile", None)
        if self._is_completed:
            bg = (active_profile.color_green_bg if active_profile else "") or DesignTokens.COLOR_GREEN_BG
            border = (active_profile.color_green_border if active_profile else "") or DesignTokens.COLOR_GREEN_BORDER
            fg = (active_profile.color_green_text if active_profile else "") or DesignTokens.COLOR_GREEN_TEXT
            icon_name = "check-circle"
        else:
            bg = (active_profile.accent_bg if active_profile else "") or DesignTokens.ACCENT_BG
            border = (active_profile.accent_border if active_profile else "") or DesignTokens.ACCENT_BORDER
            fg = (active_profile.color_purple_text if active_profile else "") or DesignTokens.COLOR_PURPLE_TEXT
            icon_name = "sparkle"

        self.status_badge.setStyleSheet(f"""
            QFrame#TourStatusBadge {{
                background-color: {bg};
                border: 1px solid {border};
                border-radius: {DesignTokens.RADIUS_SM}px;
            }}
        """)
        self.lbl_status.setStyleSheet(f"color: {fg}; font-size: 11px; font-weight: 600; background: transparent; border: none;")
        self.lbl_status_icon.setPixmap(load_phosphor_icon(icon_name, color=fg).pixmap(14, 14))

    def update_step(
        self,
        title: str,
        text: str,
        index: int,
        total: int,
        *,
        completed: bool,
        waiting_for_event: bool,
    ) -> None:
        """Met à jour le contenu affiché et ré-ancre la carte sur la fenêtre hôte."""
        self._is_completed = completed
        self._waiting_for_event = waiting_for_event

        self.lbl_title.setText(title)
        self.lbl_text.setText(text)
        self.lbl_counter.setText(tr("%1/%2", index + 1, total))

        if completed:
            self.lbl_status.setText(self.tr("Action détectée — étape validée"))
        elif waiting_for_event:
            self.lbl_status.setText(self.tr("En attente de votre action dans l'atelier"))
        else:
            self.lbl_status.setText(self.tr("Lecture libre — cliquez sur Suivant lorsque vous êtes prêt"))

        self.status_badge.setVisible(waiting_for_event or completed)
        self._apply_status_style()

        is_last = index >= total - 1
        self.btn_prev.setVisible(index > 0)
        self.btn_skip.setVisible(not is_last)

        if is_last:
            self.btn_next.setText(self.tr("Terminer"))
            self.btn_next.setIcon(load_on_accent_icon("check"))
        else:
            self.btn_next.setText(self.tr("Suivant"))
            self.btn_next.setIcon(load_on_accent_icon("arrow-right"))

        self.adjustSize()
        self.anchor_to_host()

    def anchor_to_host(self) -> None:
        """Positionne la carte dans le coin inférieur droit de la fenêtre hôte."""
        if self._host_window is None:
            return
        self.adjustSize()
        margin = self.ANCHOR_MARGIN
        host_w = self._host_window.width()
        host_h = self._host_window.height()
        x = max(margin, host_w - self.width() - margin)
        y = max(margin, host_h - self.height() - margin)
        self.move(x, y)
        self.raise_()


class InteractiveTourController(QObject):
    """Contrôleur réactif orchestrant les parcours interactifs via AppEventBus."""

    step_changed = Signal(int, int)
    step_completed = Signal(str)
    tour_finished = Signal(str)
    tour_cancelled = Signal(str)

    def __init__(
        self,
        main_window: QWidget,
        *,
        event_bus_instance: AppEventBus | None = None,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent or main_window)
        self._main_window = main_window
        self._event_bus = event_bus_instance or event_bus
        self._steps: list[InteractiveTourStep] = []
        self._track_id: str = "default"
        self._current_index: int = 0
        self._completed_steps: set[str] = set()
        self._active_subscriptions: list[tuple[type[AppEvent], Callable[[AppEvent], None]]] = []
        self._card: TourCompanionCard | None = None
        self._host_filter_installed = False

    @property
    def is_active(self) -> bool:
        """Retourne True si un parcours est actuellement affiché."""
        return bool(self._steps and self._card is not None and self._card.isVisible())

    @property
    def companion_card(self) -> TourCompanionCard | None:
        """Retourne l'instance de carte compagnon courante."""
        return self._card

    @property
    def current_index(self) -> int:
        """Index (base 0) de l'étape actuellement affichée."""
        return self._current_index

    @property
    def completed_steps(self) -> set[str]:
        """Ensemble des identifiants d'étapes validées durant ce parcours."""
        return set(self._completed_steps)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        """Ré-ancre la carte compagnon lorsque la fenêtre hôte est redimensionnée."""
        if watched is self._main_window and event.type() == QEvent.Type.Resize and self._card is not None and self._card.isVisible():
            self._card.anchor_to_host()
        return super().eventFilter(watched, event)

    def start(self, steps: Sequence[InteractiveTourStep], *, track_id: str = "default") -> None:
        """Démarre ou redémarre un parcours interactif nommé."""
        self._unsubscribe_current_event()
        self._steps = list(steps)
        self._track_id = track_id
        self._current_index = 0
        self._completed_steps = set()

        if not self._steps:
            if self._card is not None:
                self._card.hide()
            return

        self._ensure_card()
        if not self._host_filter_installed:
            self._main_window.installEventFilter(self)
            self._host_filter_installed = True

        self._activate_step(0)

    def _ensure_card(self) -> TourCompanionCard:
        if self._card is None:
            self._card = TourCompanionCard(self._main_window)
            self._card.prev_requested.connect(self.prev_step)
            self._card.skip_requested.connect(self.skip_step)
            self._card.next_requested.connect(self.next_step)
            self._card.quit_requested.connect(self.quit_tour)
        return self._card

    def _activate_step(self, index: int) -> None:
        self._unsubscribe_current_event()
        self._current_index = index
        step = self._steps[index]

        self._navigate_to_step_view(step)
        self._run_step_on_enter(step)
        self._subscribe_step_event(step)

        card = self._ensure_card()
        card.update_step(
            step.title_factory(),
            step.text_factory(),
            index,
            len(self._steps),
            completed=step.step_id in self._completed_steps,
            waiting_for_event=step.completion_event is not None,
        )
        card.show()
        self.step_changed.emit(index, len(self._steps))

    def _navigate_to_step_view(self, step: InteractiveTourStep) -> None:
        if not step.target_view_id or not hasattr(self._main_window, "_on_view_selected"):
            return
        if getattr(self._main_window, "_current_view_id", None) == step.target_view_id:
            return
        try:
            self._main_window._on_view_selected(step.target_view_id)
        except Exception as exc:
            logger.warning("Navigation impossible vers '%s' pendant le tutoriel : %s", step.target_view_id, exc)

    def _run_step_on_enter(self, step: InteractiveTourStep) -> None:
        if step.on_enter is None:
            return
        try:
            step.on_enter()
        except Exception as exc:
            logger.warning("Erreur on_enter pour l'étape '%s' : %s", step.step_id, exc)

    def _subscribe_step_event(self, step: InteractiveTourStep) -> None:
        if step.completion_event is None or step.step_id in self._completed_steps:
            return

        event_classes = step.completion_event if isinstance(step.completion_event, tuple) else (step.completion_event,)

        def _handler(ev: AppEvent) -> None:
            self._on_step_event(ev)

        for event_cls in event_classes:
            self._event_bus.subscribe(event_cls, _handler)
            self._active_subscriptions.append((event_cls, _handler))

    def _unsubscribe_current_event(self) -> None:
        if not self._active_subscriptions:
            return
        for event_cls, handler in self._active_subscriptions:
            self._event_bus.unsubscribe(event_cls, handler)
        self._active_subscriptions.clear()

    def _on_step_event(self, event: AppEvent) -> None:
        if not self._steps or not 0 <= self._current_index < len(self._steps):
            return
        step = self._steps[self._current_index]
        if step.completion_predicate is not None:
            try:
                if not step.completion_predicate(event):
                    return
            except Exception as exc:
                logger.warning("Erreur prédicat d'étape '%s' : %s", step.step_id, exc)
                return

        self._unsubscribe_current_event()
        self._completed_steps.add(step.step_id)
        self.step_completed.emit(step.step_id)

        if self._current_index + 1 < len(self._steps):
            self._activate_step(self._current_index + 1)
            return

        if self._card is not None:
            self._card.update_step(
                step.title_factory(),
                step.text_factory(),
                self._current_index,
                len(self._steps),
                completed=True,
                waiting_for_event=True,
            )
            self._card.show()

    def prev_step(self) -> None:
        """Revient à l'étape précédente du parcours."""
        if self._current_index > 0:
            self._activate_step(self._current_index - 1)

    def skip_step(self) -> None:
        """Passe l'étape active et avance vers la suivante (ou termine)."""
        self.next_step()

    def next_step(self) -> None:
        """Passe à l'étape suivante ou termine le parcours."""
        if self._current_index + 1 < len(self._steps):
            self._activate_step(self._current_index + 1)
        else:
            self.finish_tour()

    def finish_tour(self) -> None:
        """Finalise le parcours en cours et notifie les abonnés."""
        track_id = self._track_id
        self._stop_tour()
        self.tour_finished.emit(track_id)

    def quit_tour(self) -> None:
        """Interrompt prématurément le parcours sans marquer de réussite complète."""
        track_id = self._track_id
        self._stop_tour()
        self.tour_cancelled.emit(track_id)

    def _stop_tour(self) -> None:
        self._unsubscribe_current_event()
        if self._host_filter_installed and self._main_window is not None:
            with contextlib.suppress(RuntimeError):
                self._main_window.removeEventFilter(self)
            self._host_filter_installed = False
        if self._card is not None:
            self._card.hide()


def create_view_tour_steps(view_key: str, view_widget: QWidget) -> list[TourStep]:
    """Génère une mini-visite guidée thématique (3 à 4 étapes) pour une vue donnée."""
    tours: dict[str, list[TourStep]] = {
        "documents": [
            TourStep(
                title=tr("Bibliothèque de Sources"),
                text=tr("Importez vos PDF, documents Markdown, vidéos YouTube ou pages web pour alimenter la forge."),
                target_widget_getter=lambda: getattr(view_widget, "tree_sources", None),
            ),
            TourStep(
                title=tr("Délimitation & Portée"),
                text=tr("Sélectionnez précisément les chapitres, sections ou plages de pages à inclure sans modifier le document original."),
                target_widget_getter=lambda: getattr(view_widget, "btn_delimit", None),
            ),
            TourStep(
                title=tr("Indexation RAG & Couverture"),
                text=tr("Vérifiez quelles sections sont indexées et déjà couvertes par vos cartes Anki."),
                target_widget_getter=lambda: getattr(view_widget, "btn_index_rag", None),
            ),
        ],
        "creation": [
            TourStep(
                title=tr("Studio de Génération"),
                text=tr("Choisissez votre source documentaire, le paquet cible et le modèle de note Anki."),
                target_widget_getter=lambda: getattr(view_widget, "combo_source", None),
            ),
            TourStep(
                title=tr("Pipeline & Persona"),
                text=tr("Sélectionnez le pipeline DAG et le profil pédagogique adaptés à votre matière."),
                target_widget_getter=lambda: getattr(view_widget, "combo_pipeline", None),
            ),
            TourStep(
                title=tr("Lancement & Prévisualisation"),
                text=tr("Lancez la génération puis relisez chaque carte proposée avant de l'enregistrer dans votre collection."),
                target_widget_getter=lambda: getattr(view_widget, "btn_generate", None),
            ),
        ],
        "pipelines": [
            TourStep(
                title=tr("Sélection du Pipeline DAG"),
                text=tr("Créez ou sélectionnez un workflow multi-étapes (LLM, RAG, Map-Reduce, Validation humaine)."),
                target_widget_getter=lambda: getattr(view_widget, "combo_pipeline", None),
            ),
            TourStep(
                title=tr("Chaîne d'Étapes"),
                text=tr("Ordonnancez vos étapes et configurez les branchements conditionnels en cas de succès ou d'échec."),
                target_widget_getter=lambda: getattr(view_widget, "steps_container", None),
            ),
            TourStep(
                title=tr("Inspecteur d'Étape"),
                text=tr("Réglez le prompt, le mode de découpage Map-Reduce et la politique d'échec de l'étape sélectionnée."),
                target_widget_getter=lambda: getattr(view_widget, "inspector", None),
            ),
        ],
        "analysis": [
            TourStep(
                title=tr("Audit Wozniak (20 Règles)"),
                text=tr("Détectez automatiquement les cartes trop longues, ambiguës ou non atomiques."),
                target_widget=view_widget,
            ),
            TourStep(
                title=tr("Couverture Documentaire"),
                text=tr("Inspectez les paliers de résolution (exact, section, page, lexical) reliant chaque note à sa source."),
                target_widget=view_widget,
            ),
            TourStep(
                title=tr("Correction Assistée"),
                text=tr("Appliquez les suggestions d'amélioration ou ouvrez les cartes ciblées dans l'éditeur."),
                target_widget=view_widget,
            ),
        ],
        "consultant": [
            TourStep(
                title=tr("Cockpit MCP & Consultant"),
                text=tr("Supervisez le serveur MCP local et les agents externes connectés à votre collection."),
                target_widget=view_widget,
            ),
            TourStep(
                title=tr("Garde-Fou en Deux Temps"),
                text=tr("Toute mutation proposée par un agent passe par ce sas de validation humaine avant écriture en base."),
                target_widget=view_widget,
            ),
            TourStep(
                title=tr("Audit & Traçabilité"),
                text=tr("Consultez l'historique des appels d'outils et les journaux d'exécution en temps réel."),
                target_widget=view_widget,
            ),
        ],
        "card_models": [
            TourStep(
                title=tr("Types de Notes Anki"),
                text=tr("Gérez vos modèles de notes, champs personnalisés et gabarits Recto/Verso Jinja2."),
                target_widget=view_widget,
            ),
            TourStep(
                title=tr("Éditeur HTML / CSS"),
                text=tr("Personnalisez le rendu visuel de vos cartes avec aperçu instantané."),
                target_widget=view_widget,
            ),
            TourStep(
                title=tr("Directives Cloze & KaTeX"),
                text=tr("Testez vos textes à trous et formules mathématiques avant l'export .apkg."),
                target_widget=view_widget,
            ),
        ],
    }
    return tours.get(view_key, [])


def start_view_tour(view_key: str, view_widget: QWidget, parent_window: QWidget | None = None) -> TourBubble:
    """Lance une mini-visite guidée thématique sans écraser app/tour_completed."""
    host = parent_window or view_widget.window() or view_widget
    bubble = TourBubble(host, preserve_completion_flag=True)
    bubble.steps = create_view_tour_steps(view_key, view_widget)
    bubble.start_tour()
    return bubble


TourTrackStatus = Literal["todo", "in_progress", "done"]
TOUR_TRACK_CORE = "core"
TOUR_TRACK_BATCH = "batch"
TOUR_TRACK_AI_LAB = "ai_lab"
TOUR_TRACK_TEMPLATES = "templates"
TOUR_TRACK_IDS: tuple[str, ...] = (
    TOUR_TRACK_CORE,
    TOUR_TRACK_BATCH,
    TOUR_TRACK_AI_LAB,
    TOUR_TRACK_TEMPLATES,
)
_VALID_TRACK_STATUSES: frozenset[str] = frozenset({"todo", "in_progress", "done"})


def load_tour_progress() -> dict[str, TourTrackStatus]:
    """Charge l'état d'avancement des parcours depuis SettingModel (JSON)."""
    from ankidraft.database.models import SettingModel
    from ankidraft.database.seeds.demo_seed import SETTING_TOUR_PROGRESS

    try:
        raw = SettingModel.get_value(SETTING_TOUR_PROGRESS, "{}")
    except Exception as exc:
        logger.debug("Lecture de %s ignorée : %s", SETTING_TOUR_PROGRESS, exc)
        return {}

    parsed: Any = raw
    if isinstance(raw, str):
        try:
            parsed = json.loads(raw) if raw.strip() else {}
        except json.JSONDecodeError:
            return {}

    if not isinstance(parsed, dict):
        return {}

    result: dict[str, TourTrackStatus] = {}
    for key, val in parsed.items():
        if isinstance(key, str) and isinstance(val, str) and val in _VALID_TRACK_STATUSES:
            result[key] = val
    return result


def save_tour_track_status(track_id: str, status: TourTrackStatus) -> dict[str, TourTrackStatus]:
    """Enregistre le statut d'un parcours dans ``app/tour_progress_json``."""
    from ankidraft.database.models import SettingModel
    from ankidraft.database.seeds.demo_seed import SETTING_TOUR_PROGRESS

    progress = load_tour_progress()
    progress[track_id] = status
    try:
        SettingModel.set_value(
            SETTING_TOUR_PROGRESS,
            json.dumps(progress, ensure_ascii=False, sort_keys=True),
            category="app",
        )
    except Exception as exc:
        logger.debug("Impossible de persister %s : %s", SETTING_TOUR_PROGRESS, exc)
    return progress


def _build_core_track_steps() -> list[InteractiveTourStep]:
    return [
        InteractiveTourStep(
            step_id="core-sources",
            title_factory=lambda: tr("1. Sources et couverture documentaire"),
            text_factory=lambda: tr(
                "Votre mini-cours de sciences cognitives est déjà découpé et indexé localement. Ouvrez maintenant l'onglet « Analyse & Audit IA » pour inspecter la couverture des sections."
            ),
            target_view_id="documents",
            completion_event=ViewNavigatedEvent,
            completion_predicate=lambda ev: isinstance(ev, ViewNavigatedEvent) and ev.view_id == "analysis",
        ),
        InteractiveTourStep(
            step_id="core-wozniak",
            title_factory=lambda: tr("2. Hôpital Wozniak (20 règles)"),
            text_factory=lambda: tr("Deux cartes sangsues ont été détectées dans le paquet d'exemple. Appliquez une suggestion ou ignorez une règle sur une carte pour valider cette étape."),
            target_view_id="analysis",
            completion_event=WozniakAuditResolvedEvent,
        ),
        InteractiveTourStep(
            step_id="core-mcp",
            title_factory=lambda: tr("3. Garde-Fou MCP en deux temps"),
            text_factory=lambda: tr("Une modification proposée par un agent attend votre accord dans « Serveur MCP & Agents ». Approuvez ou rejetez ce patch pour valider la gouvernance humaine."),
            target_view_id="consultant",
            completion_event=(MCPDataMutatedEvent, MCPPatchRejectedEvent),
        ),
        InteractiveTourStep(
            step_id="core-edition",
            title_factory=lambda: tr("4. Édition KaTeX, Cloze et aperçu"),
            text_factory=lambda: tr("Inspectez les cartes Basique, Cloze et KaTeX dans l'éditeur. Basculez la visibilité du volet d'aperçu en direct pour passer à l'étape finale."),
            target_view_id="edition",
            completion_event=CardPreviewToggledEvent,
        ),
        InteractiveTourStep(
            step_id="core-export",
            title_factory=lambda: tr("5. Export vers Anki (.apkg)"),
            text_factory=lambda: tr(
                "Vous pouvez exporter vos cartes vers un paquet .apkg à IDs stables sans altérer la planification FSRS, ou cliquer sur Terminer pour accéder aux modules complémentaires."
            ),
            target_view_id="edition",
            completion_event=PackageExportedEvent,
        ),
    ]


def _build_batch_track_steps() -> list[InteractiveTourStep]:
    return [
        InteractiveTourStep(
            step_id="batch-open",
            title_factory=lambda: tr("1. Ouvrir Batch Factory"),
            text_factory=lambda: tr("Une tâche pré-calculée sur la Section 3 vous attend dans Batch Factory sans nécessiter de clé API. Cliquez sur « Batch Factory » dans la navigation."),
            target_view_id="dashboard",
            completion_event=ViewNavigatedEvent,
            completion_predicate=lambda ev: isinstance(ev, ViewNavigatedEvent) and ev.view_id == "batch",
        ),
        InteractiveTourStep(
            step_id="batch-review",
            title_factory=lambda: tr("2. Réviser le lot en staging"),
            text_factory=lambda: tr("Examinez les cartes générées depuis la Section 3 puis validez ou rejetez la tâche dans le panneau de revue."),
            target_view_id="batch",
            completion_event=BatchTaskReviewedEvent,
        ),
    ]


def _build_ai_lab_track_steps() -> list[InteractiveTourStep]:
    return [
        InteractiveTourStep(
            step_id="ai-lab-agents",
            title_factory=lambda: tr("1. Éditeur d'Agents et Personas"),
            text_factory=lambda: tr("Découvrez comment spécialiser les personas pédagogiques sans modifier le pipeline global, puis ouvrez « Pipelines » dans le Laboratoire IA."),
            target_view_id="agents",
            completion_event=ViewNavigatedEvent,
            completion_predicate=lambda ev: isinstance(ev, ViewNavigatedEvent) and ev.view_id == "pipelines",
        ),
        InteractiveTourStep(
            step_id="ai-lab-pipelines",
            title_factory=lambda: tr("2. Orchestrateur de Pipelines DAG"),
            text_factory=lambda: tr("Enchaînez prompts LLM, récupération RAG, Map-Reduce et validation humaine. Ouvrez ensuite « Tests A/B » pour comparer plusieurs modèles ou prompts."),
            target_view_id="pipelines",
            completion_event=ViewNavigatedEvent,
            completion_predicate=lambda ev: isinstance(ev, ViewNavigatedEvent) and ev.view_id == "ab-tests",
        ),
        InteractiveTourStep(
            step_id="ai-lab-ab",
            title_factory=lambda: tr("3. Banc d'essai A/B"),
            text_factory=lambda: tr("Comparez objectivement deux stratégies de génération sur un même fragment avant de les adopter."),
            target_view_id="ab-tests",
        ),
    ]


def _build_templates_track_steps() -> list[InteractiveTourStep]:
    return [
        InteractiveTourStep(
            step_id="templates-models",
            title_factory=lambda: tr("1. Types de note et Gabarits Jinja2"),
            text_factory=lambda: tr("Inspectez les modèles Basique, Texte à trous et Démonstration (KaTeX) fournis dans l'exemple, puis revenez dans « Édition & Navigateur »."),
            target_view_id="card-models",
            completion_event=ViewNavigatedEvent,
            completion_predicate=lambda ev: isinstance(ev, ViewNavigatedEvent) and ev.view_id == "edition",
        ),
        InteractiveTourStep(
            step_id="templates-preview",
            title_factory=lambda: tr("2. Directives Cloze, KaTeX et aperçu"),
            text_factory=lambda: tr("Basculez le panneau d'aperçu en direct dans l'éditeur pour contrôler le rendu des formules KaTeX et des occlusions."),
            target_view_id="edition",
            completion_event=CardPreviewToggledEvent,
        ),
    ]


def _build_default_track_steps() -> list[InteractiveTourStep]:
    return [
        InteractiveTourStep(
            step_id="default-dashboard",
            title_factory=lambda: tr("Atelier AnkiDraft"),
            text_factory=lambda: tr("Explorez vos documents, révisez vos cartes en lot, éditez avec aperçu en direct et auditez la qualité selon Wozniak."),
            target_view_id="dashboard",
        ),
        InteractiveTourStep(
            step_id="default-edition",
            title_factory=lambda: tr("Édition et aperçu des cartes"),
            text_factory=lambda: tr("Ouvrez une note dans l'éditeur pour inspecter son rendu recto-verso et l'exporter vers Anki (.apkg)."),
            target_view_id="edition",
        ),
    ]


_TRACK_STEP_BUILDERS: dict[str, Callable[[], list[InteractiveTourStep]]] = {
    TOUR_TRACK_CORE: _build_core_track_steps,
    TOUR_TRACK_BATCH: _build_batch_track_steps,
    TOUR_TRACK_AI_LAB: _build_ai_lab_track_steps,
    TOUR_TRACK_TEMPLATES: _build_templates_track_steps,
}


def build_tour_track_steps(track_id: str) -> list[InteractiveTourStep]:
    """Construit la liste déclarative des étapes d'un parcours nommé."""
    builder = _TRACK_STEP_BUILDERS.get(track_id, _build_default_track_steps)
    return builder()


_STATUS_PILL_ATTRS: dict[TourTrackStatus, tuple[tuple[str, str], tuple[str, str], tuple[str, str]]] = {
    "done": (("color_green_bg", "COLOR_GREEN_BG"), ("color_green_border", "COLOR_GREEN_BORDER"), ("color_green_text", "COLOR_GREEN_TEXT")),
    "in_progress": (("accent_bg", "ACCENT_BG"), ("accent_border", "ACCENT_BORDER"), ("color_purple_text", "COLOR_PURPLE_TEXT")),
    "todo": (("bg_panel", "BG_PANEL"), ("border_color", "BORDER_COLOR"), ("text_muted", "TEXT_MUTED")),
}


def _resolve_token(profile: Any, profile_attr: str, design_attr: str) -> str:
    value = getattr(profile, profile_attr, "") if profile is not None else ""
    return str(value or getattr(DesignTokens, design_attr))


class _TourTrackCard(QFrame):
    """Carte de module dans le Hub du Tutoriel affichant statut et bouton de lancement."""

    launch_requested = Signal(str)

    def __init__(
        self,
        track_id: str,
        icon_name: str,
        title_factory: Callable[[], str],
        desc_factory: Callable[[], str],
        *,
        featured: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.track_id = track_id
        self._icon_name = icon_name
        self._title_factory = title_factory
        self._desc_factory = desc_factory
        self._featured = featured
        self._status: TourTrackStatus = "todo"
        self._last_profile: Any = None

        self.setObjectName("TourTrackFeaturedCard" if featured else "TourTrackModuleCard")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._build_ui()
        self.set_status("todo")

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(12, 10, 12, 10)
        root.setSpacing(6)

        top = QHBoxLayout()
        top.setSpacing(8)
        self.lbl_icon = QLabel(self)
        self.lbl_icon.setFixedSize(18, 18)
        top.addWidget(self.lbl_icon)

        self.lbl_title = QLabel(self._title_factory(), self)
        self.lbl_title.setFont(QFont(DesignTokens.FONT_MAIN, 12 if self._featured else 11, QFont.Weight.Bold))
        self.lbl_title.setWordWrap(True)
        top.addWidget(self.lbl_title, 1)

        self.lbl_badge = QLabel(self)
        self.lbl_badge.setObjectName("TourTrackStatusPill")
        top.addWidget(self.lbl_badge)
        root.addLayout(top)

        self.lbl_desc = QLabel(self._desc_factory(), self)
        self.lbl_desc.setWordWrap(True)
        root.addWidget(self.lbl_desc, 1)

        footer = QHBoxLayout()
        footer.addStretch()
        if self._featured:
            self.btn_launch: PrimaryButton | SecondaryButton = PrimaryButton(self.tr("Lancer le tronc commun"), parent=self)
        else:
            self.btn_launch = SecondaryButton(self.tr("Lancer"), parent=self)
        apply_compact_style(self.btn_launch)
        self.btn_launch.clicked.connect(lambda: self.launch_requested.emit(self.track_id))
        footer.addWidget(self.btn_launch)
        root.addLayout(footer)

    @property
    def current_status(self) -> TourTrackStatus:
        return self._status

    def set_status(self, status: TourTrackStatus) -> None:
        self._status = status
        self.lbl_title.setText(self._title_factory())
        self.lbl_desc.setText(self._desc_factory())
        if status == "done":
            self.lbl_badge.setText(self.tr("Terminé"))
            self.btn_launch.setText(self.tr("Revoir"))
        elif status == "in_progress":
            self.lbl_badge.setText(self.tr("En cours"))
            self.btn_launch.setText(self.tr("Reprendre"))
        else:
            self.lbl_badge.setText(self.tr("À faire"))
            self.btn_launch.setText(self.tr("Lancer le tronc commun") if self._featured else self.tr("Lancer"))
        self.refresh_theme(self._last_profile)

    def refresh_theme(self, profile: Any = None) -> None:
        self._last_profile = profile
        text_primary = _resolve_token(profile, "text_primary", "TEXT_PRIMARY")
        text_secondary = _resolve_token(profile, "text_secondary", "TEXT_SECONDARY")
        accent = _resolve_token(profile, "accent_primary", "ACCENT_PRIMARY")
        bg_card = _resolve_token(profile, *("accent_bg", "ACCENT_BG") if self._featured else ("bg_input", "BG_INPUT"))
        border_card = _resolve_token(profile, *("accent_border", "ACCENT_BORDER") if self._featured else ("border_color", "BORDER_COLOR"))

        self.setStyleSheet(f"""
            QFrame#{self.objectName()} {{
                background-color: {bg_card};
                border: 1px solid {border_card};
                border-radius: {DesignTokens.RADIUS_MD}px;
            }}
        """)
        self.lbl_title.setStyleSheet(f"color: {text_primary}; border: none; background: transparent;")
        self.lbl_desc.setStyleSheet(f"color: {text_secondary}; font-size: 11px; border: none; background: transparent;")
        self.lbl_icon.setPixmap(load_phosphor_icon(self._icon_name, color=accent if self._featured else text_primary).pixmap(16, 16))
        self.btn_launch.refresh_theme(profile)

        bg_spec, border_spec, fg_spec = _STATUS_PILL_ATTRS.get(self._status, _STATUS_PILL_ATTRS["todo"])
        pill_bg = _resolve_token(profile, *bg_spec)
        pill_border = _resolve_token(profile, *border_spec)
        pill_fg = _resolve_token(profile, *fg_spec)

        self.lbl_badge.setStyleSheet(f"""
            QLabel#TourTrackStatusPill {{
                background-color: {pill_bg};
                border: 1px solid {pill_border};
                border-radius: {DesignTokens.RADIUS_SM}px;
                color: {pill_fg};
                font-size: 10px;
                font-weight: 600;
                padding: 2px 7px;
            }}
        """)


class TourHubWidget(QFrame):
    """Hub du Tutoriel remplaçant la checklist statique sur le profil Exemple d'introduction."""

    launch_track_requested = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("TourHubWidget")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.track_cards: dict[str, _TourTrackCard] = {}
        self._build_ui()
        self.refresh_theme()
        self.refresh_progress()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(12, 10, 12, 10)
        root.setSpacing(8)

        header = QHBoxLayout()
        header.setSpacing(8)
        self.lbl_header_icon = QLabel(self)
        self.lbl_header_icon.setFixedSize(18, 18)
        header.addWidget(self.lbl_header_icon)

        self.lbl_title = QLabel(self.tr("Hub du Tutoriel Interactif"), self)
        self.lbl_title.setFont(QFont(DesignTokens.FONT_MAIN, 12, QFont.Weight.Bold))
        header.addWidget(self.lbl_title)

        self.lbl_summary = QLabel(self)
        header.addWidget(self.lbl_summary)
        header.addStretch()
        root.addLayout(header)

        core_card = _TourTrackCard(
            TOUR_TRACK_CORE,
            "compass",
            lambda: self.tr("Tronc commun : L'essentiel AnkiDraft"),
            lambda: self.tr("Parcours guidé réactif (5 étapes) : couverture Smart Coverage, Hôpital Wozniak, Garde-Fou MCP, aperçu KaTeX/Cloze et export .apkg."),
            featured=True,
            parent=self,
        )
        core_card.launch_requested.connect(self.launch_track)
        self.track_cards[TOUR_TRACK_CORE] = core_card
        root.addWidget(core_card)

        modules_row = QHBoxLayout()
        modules_row.setSpacing(8)
        module_specs = [
            (
                TOUR_TRACK_BATCH,
                "stack",
                lambda: self.tr("Forge & Batch Factory"),
                lambda: self.tr("Réviser la tâche pré-calculée sur la Section 3."),
            ),
            (
                TOUR_TRACK_AI_LAB,
                "cpu",
                lambda: self.tr("Laboratoire IA"),
                lambda: self.tr("Explorer Éditeur d'Agents, Pipelines DAG et Tests A/B."),
            ),
            (
                TOUR_TRACK_TEMPLATES,
                "swatches",
                lambda: self.tr("Types de note & Jinja2"),
                lambda: self.tr("Inspecter gabarits Cloze, KaTeX et Starter Pack."),
            ),
        ]
        for track_id, icon_name, title_fn, desc_fn in module_specs:
            card = _TourTrackCard(track_id, icon_name, title_fn, desc_fn, featured=False, parent=self)
            card.launch_requested.connect(self.launch_track)
            self.track_cards[track_id] = card
            modules_row.addWidget(card, 1)
        root.addLayout(modules_row)

    def launch_track(self, track_id: str) -> None:
        """Émet la demande d'ouverture d'un parcours nommé."""
        self.launch_track_requested.emit(track_id)

    def status_for_track(self, track_id: str) -> TourTrackStatus:
        """Retourne le statut mémorisé pour un parcours du Hub."""
        card = self.track_cards.get(track_id)
        return card.current_status if card is not None else "todo"

    def refresh_progress(self) -> None:
        """Relit ``app/tour_progress_json`` et synchronise les badges des 4 parcours."""
        progress = load_tour_progress()
        done_count = 0
        for track_id, card in self.track_cards.items():
            status = progress.get(track_id, "todo")
            if status == "done":
                done_count += 1
            card.set_status(status)
        self.lbl_summary.setText(tr("%1/%2 parcours terminés", done_count, len(self.track_cards)))

    def refresh_theme(self, profile: Any = None) -> None:
        """Applique les jetons sémantiques du thème actif au Hub et ses cartes."""
        bg_panel = (profile.bg_panel if profile else "") or DesignTokens.BG_PANEL
        border_color = (profile.border_color if profile else "") or DesignTokens.BORDER_COLOR
        text_primary = (profile.text_primary if profile else "") or DesignTokens.TEXT_PRIMARY
        text_muted = (profile.text_muted if profile else "") or DesignTokens.TEXT_MUTED
        accent = (profile.accent_primary if profile else "") or DesignTokens.ACCENT_PRIMARY

        self.setStyleSheet(f"""
            QFrame#TourHubWidget {{
                background-color: {bg_panel};
                border: 1px solid {border_color};
                border-radius: {DesignTokens.RADIUS_MD}px;
            }}
        """)
        self.lbl_header_icon.setPixmap(load_phosphor_icon("squares-four", color=accent).pixmap(16, 16))
        self.lbl_title.setStyleSheet(f"color: {text_primary}; border: none; background: transparent;")
        self.lbl_summary.setStyleSheet(f"color: {text_muted}; font-size: 11px; border: none; background: transparent;")
        for card in self.track_cards.values():
            card.refresh_theme(profile)
