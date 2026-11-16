"""Tests headless pytest-qt pour InlineDiffCardWidget (résorption CRAP)."""

from __future__ import annotations

import json
import uuid
from typing import Any

import pytest
from pytestqt.qtbot import QtBot

from ankidraft.database.models import (
    CardModel,
    DeckModel,
    NoteModel,
    NoteTypeModel,
    NoteVersionModel,
)
from ankidraft.services.ai.staged_patch_registry import StagedPatchRegistry
from ankidraft.ui.views.consultant_view.widgets.inline_diff_card_widget import InlineDiffCardWidget

pytestmark = pytest.mark.ui


def _create_note_with_deck(front: str = "Ancienne question", back: str = "Ancienne réponse") -> tuple[NoteTypeModel, DeckModel, NoteModel]:
    """Crée un type de note, un paquet et une note avec sa version initiale active."""
    uid = uuid.uuid4().hex[:6]
    nt = NoteTypeModel.create(
        name=f"NT_DIFF_{uid}",
        fields_schema='["Front", "Back"]',
        templates='[{"name": "Carte 1", "qfmt": "{{Front}}", "afmt": "{{Back}}"}]',
        css_style=".card { color: black; }",
    )
    deck = DeckModel.create(name=f"Deck_DIFF_{uid}")
    note = NoteModel.create(guid=f"guid_{uid}", note_type=nt, tags=json.dumps(["tag1"]))
    NoteVersionModel.create(
        note=note,
        version_number=1,
        content=json.dumps({"Front": front, "Back": back}),
        source="manual",
        is_active=True,
    )
    CardModel.create(note=note, deck=deck, template_index=0)
    return nt, deck, note


def test_inline_diff_card_apply_edit_and_revert(qtbot: QtBot) -> None:
    """Couvre le rendu champ par champ, la retouche directe, l'application en BDD et le revert."""
    _nt, _deck, note = _create_note_with_deck()

    patch_data: dict[str, Any] = {
        "type": "card",
        "title": "Améliorer la formulation",
        "explanation": "Question rendue plus atomique.",
        "note_id": note.id,
        "original": {"Front": "Ancienne question", "Back": "Ancienne réponse"},
        "modified": {"Front": "Nouvelle question", "Back": "Nouvelle réponse"},
    }
    widget = InlineDiffCardWidget(patch_data)
    qtbot.addWidget(widget)
    widget.show()

    assert len(widget.field_widgets) == 2
    assert widget.btn_apply.isEnabled()
    assert widget.btn_reject.isEnabled()

    # Bascule ratures et mode édition directe sur le premier champ
    fw_front = widget.field_widgets[0]
    fw_front.btn_toggle_deletions.click()
    assert fw_front.show_deletions is True
    fw_front.btn_mode_toggle.click()
    fw_front.editor.setPlainText("Question retouchée par utilisateur")
    assert fw_front.get_current_value() == "Question retouchée par utilisateur"

    applied_signals: list[str] = []
    widget.applied.connect(applied_signals.append)

    widget.btn_apply.click()

    assert widget.is_applied is True
    assert not widget.btn_reject.isEnabled()
    assert "Revert" in widget.btn_apply.text()
    assert len(applied_signals) == 1

    active_v = note.versions.where(NoteVersionModel.is_active == True).first()  # noqa: E712
    assert active_v is not None
    assert json.loads(active_v.content)["Front"] == "Question retouchée par utilisateur"

    # Annulation (Revert) en cliquant à nouveau sur le bouton
    reverted_signals: list[str] = []
    widget.reverted.connect(reverted_signals.append)
    widget.btn_apply.click()

    assert widget.is_applied is False
    assert widget.btn_reject.isEnabled()
    assert len(reverted_signals) == 1
    reverted_v = note.versions.where(NoteVersionModel.is_active == True).first()  # noqa: E712
    assert reverted_v is not None
    assert json.loads(reverted_v.content)["Front"] == "Ancienne question"


def test_inline_diff_card_detects_already_applied_from_db(qtbot: QtBot) -> None:
    """Détecte au montage si la note en BDD reflète déjà les valeurs modifiées et restaure original."""
    _nt, _deck, note = _create_note_with_deck(front="V1 Front", back="V1 Back")
    v1 = note.versions.where(NoteVersionModel.is_active == True).first()  # noqa: E712
    assert v1 is not None
    v1.is_active = False
    v1.save()
    NoteVersionModel.create(
        note=note,
        version_number=2,
        content=json.dumps({"Front": "V2 Front", "Back": "V2 Back"}),
        source="ai",
        is_active=True,
    )

    widget = InlineDiffCardWidget(
        {
            "type": "card",
            "note_id": note.id,
            "original": {},
            "modified": {"Front": "V2 Front", "Back": "V2 Back"},
        }
    )
    qtbot.addWidget(widget)

    assert widget.is_applied is True
    assert not widget.btn_reject.isEnabled()
    assert "Revert" in widget.btn_apply.text()
    assert widget.field_widgets[0].original_val == "V1 Front"


