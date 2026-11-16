"""Tests headless du moteur de tutoriel interactif et des signaux réactifs EventBus."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import QRect
from PySide6.QtWidgets import QLabel, QWidget

import ankidraft.ui.widgets.tour_guide as tour_guide_mod
from ankidraft.database.models import (
    AuditRecordModel,
    DeckModel,
    NoteModel,
    NoteTypeModel,
    NoteVersionModel,
    SettingModel,
    StagedBundleModel,
    StagedPatchModel,
)
from ankidraft.services.ai.staged_patch_registry import StagedPatchRegistry
from ankidraft.ui.dialogs.export_dialog import ExportDialog
from ankidraft.ui.views.analysis_view.tabs.wozniak_tab import AIWozniakLinterTab
from ankidraft.ui.views.batch_view.view import BatchView
from ankidraft.ui.views.edition_view.view import EditionView
from ankidraft.ui.widgets.tour_guide import (
    InteractiveTourController,
    InteractiveTourStep,
    TourBubble,
    TourCompanionCard,
    TourStep,
)
from ankidraft.utils.event_bus import (
    AppEventBus,
    BatchTaskReviewedEvent,
    CardPreviewToggledEvent,
    MCPPatchRejectedEvent,
    PackageExportedEvent,
    ViewNavigatedEvent,
    WozniakAuditResolvedEvent,
)

pytestmark = pytest.mark.ui


@pytest.fixture
def isolated_bus() -> AppEventBus:
    """Fournit un bus d'événements neuf sans fuiter vers le singleton global."""
    return AppEventBus()


def test_tour_bubble_creation(qtbot: Any) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)

    bubble = TourBubble(parent)
    qtbot.addWidget(bubble)
    assert bubble is not None
    assert bubble.current_step == 0


def test_tour_bubble_navigation(qtbot: Any) -> None:
    parent = QWidget()
    target_label = QLabel("Cible", parent)
    qtbot.addWidget(parent)

    action_executed = False

    def on_step_action() -> None:
        nonlocal action_executed
        action_executed = True

    steps = [
        TourStep(title="Étape 1", text="Bienvenue", target_widget=None),
        TourStep(title="Étape 2", text="Inspection", target_widget=target_label, action=on_step_action),
    ]

    bubble = TourBubble(parent)
    qtbot.addWidget(bubble)
    bubble.set_scenario(steps)

    bubble.start_tour()
    assert bubble.isVisible()
    assert bubble.lbl_title.text() == "Étape 1"
    assert bubble.lbl_counter.text() == "1/2"
    assert not bubble.btn_prev.isVisible()

    bubble.next_step()
    assert bubble.current_step == 1
    assert bubble.lbl_title.text() == "Étape 2"
    assert bubble.lbl_counter.text() == "2/2"
    assert bubble.btn_prev.isVisible()
    assert action_executed is True

    bubble.prev_step()
    assert bubble.current_step == 0
    assert bubble.lbl_title.text() == "Étape 1"

    bubble.next_step()
    bubble.next_step()
    assert bubble.isHidden()


def test_tour_dict_scenario_compatibility(qtbot: Any) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)

    dict_steps = [
        {"title": "Step Dict 1", "text": "Contenu 1"},
        {"title": "Step Dict 2", "text": "Contenu 2"},
    ]

    bubble = TourBubble(parent)
    qtbot.addWidget(bubble)
    bubble.set_scenario(dict_steps)
    bubble.start_tour()

    assert len(bubble.steps) == 2
    assert bubble.steps[0].title == "Step Dict 1"
    bubble.end_tour()
    assert bubble.isHidden()


def test_default_static_tour_removed_and_no_emojis_or_hex_colors() -> None:
    assert not hasattr(tour_guide_mod, "create_default_tour_steps")
    source = Path(tour_guide_mod.__file__).read_text(encoding="utf-8")
    emoji_pattern = re.compile(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]")
    assert not emoji_pattern.search(source), "Aucun emoji textuel ne doit rester dans tour_guide.py"
    hex_pattern = re.compile(r"#[0-9a-fA-F]{3,8}\b")
    assert not hex_pattern.search(source), "Aucune couleur hexadécimale codée en dur dans tour_guide.py"


