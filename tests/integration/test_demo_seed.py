"""Tests d'intégration du constructeur idempotent demo_seed et de l'hydratation BatchView."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from ankidraft.database.models import (
    AuditRecordModel,
    CardModel,
    DeckModel,
    DocumentChunkModel,
    DocumentModel,
    MediaModel,
    NoteChunkLinkModel,
    NoteModel,
    NoteTypeModel,
    SettingModel,
    StagedPatchModel,
)
from ankidraft.database.seeds.initial_seed import seed_initial_data
from ankidraft.services.ai.staged_patch_registry import StagedPatchRegistry
from ankidraft.services.audit.leech_service import LeechService
from ankidraft.services.batch.models import BatchTaskStatus
from ankidraft.utils.paths import get_resource_path


@pytest.mark.integration
def test_demo_resources_exist_and_contain_katex_and_sections() -> None:
    """Les ressources embarquées du mini-cours et du schéma existent et respectent la structure attendue."""
    course_path = get_resource_path("src", "ankidraft", "resources", "demo", "intro_course.md")
    diagram_path = get_resource_path("src", "ankidraft", "resources", "demo", "intro_diagram.svg")

    assert course_path.exists(), f"Cours d'exemple manquant : {course_path}"
    assert diagram_path.exists(), f"Schéma d'exemple manquant : {diagram_path}"

    course_text = course_path.read_text(encoding="utf-8")
    assert "## 1." in course_text
    assert "## 2." in course_text
    assert "## 3." in course_text
    assert "$$" in course_text
    assert "intro_diagram.svg" in course_text

    diagram_text = diagram_path.read_text(encoding="utf-8")
    assert "<svg" in diagram_text


@pytest.mark.integration
def test_seed_intro_example_data_is_idempotent_and_complete(mock_db: Any, tmp_path: Path) -> None:
    """Deux exécutions consécutives de seed_intro_example_data ne dupliquent aucune entité."""
    from ankidraft.database.seeds.demo_seed import (
        DEMO_DECK_NAME,
        INTRO_PROFILE_ID,
        SETTING_IS_INTRO_EXAMPLE,
        get_profile_display_name,
        is_intro_example_profile,
        seed_intro_example_data,
    )

    seed_initial_data()
    assert is_intro_example_profile() is False
    assert get_profile_display_name("default") == "default"

    media_dir = tmp_path / "media"
    first_summary = seed_intro_example_data(media_dir=media_dir)
    second_summary = seed_intro_example_data(media_dir=media_dir)

    assert is_intro_example_profile() is True
    assert SettingModel.get(SettingModel.key == SETTING_IS_INTRO_EXAMPLE).value == "true"
    assert get_profile_display_name(INTRO_PROFILE_ID) != INTRO_PROFILE_ID

    assert first_summary["notes"] >= 8
    assert second_summary["notes"] == first_summary["notes"]
    assert DocumentModel.select().count() == 1
    assert DeckModel.select().count() == 2
    assert DeckModel.select().where(DeckModel.name == DEMO_DECK_NAME).count() == 1
    assert NoteModel.select().count() == first_summary["notes"]
    assert MediaModel.select().count() >= 1
    assert StagedPatchModel.select().where(StagedPatchModel.status == "pending").count() == 1

    # Vérifier la non-duplication des types de note Cloze et Maths & KaTeX Minimal
    assert NoteTypeModel.select().where(NoteTypeModel.name == "Texte à trous (Cloze)").count() == 1
    assert NoteTypeModel.select().where(NoteTypeModel.name == "Maths & KaTeX Minimal").count() == 1

    # Vérifier qu'Enonce_Formule sur Maths & KaTeX Minimal reste du LaTeX brut sans délimiteurs '$' imbriqués
    from ankidraft.database.models import NoteVersionModel

    katex_type = NoteTypeModel.get(NoteTypeModel.name == "Maths & KaTeX Minimal")
    katex_notes = list(NoteModel.select().where(NoteModel.note_type == katex_type))
    assert len(katex_notes) == 2
    for kn in katex_notes:
        active_v = kn.versions.where(NoteVersionModel.is_active == True).first()  # noqa: E712
        assert active_v is not None
        fields = json.loads(active_v.content)
        assert "$" not in fields["Enonce_Formule"]

    # Vérifier Smart Coverage : au moins une section couverte et la section 3 non couverte
    doc = DocumentModel.get()
    chunks = list(DocumentChunkModel.select().where(DocumentChunkModel.document == doc))
    assert len(chunks) >= 3
    covered_chunk_ids = {link.chunk_id for link in NoteChunkLinkModel.select()}
    assert len(covered_chunk_ids) >= 1
    sec3_chunks = [c for c in chunks if c.heading_path and "3." in c.heading_path]
    assert sec3_chunks, "La section 3 doit produire au moins un DocumentChunkModel"
    assert all(c.id not in covered_chunk_ids for c in sec3_chunks), "La section 3 doit rester non couverte"

    # Vérifier les 2 cartes sangsues + AuditRecordModel Wozniak
    deck = DeckModel.get(DeckModel.name == DEMO_DECK_NAME)
    leeches = LeechService.get_leech_cards(deck_id=deck.id, include_high_lapses=False)
    assert len(leeches) == 2
    audits = list(AuditRecordModel.select().where(AuditRecordModel.is_compliant == False))  # noqa: E712
    assert len(audits) == 2
    for audit in audits:
        parsed_sug = json.loads(audit.suggestion or "{}")
        assert {"NoteType", "Recto", "Verso"}.issubset(parsed_sug.keys())

    # Vérifier que le StagedPatchModel en attente est valide, préserve la provenance et est applicable
    patch = StagedPatchModel.get(StagedPatchModel.status == "pending")
    assert patch.patch_type == "note_update"
    payload = json.loads(patch.diff_payload)
    assert isinstance(payload.get("original"), dict)
    assert isinstance(payload.get("modified"), dict)
    assert any(t.startswith("source:") for t in payload.get("modified_tags", []))
    assert any(t.startswith("section:") for t in payload.get("modified_tags", []))
    apply_res = StagedPatchRegistry.apply_staged_patch(patch.patch_id)
    assert apply_res.get("status") == "applied"
    patched_note = NoteModel.get_by_id(patch.target_id)
    assert "source:" in (patched_note.tags or "") and "katex" in (patched_note.tags or "")


@pytest.mark.integration
def test_reset_intro_example_data_restores_clean_state(mock_db: Any, tmp_path: Path) -> None:
    """reset_intro_example_data purge proprement et ré-amorce l'état initial."""
    from ankidraft.database.seeds.demo_seed import (
        SETTING_DEMO_BATCH_REVIEWED,
        reset_intro_example_data,
        seed_intro_example_data,
    )

    seed_initial_data()
    media_dir = tmp_path / "media"
    initial = seed_intro_example_data(media_dir=media_dir)

    SettingModel.set_value(SETTING_DEMO_BATCH_REVIEWED, "true")
    SettingModel.set_value("app/tour_progress_json", '{"core": true}')
    patch = StagedPatchModel.get(StagedPatchModel.status == "pending")
    StagedPatchRegistry.apply_staged_patch(patch.patch_id)
    assert StagedPatchModel.select().where(StagedPatchModel.status == "pending").count() == 0

    reset_summary = reset_intro_example_data(media_dir=media_dir)

    assert reset_summary["notes"] == initial["notes"]
    assert NoteModel.select().count() == initial["notes"]
    assert DocumentModel.select().count() == 1
    assert StagedPatchModel.select().where(StagedPatchModel.status == "pending").count() == 1
    assert SettingModel.get_or_none(SettingModel.key == SETTING_DEMO_BATCH_REVIEWED) is None
    assert SettingModel.get_or_none(SettingModel.key == "app/tour_progress_json") is None
    assert CardModel.select().count() >= initial["notes"]