def test_inline_diff_card_staged_patch_apply_conflict_and_failure(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Couvre l'application d'un StagedPatch pending, les conflits et les échecs."""
    _nt, _deck, note = _create_note_with_deck()

    staged = StagedPatchRegistry.create_patch(
        patch_type="card_refactor",
        target_id=note.id,
        diff_payload={
            "type": "card",
            "note_id": note.id,
            "original": {"Front": "Ancienne question", "Back": "Ancienne réponse"},
            "modified": {"Front": "Staged Front", "Back": "Ancienne réponse"},
        },
    )

    # 1. Conflit de version
    monkeypatch.setattr(
        StagedPatchRegistry,
        "apply_staged_patch",
        staticmethod(lambda _pid: {"status": "conflict", "message": "Conflit détecté"}),
    )
    w_conflict = InlineDiffCardWidget(
        {
            "type": "card",
            "patch_id": staged.patch_id,
            "note_id": note.id,
            "original": {"Front": "Ancienne question", "Back": "Ancienne réponse"},
            "modified": {"Front": "Staged Front", "Back": "Ancienne réponse"},
        }
    )
    qtbot.addWidget(w_conflict)
    w_conflict.btn_apply.click()
    assert w_conflict.is_applied is False
    assert "Conflit" in w_conflict.status_badge.text()

    # 2. Échec générique
    monkeypatch.setattr(
        StagedPatchRegistry,
        "apply_staged_patch",
        staticmethod(lambda _pid: {"status": "error", "message": "Erreur test"}),
    )
    w_err = InlineDiffCardWidget(
        {
            "type": "card",
            "patch_id": staged.patch_id,
            "note_id": note.id,
            "original": {"Front": "Ancienne question", "Back": "Ancienne réponse"},
            "modified": {"Front": "Staged Front", "Back": "Ancienne réponse"},
        }
    )
    qtbot.addWidget(w_err)
    w_err.btn_apply.click()
    assert w_err.is_applied is False

    # 3. Succès nominal avec synchronisation de la retouche directe
    captured_payloads: list[dict[str, Any]] = []

    def _fake_apply(pid: str) -> dict[str, Any]:
        refreshed = StagedPatchRegistry.get_patch(pid)
        assert refreshed is not None
        captured_payloads.append(json.loads(refreshed.diff_payload))
        return {"status": "applied", "message": "Patch appliqué !"}

    monkeypatch.setattr(StagedPatchRegistry, "apply_staged_patch", staticmethod(_fake_apply))
    w_ok = InlineDiffCardWidget(
        {
            "type": "card",
            "patch_id": staged.patch_id,
            "note_id": note.id,
            "original": {"Front": "Ancienne question", "Back": "Ancienne réponse"},
            "modified": {"Front": "Staged Front", "Back": "Ancienne réponse"},
        }
    )
    qtbot.addWidget(w_ok)
    w_ok.field_widgets[0].sbs_editor.setPlainText("Staged Front Modifié")
    w_ok.btn_apply.click()

    assert w_ok.is_applied is True
    assert captured_payloads[0]["modified"]["Front"] == "Staged Front Modifié"


def test_inline_diff_card_css_and_split_patches(qtbot: QtBot) -> None:
    """Couvre les modes CSS et scission (split) avec sélection partielle de cartes atomiques."""
    nt, deck, note = _create_note_with_deck()

    # 1. CSS patch
    css_widget = InlineDiffCardWidget(
        {
            "type": "css",
            "title": "Ajouter style CSS",
            "modified": ".card { font-size: 18px; }",
            "metadata": {"note_type_name": nt.name, "snippet": ".card { font-size: 18px; }"},
        }
    )
    qtbot.addWidget(css_widget)
    assert hasattr(css_widget, "diff_view")
    css_widget.btn_apply.click()

    refreshed_nt = NoteTypeModel.get_by_id(nt.id)
    assert ".card { font-size: 18px; }" in refreshed_nt.css_style
    assert not css_widget.btn_apply.isEnabled()
    assert not css_widget.btn_reject.isEnabled()

    # 2. Split patch (2 cartes, 1 décochée)
    split_widget = InlineDiffCardWidget(
        {
            "type": "split",
            "title": "Scinder la note",
            "note_id": note.id,
            "modified": [
                {"Front": "Atome 1", "Back": "R1"},
                {"Front": "Atome 2", "Back": "R2"},
            ],
        }
    )
    qtbot.addWidget(split_widget)
    assert len(split_widget.split_widgets) == 2
    split_widget.split_widgets[1].chk_include.setChecked(False)
    split_widget.btn_apply.click()

    refreshed_note = NoteModel.get_by_id(note.id)
    assert refreshed_note.status == "archived"
    assert CardModel.select().where(CardModel.deck == deck).count() == 2


def test_inline_diff_card_view_mode_propagation_and_actions(qtbot: QtBot) -> None:
    """Couvre la propagation split/unified entre cartes actives, Rejeter et Éditeur."""
    w1 = InlineDiffCardWidget(
        {
            "type": "card",
            "note_id": 42,
            "original": {"Front": "A"},
            "modified": {"Front": "B"},
        }
    )
    w2 = InlineDiffCardWidget(
        {
            "type": "card",
            "note_id": 43,
            "original": {"Front": "C"},
            "modified": {"Front": "D"},
        }
    )
    qtbot.addWidget(w1)
    qtbot.addWidget(w2)

    w1.set_view_mode("split", propagate=True)
    assert w1.current_view_mode == "split"
    assert w2.current_view_mode == "split"

    w1.set_view_mode("unified", propagate=True)
    assert w2.current_view_mode == "unified"

    rejected: list[str] = []
    opened: list[int] = []
    w1.rejected.connect(rejected.append)
    w1.open_editor_requested.connect(opened.append)

    w1.btn_open_editor.click()
    w1.btn_reject.click()

    assert opened == [42]
    assert len(rejected) == 1
    assert not w1.btn_apply.isEnabled()