def test_new_event_bus_dataclasses_and_aliases() -> None:
    bus = AppEventBus()
    received: list[Any] = []

    bus.subscribe("view_navigated", lambda ev: received.append(ev))
    bus.subscribe("wozniak_audit_resolved", lambda ev: received.append(ev))
    bus.subscribe("mcp_patch_rejected", lambda ev: received.append(ev))
    bus.subscribe("batch_task_reviewed", lambda ev: received.append(ev))
    bus.subscribe("card_preview_toggled", lambda ev: received.append(ev))
    bus.subscribe("package_exported", lambda ev: received.append(ev))

    events = [
        ViewNavigatedEvent(view_id="edition"),
        WozniakAuditResolvedEvent(note_id=10, resolution="applied"),
        MCPPatchRejectedEvent(patch_id="patch-1"),
        BatchTaskReviewedEvent(task_uid="task-1", decision="accepted"),
        CardPreviewToggledEvent(visible=True),
        PackageExportedEvent(output_path="/tmp/out.apkg", card_count=4),
    ]
    for ev in events:
        bus.publish(ev)

    assert len(received) == 6


def test_view_navigated_event_emitted_from_main_window(qtbot: Any, mock_db: Any) -> None:
    from ankidraft.ui.main_window import MainWindow
    from ankidraft.utils.event_bus import event_bus

    captured: list[ViewNavigatedEvent] = []
    event_bus.subscribe(ViewNavigatedEvent, captured.append)
    try:
        with (
            patch("ankidraft.ui.main_window.AIManager"),
            patch("ankidraft.ui.main_window.MainWindow._init_mcp_daemon"),
        ):
            window = MainWindow(ai_manager=None, profile_name="test_tour_nav")
        qtbot.addWidget(window)
        window._on_view_selected("edition")
        assert any(ev.view_id == "edition" for ev in captured)
    finally:
        event_bus.unsubscribe(ViewNavigatedEvent, captured.append)


def test_wozniak_audit_resolved_events_emitted(qtbot: Any, mock_db: Any) -> None:
    from ankidraft.utils.event_bus import event_bus

    nt = NoteTypeModel.create(name="Basique", fields_schema='["Recto", "Verso"]')
    note1 = NoteModel.create(guid="g-woz-1", note_type=nt)
    NoteVersionModel.create(note=note1, content=json.dumps({"Recto": "Q1", "Verso": "R1"}), is_active=True)
    note2 = NoteModel.create(guid="g-woz-2", note_type=nt)
    NoteVersionModel.create(note=note2, content=json.dumps({"Recto": "Q2", "Verso": "R2"}), is_active=True)

    tab = AIWozniakLinterTab()
    qtbot.addWidget(tab)

    captured: list[WozniakAuditResolvedEvent] = []
    event_bus.subscribe(WozniakAuditResolvedEvent, captured.append)
    try:
        w1 = QWidget()
        w2 = QWidget()
        qtbot.addWidget(w1)
        qtbot.addWidget(w2)
        with patch("ankidraft.ui.views.analysis_view.tabs.wozniak_tab.show_toast"):
            tab._on_card_applied(note1.id, {"Recto": "Q1 atomique", "Verso": "R1"}, w1)
            tab._on_card_ignored(note2.id, w2)

        assert (note1.id, "applied") in [(e.note_id, e.resolution) for e in captured]
        assert (note2.id, "ignored") in [(e.note_id, e.resolution) for e in captured]
        assert AuditRecordModel.select().where(AuditRecordModel.note == note1).exists()
    finally:
        event_bus.unsubscribe(WozniakAuditResolvedEvent, captured.append)


def test_mcp_patch_rejected_event_emitted(mock_db: Any) -> None:
    from ankidraft.utils.event_bus import event_bus

    bundle = StagedBundleModel.create(bundle_id="b-tour-1", title="Bundle tour")
    StagedPatchModel.create(
        patch_id="p-tour-reject",
        bundle=bundle,
        patch_type="note_refactor",
        target_id=1,
        diff_payload=json.dumps({"before": {}, "after": {}}),
        status="pending",
    )

    captured: list[MCPPatchRejectedEvent] = []
    event_bus.subscribe(MCPPatchRejectedEvent, captured.append)
    try:
        res = StagedPatchRegistry.reject_staged_patch("p-tour-reject", reason="Refus utilisateur")
        assert res["status"] == "rejected"
        assert [e.patch_id for e in captured] == ["p-tour-reject"]
    finally:
        event_bus.unsubscribe(MCPPatchRejectedEvent, captured.append)