@pytest.mark.ui
def test_batch_view_hydrates_demo_review_task_once(
    qtbot: Any,
    mock_db: Any,
    tmp_path: Path,
    cleanup_qt_widgets: Any,
) -> None:
    """BatchView hydrate une tâche À réviser dans intro-example puis respecte demo_batch_reviewed."""
    from ankidraft.database.seeds.demo_seed import (
        SETTING_DEMO_BATCH_REVIEWED,
        build_demo_batch_snapshot,
        seed_intro_example_data,
    )
    from ankidraft.ui.views.batch_view.view import BatchView

    seed_initial_data()
    seed_intro_example_data(media_dir=tmp_path / "media")

    snapshot = build_demo_batch_snapshot()
    assert snapshot is not None
    assert snapshot.status == BatchTaskStatus.REVIEW
    assert len(snapshot.cards) >= 2

    view = BatchView()
    qtbot.addWidget(view)

    assert len(view.queue_tasks_data) == 1
    assert view.card_cards.val_lbl.text() == "1 à valider"
    row = view.queue_tasks_data[0]
    assert row["status"] == "À réviser"
    uid = row["_queue_uid"]
    assert len(view._prepared_notes_by_uid[uid]) >= 2

    # Valider la tâche de démonstration marque demo_batch_reviewed
    view._on_staging_accepted(uid, view._prepared_notes_by_uid[uid])
    reviewed_setting = SettingModel.get_or_none(SettingModel.key == SETTING_DEMO_BATCH_REVIEWED)
    assert reviewed_setting is not None and reviewed_setting.value == "true"

    # Une ré-ouverture de BatchView ne ré-injecte pas la tâche déjà tranchée
    view_reopened = BatchView()
    qtbot.addWidget(view_reopened)
    assert len(view_reopened.queue_tasks_data) == 0


@pytest.mark.ui
def test_batch_view_does_not_hydrate_on_regular_profile_and_reject_marks_reviewed(
    qtbot: Any,
    mock_db: Any,
    tmp_path: Path,
    cleanup_qt_widgets: Any,
) -> None:
    """Un profil ordinaire n'hydrate aucune tâche démo, et le rejet marque aussi la revue."""
    from ankidraft.database.seeds.demo_seed import (
        SETTING_DEMO_BATCH_REVIEWED,
        build_demo_batch_snapshot,
        seed_intro_example_data,
    )
    from ankidraft.ui.views.batch_view.view import BatchView

    seed_initial_data()
    assert build_demo_batch_snapshot() is None

    regular_view = BatchView()
    qtbot.addWidget(regular_view)
    assert len(regular_view.queue_tasks_data) == 0

    seed_intro_example_data(media_dir=tmp_path / "media")
    demo_view = BatchView()
    qtbot.addWidget(demo_view)
    assert len(demo_view.queue_tasks_data) == 1
    uid = demo_view.queue_tasks_data[0]["_queue_uid"]
    demo_view._on_staging_rejected(uid)
    reviewed_setting = SettingModel.get_or_none(SettingModel.key == SETTING_DEMO_BATCH_REVIEWED)
    assert reviewed_setting is not None and reviewed_setting.value == "true"
