"""Dialogues d'accueil au premier lancement et de transition hors du profil Exemple d'introduction."""

from __future__ import annotations

import logging
import re
from typing import ClassVar

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from ankidraft.database.seeds.demo_seed import INTRO_PROFILE_ID
from ankidraft.ui.components.buttons import PrimaryButton, SecondaryButton
from ankidraft.ui.components.inputs import StyledLineEdit
from ankidraft.ui.theme import DesignTokens
from ankidraft.utils.icon_loader import load_logo_icon, load_on_accent_icon, load_phosphor_icon

logger = logging.getLogger(__name__)


def sanitize_profile_name(raw_name: str, fallback: str = "default") -> str:
    """Nettoie un nom saisi pour obtenir un identifiant de répertoire de profil valide."""
    cleaned = re.sub(r"[^a-zA-Z0-9_\-]", "_", raw_name.strip())
    cleaned = cleaned.strip("_")
    if not cleaned or cleaned == INTRO_PROFILE_ID:
        return fallback
    return cleaned


class FirstLaunchWelcomeDialog(QDialog):
    """Écran d'accueil au tout premier lancement offrant 3 portes d'entrée explicites."""

    CHOICE_EXPLORE: ClassVar[str] = "explore"
    CHOICE_IMPORT: ClassVar[str] = "import"
    CHOICE_BLANK: ClassVar[str] = "blank"

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.choice: str | None = None
        self.selected_profile_name: str = "default"
        self.setWindowTitle(self.tr("Bienvenue dans AnkiDraft"))
        self.setFixedSize(620, 560)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._build_ui()
        self._apply_style()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 22, 24, 22)
        root.setSpacing(14)

        # En-tête identitaire
        header = QHBoxLayout()
        header.setSpacing(12)
        logo_lbl = QLabel()
        logo_lbl.setPixmap(load_logo_icon(DesignTokens.ACCENT_PRIMARY).pixmap(36, 36))
        logo_lbl.setStyleSheet("border: none; background: transparent;")
        header.addWidget(logo_lbl)

        title_col = QVBoxLayout()
        title_col.setContentsMargins(0, 0, 0, 0)
        title_col.setSpacing(2)
        title_lbl = QLabel(self.tr("Bienvenue dans AnkiDraft"))
        title_lbl.setFont(QFont(DesignTokens.FONT_MAIN, 16, QFont.Weight.Bold))
        title_lbl.setStyleSheet(f"color: {DesignTokens.TEXT_PRIMARY}; border: none; background: transparent;")
        subtitle_lbl = QLabel(self.tr("Choisissez comment démarrer votre premier espace de travail :"))
        subtitle_lbl.setFont(QFont(DesignTokens.FONT_MAIN, 11))
        subtitle_lbl.setStyleSheet(f"color: {DesignTokens.TEXT_SECONDARY}; border: none; background: transparent;")
        title_col.addWidget(title_lbl)
        title_col.addWidget(subtitle_lbl)
        header.addLayout(title_col, 1)
        root.addLayout(header)

        # Porte 1 (Recommandée) : Explorer avec l'Exemple d'introduction
        explore_card = QFrame()
        explore_card.setObjectName("WelcomeExploreCard")
        explore_layout = QVBoxLayout(explore_card)
        explore_layout.setContentsMargins(16, 14, 16, 14)
        explore_layout.setSpacing(8)

        explore_top = QHBoxLayout()
        explore_top.setSpacing(8)
        badge_lbl = QLabel(self.tr("RECOMMANDÉ · SANS CLÉ API"))
        badge_lbl.setFont(QFont(DesignTokens.FONT_MAIN, 9, QFont.Weight.Bold))
        badge_lbl.setStyleSheet(
            f"background-color: {DesignTokens.ACCENT_BG}; color: {DesignTokens.ACCENT_PRIMARY}; border: 1px solid {DesignTokens.ACCENT_BORDER}; border-radius: 6px; padding: 2px 8px;"
        )
        explore_top.addWidget(badge_lbl)
        explore_top.addStretch()
        explore_layout.addLayout(explore_top)

        explore_desc = QLabel(self.tr("Explorez immédiatement un mini-cours complet (Smart Coverage, Hôpital Wozniak, KaTeX/Cloze, Garde-Fou MCP et revue Batch) sans configuration préalable."))
        explore_desc.setWordWrap(True)
        explore_desc.setStyleSheet(f"color: {DesignTokens.TEXT_SECONDARY}; font-size: 12px; border: none; background: transparent;")
        explore_layout.addWidget(explore_desc)

        self.btn_explore = PrimaryButton(self.tr("Explorer avec l'Exemple d'introduction"))
        self.btn_explore.setIcon(load_on_accent_icon("compass"))
        self.btn_explore.clicked.connect(self._on_choose_explore)
        explore_layout.addWidget(self.btn_explore)
        root.addWidget(explore_card)

        # Configuration du nom pour les portes 2 et 3
        direct_card = QFrame()
        direct_card.setObjectName("WelcomeDirectCard")
        direct_layout = QVBoxLayout(direct_card)
        direct_layout.setContentsMargins(16, 14, 16, 14)
        direct_layout.setSpacing(10)

        name_row = QHBoxLayout()
        name_row.setSpacing(8)
        name_lbl = QLabel(self.tr("Nom du profil personnel :"))
        name_lbl.setFont(QFont(DesignTokens.FONT_MAIN, 11, QFont.Weight.DemiBold))
        name_lbl.setStyleSheet(f"color: {DesignTokens.TEXT_PRIMARY}; border: none; background: transparent;")
        self.profile_name_input = StyledLineEdit()
        self.profile_name_input.setPlaceholderText("default")
        name_row.addWidget(name_lbl)
        name_row.addWidget(self.profile_name_input, 1)
        direct_layout.addLayout(name_row)

        # Porte 2 : Importer collection Anki
        self.btn_import = SecondaryButton(self.tr("Importer ma collection Anki (.apkg / .colpkg)"))
        self.btn_import.setIcon(load_phosphor_icon("ph.download-simple", color=DesignTokens.TEXT_PRIMARY))
        self.btn_import.setToolTip(self.tr("Passe la présentation guidée et ouvre directement l'import Anki."))
        self.btn_import.clicked.connect(self._on_choose_import)
        self.import_hint_lbl = QLabel(self.tr("Passe la présentation guidée et ouvre directement la boîte d'importation."))
        self.import_hint_lbl.setStyleSheet(f"color: {DesignTokens.TEXT_MUTED}; font-size: 11px; border: none; background: transparent;")
        direct_layout.addWidget(self.btn_import)
        direct_layout.addWidget(self.import_hint_lbl)

        # Porte 3 : Démarrer un espace vierge
        self.btn_blank = SecondaryButton(self.tr("Démarrer un espace vierge"))
        self.btn_blank.setIcon(load_phosphor_icon("ph.plus-circle", color=DesignTokens.TEXT_PRIMARY))
        self.btn_blank.setToolTip(self.tr("Passe la présentation guidée et démarre un profil vierge."))
        self.btn_blank.clicked.connect(self._on_choose_blank)
        self.blank_hint_lbl = QLabel(self.tr("Passe la présentation guidée et crée un espace prêt à accueillir vos documents."))
        self.blank_hint_lbl.setStyleSheet(f"color: {DesignTokens.TEXT_MUTED}; font-size: 11px; border: none; background: transparent;")
        direct_layout.addWidget(self.btn_blank)
        direct_layout.addWidget(self.blank_hint_lbl)

        root.addWidget(direct_card)
        root.addStretch()

    def _apply_style(self) -> None:
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {DesignTokens.BG_MAIN};
                color: {DesignTokens.TEXT_PRIMARY};
            }}
            QFrame#WelcomeExploreCard {{
                background-color: {DesignTokens.BG_PANEL};
                border: 1.5px solid {DesignTokens.ACCENT_BORDER};
                border-radius: {DesignTokens.RADIUS_MD}px;
            }}
            QFrame#WelcomeDirectCard {{
                background-color: {DesignTokens.BG_PANEL};
                border: 1px solid {DesignTokens.BORDER_COLOR};
                border-radius: {DesignTokens.RADIUS_MD}px;
            }}
        """)

    def _on_choose_explore(self) -> None:
        self.choice = self.CHOICE_EXPLORE
        self.selected_profile_name = INTRO_PROFILE_ID
        self.accept()

    def _on_choose_import(self) -> None:
        self.choice = self.CHOICE_IMPORT
        self.selected_profile_name = sanitize_profile_name(self.profile_name_input.text(), fallback="default")
        self.accept()

    def _on_choose_blank(self) -> None:
        self.choice = self.CHOICE_BLANK
        self.selected_profile_name = sanitize_profile_name(self.profile_name_input.text(), fallback="default")
        self.accept()

    def get_selection(self) -> tuple[str, str]:
        """Retourne ``(choix, profile_id)`` sélectionné par l'utilisateur."""
        return (self.choice or self.CHOICE_BLANK, self.selected_profile_name)


