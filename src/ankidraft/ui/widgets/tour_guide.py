"""Tour Guide & Onboarding interactif pour AnkiForge.

Affiche une bulle d'aide flottante guidant l'utilisateur à travers les zones clés de l'application.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtGui import QColor, QScreen
from PySide6.QtWidgets import (
    QApplication,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from ankidraft.ui.components.buttons import ActionButton, PrimaryButton
from ankidraft.ui.theme import DesignTokens
from ankidraft.utils.i18n import tr
from ankidraft.utils.icon_loader import load_on_accent_icon

logger = logging.getLogger(__name__)


@dataclass
class TourStep:
    """Étape individuelle de la visite guidée."""

    title: str
    text: str
    target_widget: QWidget | None = None
    target_widget_getter: Callable[[], QWidget | None] | None = None
    action: Callable[[], None] | None = None


class TourBubble(QWidget):
    """La bulle d'information flottante qui guide l'utilisateur."""

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

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24)
        shadow.setColor(QColor(0, 0, 0, 160))
        shadow.setOffset(0, 6)
        self.bg_frame.setGraphicsEffect(shadow)

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

        # --- BARRE DE BOUTONS ---
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        self.btn_skip = ActionButton("x", " Quitter", parent=self)
        self.btn_skip.clicked.connect(self.end_tour)
        btn_layout.addWidget(self.btn_skip)

        btn_layout.addStretch()

        self.btn_prev = ActionButton("arrow-left", " Précédent", parent=self)
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

        self.btn_next = PrimaryButton("Suivant ", parent=self)
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

        # Gestion des boutons
        self.btn_prev.setVisible(self.current_step > 0)

        if self.current_step == len(self.steps) - 1:
            self.btn_next.setText(self.tr(" Terminer"))
            self.btn_next.setIcon(load_on_accent_icon("check"))
        else:
            self.btn_next.setText(self.tr(" Suivant"))
            self.btn_next.setIcon(load_on_accent_icon("arrow-right"))

        QApplication.processEvents()

        # Résolution du widget cible
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

        # Essayer d'abord à droite
        if target_pos.x() + target_widget.width() + 16 + self.width() <= screen_rect.right():
            x = target_pos.x() + target_widget.width() + 16
            y = target_pos.y()
        # Sinon à gauche
        elif target_pos.x() - self.width() - 16 >= screen_rect.left():
            x = target_pos.x() - self.width() - 16
            y = target_pos.y()
        # Sinon en-dessous
        else:
            x = max(screen_rect.left() + 10, target_pos.x())
            y = target_pos.y() + target_widget.height() + 16

        # Clamping vertical
        if y + self.height() > screen_rect.bottom() - 16:
            y = screen_rect.bottom() - self.height() - 16
        if y < screen_rect.top() + 16:
            y = screen_rect.top() + 16

        # Clamping horizontal
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


def create_default_tour_steps(main_window: Any) -> list[TourStep]:
    """Génère le parcours d'onboarding standard pour AnkiDraft."""
    return [
        TourStep(
            title="✨ Bienvenue dans AnkiDraft",
            text=(
                "AnkiDraft est votre atelier professionnel de création, d'ingestion "
                "et d'audit de cartes Anki assisté par IA.\n\n"
                "Ce guide rapide vous présente en 5 étapes les zones clés de l'application."
            ),
            target_widget=None,
        ),
        TourStep(
            title="🧭 Barre de Navigation & Espaces",
            text=(
                "La barre latérale regroupe tous vos ateliers : Tableau de bord, Studio de création, "
                "Éditeur de notes, Audit Wozniak & SRS, Consultant IA, Pipelines et Laboratoire A/B.\n"
                "Vous pouvez la replier à tout moment pour maximiser votre espace de travail."
            ),
            target_widget_getter=lambda: getattr(main_window, "sidebar", None),
        ),
        TourStep(
            title="⚡ Studio de Création & Ingestion",
            text=("Transformez vos cours et documents (PDF, Markdown, pages web, vidéos YouTube) en cartes mémoires atomiques de haute qualité grâce à l'IA et aux pipelines modulaires."),
            target_widget_getter=lambda: main_window.sidebar._items.get("creation") if hasattr(main_window, "sidebar") and hasattr(main_window.sidebar, "_items") else None,
            action=lambda: main_window._on_view_selected("creation") if hasattr(main_window, "_on_view_selected") else None,
        ),
        TourStep(
            title="🎴 Édition & Navigateur de Cartes",
            text=(
                "Visualisez, filtrez et peaufinez vos notes avec aperçu en temps réel (Bureau, Tablette, Mobile). Profitez du support KaTeX, du gestionnaire de cloze et de l'historique Time Machine."
            ),
            target_widget_getter=lambda: main_window.sidebar._items.get("edition") if hasattr(main_window, "sidebar") and hasattr(main_window.sidebar, "_items") else None,
            action=lambda: main_window._on_view_selected("edition") if hasattr(main_window, "_on_view_selected") else None,
        ),
        TourStep(
            title="🔬 Analyse, Audit Wozniak & RAG",
            text=(
                "Vérifiez l'atomicité et l'efficacité mémorielle de vos cartes selon les 20 règles de Piotr Wozniak. "
                "Identifiez les lacunes documentaires et projetez votre charge de révision à l'équilibre (FSRS)."
            ),
            target_widget_getter=lambda: main_window.sidebar._items.get("analysis") if hasattr(main_window, "sidebar") and hasattr(main_window.sidebar, "_items") else None,
            action=lambda: main_window._on_view_selected("analysis") if hasattr(main_window, "_on_view_selected") else None,
        ),
        TourStep(
            title="🤖 Consultant IA & Palette de Commandes",
            text=(
                "Votre copilote autonome disponible pour auditer ou enrichir vos paquets. "
                "Astuce : ouvrez la Palette de commandes à tout moment via Ctrl+K / ⌘K "
                "pour rechercher et naviguer instantanément !"
            ),
            target_widget_getter=lambda: main_window.sidebar._items.get("consultant") if hasattr(main_window, "sidebar") and hasattr(main_window.sidebar, "_items") else None,
            action=lambda: main_window._on_view_selected("consultant") if hasattr(main_window, "_on_view_selected") else None,
        ),
    ]


def create_view_tour_steps(view_key: str, view_widget: QWidget) -> list[TourStep]:
    """Génère une mini-visite guidée thématique (3 à 4 étapes) pour une vue donnée."""
    from ankidraft.utils.i18n import tr

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