def test_batch_task_reviewed_events_emitted(qtbot: Any, mock_db: Any) -> None:
    from ankidraft.utils.event_bus import event_bus

    view = BatchView(ai_manager=None)
    qtbot.addWidget(view)
    view.queue_tasks_data = [
        {"_queue_uid": "u-acc", "status": "À réviser", "cards_count": 1, "pending_cards": []},
        {"_queue_uid": "u-rej", "status": "À réviser", "cards_count": 1, "pending_cards": []},
    ]
    view.queue_widget.set_tasks(view.queue_tasks_data)

    captured: list[BatchTaskReviewedEvent] = []
    event_bus.subscribe(BatchTaskReviewedEvent, captured.append)
    try:
        view._on_staging_accepted("u-acc", [{"Recto": "Q", "Verso": "R"}])
        view._on_staging_rejected("u-rej")
        assert [(e.task_uid, e.decision) for e in captured] == [
            ("u-acc", "accepted"),
            ("u-rej", "rejected"),
        ]
    finally:
        event_bus.unsubscribe(BatchTaskReviewedEvent, captured.append)


def test_card_preview_toggled_event_emitted(qtbot: Any, mock_db: Any) -> None:
    from ankidraft.utils.event_bus import event_bus

    view = EditionView(ai_manager=None)
    qtbot.addWidget(view)

    captured: list[CardPreviewToggledEvent] = []
    event_bus.subscribe(CardPreviewToggledEvent, captured.append)
    try:
        initial = view._preview_visible
        view._toggle_preview_pane()
        assert len(captured) == 1
        assert captured[0].visible is (not initial)
    finally:
        event_bus.unsubscribe(CardPreviewToggledEvent, captured.append)


@patch("ankidraft.ui.dialogs.export_dialog.QMessageBox.information")
@patch("ankidraft.ui.dialogs.export_dialog.show_toast")
def test_package_exported_event_and_setting_emitted(
    mock_toast: MagicMock,
    mock_info: MagicMock,
    qtbot: Any,
    mock_db: Any,
    tmp_path: Path,
) -> None:
    from ankidraft.utils.event_bus import event_bus

    DeckModel.create(name="ExportTest")
    dialog = ExportDialog()
    qtbot.addWidget(dialog)

    out_path = str(tmp_path / "demo.apkg")
    dialog.dest_input.setText(out_path)
    dialog.export_manager = MagicMock()
    dialog.export_manager.export_package.return_value = 7

    captured: list[PackageExportedEvent] = []
    event_bus.subscribe(PackageExportedEvent, captured.append)
    try:
        dialog._start_export()
        assert len(captured) == 1
        assert captured[0].output_path == out_path
        assert captured[0].card_count == 7
        setting = SettingModel.get_or_none(SettingModel.key == "telemetry/first_apkg_exported")
        assert setting is not None
        assert setting.value == "true"
    finally:
        event_bus.unsubscribe(PackageExportedEvent, captured.append)


