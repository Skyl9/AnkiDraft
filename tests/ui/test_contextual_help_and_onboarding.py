from __future__ import annotations

from pathlib import Path
from typing import Any

from PySide6.QtWidgets import QWidget

from ankidraft.ui.components import ContextHelpButton
from ankidraft.ui.dialogs.doc_reader_dialog import DocReaderDialog


def test_doc_reader_generates_toc_anchors_and_scrolls(qtbot: Any) -> None:
    dlg = DocReaderDialog()
    qtbot.addWidget(dlg)
    dlg.load_markdown(
        "# Titre Principal\n\nIntro\n\n## Section Cible\n\nContenu détaillé de la section.\n",
        title="Guide Test",
    )
    html = dlg.text_browser.toHtml()
    assert 'id="section-cible"' in html or 'name="section-cible"' in html
    assert dlg.scroll_to_anchor("section-cible") is True
    assert dlg.scroll_to_anchor("") is False


def test_doc_reader_open_at_resolves_page_and_anchor(qtbot: Any, monkeypatch: Any, tmp_path: Path) -> None:
    docs_dir = tmp_path / "docs"
    (docs_dir / "cards").mkdir(parents=True)
    target = docs_dir / "cards" / "dag_et_rag.md"
    target.write_text("# DAG et RAG\n\n## Etape Map Reduce\n\nExplication.", encoding="utf-8")

    monkeypatch.setattr("ankidraft.ui.dialogs.doc_reader_dialog.get_user_docs_path", lambda: docs_dir)
    monkeypatch.setattr("ankidraft.ui.dialogs.doc_reader_dialog.get_docs_path", lambda: docs_dir)

    dlg = DocReaderDialog.open_at("cards/dag_et_rag.md#etape-map-reduce")
    qtbot.addWidget(dlg)
    assert "DAG et RAG" in dlg.lbl_title.text()
    assert "Explication." in dlg.text_browser.toPlainText()


def test_context_help_button_opens_doc_reader_at_target(qtbot: Any, monkeypatch: Any) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)

    captured: list[tuple[str, str]] = []

    class _FakeDlg:
        def show(self) -> None:
            pass

        def raise_(self) -> None:
            pass

    def _fake_open_at(cls: Any, page_path: str, anchor: str = "", parent: QWidget | None = None) -> _FakeDlg:
        captured.append((page_path, anchor))
        return _FakeDlg()

    monkeypatch.setattr(DocReaderDialog, "open_at", classmethod(_fake_open_at))

    btn = ContextHelpButton("cards/dag_et_rag.md", "etape-map-reduce", parent=parent)
    qtbot.addWidget(btn)
    btn.click()

    assert captured == [("cards/dag_et_rag.md", "etape-map-reduce")]


def test_empty_state_widget_with_guide_button(qtbot: Any, monkeypatch: Any) -> None:
    from ankidraft.ui.components import EmptyStateWidget, PrimaryButton

    captured: list[tuple[str, str]] = []

    class _FakeDlg:
        def show(self) -> None:
            pass

        def raise_(self) -> None:
            pass

    def _fake_open_at(cls: Any, page_path: str, anchor: str = "", parent: QWidget | None = None) -> _FakeDlg:
        captured.append((page_path, anchor))
        return _FakeDlg()

    monkeypatch.setattr(DocReaderDialog, "open_at", classmethod(_fake_open_at))

    primary = PrimaryButton("Action")
    empty = EmptyStateWidget(
        icon_name="ph.shield-check",
        title="Vide",
        description="Desc",
        action_button=primary,
        guide_page="ai-setup/consultant_mcp.md",
        guide_anchor="2-garde-fou",
    )
    qtbot.addWidget(empty)
    assert empty.guide_button is not None
    empty.guide_button.click()
    assert captured == [("ai-setup/consultant_mcp.md", "2-garde-fou")]


def test_view_tour_steps_and_preserve_flag(qtbot: Any) -> None:
    from ankidraft.ui.widgets.tour_guide import create_view_tour_steps, start_view_tour

    host = QWidget()
    qtbot.addWidget(host)

    for key in ("documents", "creation", "pipelines", "analysis", "consultant", "card_models"):
        steps = create_view_tour_steps(key, host)
        assert 3 <= len(steps) <= 4

    bubble = start_view_tour("pipelines", host, parent_window=host)
    qtbot.addWidget(bubble)
    assert bubble.preserve_completion_flag is True
    bubble.end_tour()