class LeaveDemoProfileDialog(QDialog):
    """Dialogue permettant de basculer du profil d'exemple vers un espace personnel."""

    def __init__(self, default_target: str = "default", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(self.tr("Passer à mon espace de travail"))
        self.setFixedSize(460, 240)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(12)

        desc = QLabel(self.tr("Choisissez ou nommez votre espace de travail personnel. Vous pourrez toujours retrouver l'Exemple d'introduction plus tard."))
        desc.setWordWrap(True)
        desc.setStyleSheet(f"color: {DesignTokens.TEXT_SECONDARY}; font-size: 12px;")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(8)
        lbl = QLabel(self.tr("Nom de l'espace :"))
        lbl.setStyleSheet(f"color: {DesignTokens.TEXT_PRIMARY}; font-weight: 600;")
        self.target_profile_input = StyledLineEdit()
        self.target_profile_input.setText(default_target)
        row.addWidget(lbl)
        row.addWidget(self.target_profile_input, 1)
        layout.addLayout(row)

        self.delete_intro_checkbox = QCheckBox(self.tr("Supprimer le profil Exemple d'introduction après bascule"))
        self.delete_intro_checkbox.setChecked(True)
        self.delete_intro_checkbox.setStyleSheet(f"color: {DesignTokens.TEXT_PRIMARY};")
        layout.addWidget(self.delete_intro_checkbox)

        layout.addStretch()

        buttons = QHBoxLayout()
        buttons.setSpacing(8)
        buttons.addStretch()
        self.btn_cancel = SecondaryButton(self.tr("Annuler"))
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_confirm = PrimaryButton(self.tr("Basculer maintenant"))
        self.btn_confirm.setIcon(load_on_accent_icon("arrow-right"))
        self.btn_confirm.clicked.connect(self.accept)
        buttons.addWidget(self.btn_cancel)
        buttons.addWidget(self.btn_confirm)
        layout.addLayout(buttons)

        self.setStyleSheet(f"""
            QDialog {{
                background-color: {DesignTokens.BG_MAIN};
                color: {DesignTokens.TEXT_PRIMARY};
            }}
        """)

    def target_profile_name(self) -> str:
        """Retourne l'identifiant nettoyé du profil cible."""
        return sanitize_profile_name(self.target_profile_input.text(), fallback="default")

    def should_delete_intro(self) -> bool:
        """Indique si l'utilisateur souhaite supprimer ``intro-example`` après la bascule."""
        return self.delete_intro_checkbox.isChecked()