def test_interactive_tour_controller_reactive_lifecycle_and_controls(
    qtbot: Any,
    isolated_bus: AppEventBus,
) -> None:
    host = QWidget()
    host.resize(1024, 720)
    host.show()
    qtbot.addWidget(host)
    navigated_views: list[str] = []
    host._current_view_id = "dashboard"  # type: ignore[attr-defined]

    def fake_nav(view_id: str) -> None:
        navigated_views.append(view_id)
        host._current_view_id = view_id  # type: ignore[attr-defined]
        isolated_bus.publish(ViewNavigatedEvent(view_id=view_id))

    host._on_view_selected = fake_nav  # type: ignore[attr-defined]

    entered_steps: list[str] = []
    steps = [
        InteractiveTourStep(
            step_id="step-nav",
            title_factory=lambda: "Naviguer vers l'éditeur",
            text_factory=lambda: "Cliquez sur Édition.",
            target_view_id="dashboard",
            on_enter=lambda: entered_steps.append("step-nav"),
            completion_event=ViewNavigatedEvent,
            completion_predicate=lambda ev: isinstance(ev, ViewNavigatedEvent) and ev.view_id == "edition",
        ),
        InteractiveTourStep(
            step_id="step-preview",
            title_factory=lambda: "Basculer l'aperçu",
            text_factory=lambda: "Affichez le volet d'aperçu.",
            target_view_id="edition",
            on_enter=lambda: entered_steps.append("step-preview"),
            completion_event=CardPreviewToggledEvent,
            completion_predicate=lambda ev: isinstance(ev, CardPreviewToggledEvent) and ev.visible is True,
        ),
        InteractiveTourStep(
            step_id="step-final",
            title_factory=lambda: "Exporter le paquet",
            text_factory=lambda: "Exportez un paquet .apkg.",
            target_view_id=None,
            on_enter=lambda: entered_steps.append("step-final"),
            completion_event=PackageExportedEvent,
        ),
    ]

    controller = InteractiveTourController(host, event_bus_instance=isolated_bus)
    completed_steps: list[str] = []
    finished_tracks: list[str] = []
    cancelled_tracks: list[str] = []
    controller.step_completed.connect(completed_steps.append)
    controller.tour_finished.connect(finished_tracks.append)
    controller.tour_cancelled.connect(cancelled_tracks.append)

    controller.start(steps, track_id="discover")
    card = controller.companion_card
    assert isinstance(card, TourCompanionCard)
    assert card.parent() is host
    assert card.isVisible()
    assert card.lbl_title.text() == "Naviguer vers l'éditeur"
    assert entered_steps == ["step-nav"]

    # Ancrage bas-droite dans la géométrie hôte
    card_geom: QRect = card.geometry()
    assert card_geom.right() <= host.width()
    assert card_geom.bottom() <= host.height()

    # Un événement qui ne valide pas le prédicat laisse l'étape en attente
    isolated_bus.publish(ViewNavigatedEvent(view_id="analysis"))
    assert controller.current_index == 0
    assert completed_steps == []

    # L'événement attendu valide l'étape et passe à l'étape suivante (en naviguant vers target_view_id)
    isolated_bus.publish(ViewNavigatedEvent(view_id="edition"))
    assert completed_steps == ["step-nav"]
    assert controller.current_index == 1
    assert card.lbl_title.text() == "Basculer l'aperçu"

    # Contrôles manuels : Précédent puis Passer l'étape
    card.btn_prev.click()
    assert controller.current_index == 0
    card.btn_skip.click()
    assert controller.current_index == 1
    assert isolated_bus.listener_count(CardPreviewToggledEvent) == 1

    # Passage vers la dernière étape puis accomplissement final + Terminer
    isolated_bus.publish(CardPreviewToggledEvent(visible=True))
    assert controller.current_index == 2
    isolated_bus.publish(PackageExportedEvent(output_path="out.apkg", card_count=3))
    assert "step-final" in completed_steps
    assert finished_tracks == []
    card.btn_next.click()
    assert finished_tracks == ["discover"]
    assert card.isHidden()
    assert isolated_bus.listener_count(PackageExportedEvent) == 0

    # Annulation propre via Quitter et désinstallation du filtre d'événements
    controller.start(steps, track_id="discover")
    assert isolated_bus.listener_count(ViewNavigatedEvent) == 1
    assert controller._host_filter_installed is True
    controller.companion_card.btn_quit.click()
    assert cancelled_tracks == ["discover"]
    assert isolated_bus.listener_count(ViewNavigatedEvent) == 0
    assert controller._host_filter_installed is False


def test_companion_card_refresh_theme_fallback_with_builtin_profile(qtbot: Any) -> None:
    from ankidraft.ui.style_engine.themes import JETBRAINS_DARK

    host = QWidget()
    qtbot.addWidget(host)
    card = TourCompanionCard(host)
    qtbot.addWidget(card)
    card.refresh_theme(JETBRAINS_DARK)

    badge_sheet = card.status_badge.styleSheet()
    assert "background-color: ;" not in badge_sheet
    assert "border: 1px solid ;" not in badge_sheet
    assert "color: ;" not in card.lbl_status.styleSheet()


def test_main_window_start_tour_guide_uses_interactive_controller(qtbot: Any, mock_db: Any) -> None:
    from ankidraft.ui.main_window import MainWindow
    from ankidraft.utils.event_bus import event_bus

    with (
        patch("ankidraft.ui.main_window.AIManager"),
        patch("ankidraft.ui.main_window.MainWindow._init_mcp_daemon"),
        patch("ankidraft.ui.views.dashboard_view.StatsWorker.start"),
    ):
        window = MainWindow(ai_manager=None, profile_name="test_tour_ctrl")
    qtbot.addWidget(window)
    window.show()
    window.start_tour_guide()

    assert hasattr(window, "_tour_controller")
    assert window._tour_controller is not None
    assert window._tour_controller.companion_card is not None
    assert window._tour_controller.companion_card.isVisible()

    # Une vue inexistante ne doit pas émettre ViewNavigatedEvent
    captured: list[ViewNavigatedEvent] = []
    event_bus.subscribe(ViewNavigatedEvent, captured.append)
    try:
        window._on_view_selected("nonexistent_view_xyz")
        assert captured == []
    finally:
        event_bus.unsubscribe(ViewNavigatedEvent, captured.append)

    window._tour_controller.quit_tour()
