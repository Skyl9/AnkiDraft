"""Tour Guide & Onboarding interactif pour AnkiForge.

Fournit à la fois les bulles d'aide contextuelles par vue (``TourBubble``)
et le moteur compagnon non bloquant piloté par événements (``InteractiveTourController``
et ``TourCompanionCard``).
"""

from __future__ import annotations

import contextlib
import logging
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

from PySide6.QtCore import QEvent, QObject, QPoint, Qt, Signal
from PySide6.QtGui import QScreen
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from ankidraft.ui.components.buttons import ActionButton, PrimaryButton, apply_compact_style
from ankidraft.ui.theme import DesignTokens, apply_shadow
from ankidraft.utils.event_bus import AppEvent, AppEventBus, event_bus
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
    completion_event: type[AppEvent] | None = None
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
        self._active_subscription: tuple[type[AppEvent], Callable[[AppEvent], None]] | None = None
        self._card: TourCompanionCard | None = None
        self._host_filter_installed = False

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

        event_cls = step.completion_event

        def _handler(ev: AppEvent) -> None:
            self._on_step_event(ev)

        self._event_bus.subscribe(event_cls, _handler)
        self._active_subscription = (event_cls, _handler)

    def _unsubscribe_current_event(self) -> None:
        if self._active_subscription is None:
            return
        event_cls, handler = self._active_subscription
        self._event_bus.unsubscribe(event_cls, handler)
        self._active_subscription = None

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
