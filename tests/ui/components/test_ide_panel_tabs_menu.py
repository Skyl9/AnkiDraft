"""Tests headless pytest-qt pour le catalogue et menu d'onglets d'IdePanel (résorption CRAP)."""

from __future__ import annotations

from typing import Any

import pytest
from PySide6.QtWidgets import QHBoxLayout, QStackedWidget, QWidget
from pytestqt.qtbot import QtBot

from ankidraft.ui.components.panels import IdePanel
from ankidraft.ui.theme import StyledMenu

pytestmark = pytest.mark.ui


def _build_two_panels_view(qtbot: QtBot) -> tuple[QStackedWidget, IdePanel, IdePanel]:
    """Construit une vue conteneur avec deux IdePanel frères dans un QStackedWidget."""
    stack = QStackedWidget()
    qtbot.addWidget(stack)
    container = QWidget()
    layout = QHBoxLayout(container)
    panel_a = IdePanel()
    panel_b = IdePanel()
    layout.addWidget(panel_a)
    layout.addWidget(panel_b)
    stack.addWidget(container)
    stack.show()
    return stack, panel_a, panel_b


def test_ide_panel_collect_view_tabs_catalog_categories(qtbot: QtBot) -> None:
    """Catégorise fidèlement onglets ouverts ici, ouverts ailleurs et fermés."""
    _stack, panel_a, panel_b = _build_two_panels_view(qtbot)

    panel_a.register_tab("Principal", QWidget(), icon_name="ph.house", closable=False, active_by_default=True)
    panel_a.register_tab("Actif A", QWidget(), icon_name="ph.file-text", closable=True, active_by_default=True)
    panel_a.register_tab("Fermé", QWidget(), icon_name="ph.folder", closable=True, active_by_default=False)
    panel_b.register_tab("Ailleurs B", QWidget(), icon_name="ph.cards", closable=True, active_by_default=True)

    open_here, open_elsewhere, closed = panel_a._collect_view_tabs_catalog()

    assert open_here == ["Principal", "Actif A"]
    assert open_elsewhere == ["Ailleurs B"]
    assert [title for title, _info in closed] == ["Fermé"]


def test_ide_panel_tabs_menu_populates_and_triggers_actions(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Peuple le StyledMenu des onglets et exécute réouverture, déplacement et masquage."""
    _stack, panel_a, panel_b = _build_two_panels_view(qtbot)

    panel_a.register_tab("Principal", QWidget(), icon_name="ph.house", closable=False, active_by_default=True)
    panel_a.register_tab("Actif A", QWidget(), icon_name="ph.file-text", closable=True, active_by_default=True)
    panel_a.register_tab("Fermé", QWidget(), icon_name="ph.folder", closable=True, active_by_default=False)
    panel_b.register_tab("Ailleurs B", QWidget(), icon_name="ph.cards", closable=True, active_by_default=True)

    captured_menus: list[StyledMenu] = []

    def _fake_exec(self_menu: StyledMenu, *_args: Any, **_kwargs: Any) -> None:
        captured_menus.append(self_menu)

    monkeypatch.setattr(StyledMenu, "exec", _fake_exec)

    panel_a._show_tabs_menu()
    assert len(captured_menus) == 1
    menu = captured_menus[0]

    actions_by_text = {act.text(): act for act in menu.actions() if act.text()}
    assert "Rouvrir un onglet :" in actions_by_text
    assert "Déplacer vers ce panneau :" in actions_by_text
    assert "Onglets actifs dans ce panneau :" in actions_by_text

    assert actions_by_text["Principal"].isEnabled() is False
    assert actions_by_text["Actif A"].isChecked() is True
    assert actions_by_text["Fermé"].isChecked() is False

    # 1. Déclenche réouverture d'un onglet fermé
    actions_by_text["Fermé"].trigger()
    assert any(btn.text().strip() == "Fermé" for btn in panel_a.tabs_bar.tabs)

    # 2. Déclenche déplacement d'un onglet ouvert ailleurs
    actions_by_text["Ailleurs B"].trigger()
    assert any(btn.text().strip() == "Ailleurs B" for btn in panel_a.tabs_bar.tabs)
    assert not any(btn.text().strip() == "Ailleurs B" for btn in panel_b.tabs_bar.tabs)

    # 3. Déclenche masquage d'un onglet actif fermable
    actions_by_text["Actif A"].trigger()
    assert not any(btn.text().strip() == "Actif A" for btn in panel_a.tabs_bar.tabs)


def test_ide_panel_tabs_menu_empty_state(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Affiche une entrée désactivée « Aucun onglet disponible » lorsque le catalogue est vide."""
    panel = IdePanel()
    qtbot.addWidget(panel)

    captured_menus: list[StyledMenu] = []
    monkeypatch.setattr(StyledMenu, "exec", lambda self_menu, *a, **kw: captured_menus.append(self_menu))

    panel._show_tabs_menu()
    assert len(captured_menus) == 1
    actions = captured_menus[0].actions()
    assert len(actions) == 1
    assert actions[0].text() == "Aucun onglet disponible"
    assert actions[0].isEnabled() is False
