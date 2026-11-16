"""Tests bout-en-bout headless du Hub du Tutoriel Dashboard et des parcours interactifs."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from ankidraft.database.models import SettingModel, seed_initial_data
from ankidraft.database.seeds.demo_seed import (
    INTRO_PROFILE_ID,
    SETTING_TOUR_PROGRESS,
    reset_intro_example_data,
    seed_intro_example_data,
)
from ankidraft.services.profile_lock_service import ProfileLockService
from ankidraft.services.profile_manager import ProfileManager
from ankidraft.ui.main_window import MainWindow
from ankidraft.ui.views.dashboard_view import DashboardView
from ankidraft.ui.widgets.tour_guide import (
    TOUR_TRACK_CORE,
    TOUR_TRACK_IDS,
    TourHubWidget,
    build_tour_track_steps,
    load_tour_progress,
    save_tour_track_status,
)
from ankidraft.utils.event_bus import (
    BatchTaskReviewedEvent,
    CardPreviewToggledEvent,
    MCPDataMutatedEvent,
    MCPPatchRejectedEvent,
    PackageExportedEvent,
    ViewNavigatedEvent,
    WozniakAuditResolvedEvent,
    event_bus,
)

pytestmark = pytest.mark.ui


@pytest.fixture
def isolated_profiles_dir(tmp_path: Path) -> Any:
    """Isole ProfileManager et ProfileLockService dans tmp_path et libère les verrous."""
    with patch("ankidraft.services.profile_manager.ProfileManager.PROFILES_DIR", tmp_path):
        yield tmp_path
    for prof_name in list(ProfileLockService._active_locks.keys()):
        ProfileLockService.release_lock(prof_name)


def test_dashboard_displays_tour_hub_on_intro_example_and_checklist_on_real_profile(
    qtbot: Any,
    mock_db: Any,
    tmp_path: Path,
    cleanup_qt_widgets: Any,
) -> None:
    """TourHubWidget remplace OnboardingChecklistWidget uniquement sur le profil Exemple d'introduction."""
    seed_initial_data()
    real_dash = DashboardView(ai_manager=MagicMock(), profile_name="default")
    qtbot.addWidget(real_dash)

    assert real_dash.onboarding_checklist.isVisibleTo(real_dash)
    assert not real_dash.tour_hub.isVisibleTo(real_dash)
    if real_dash.worker and real_dash.worker.isRunning():
        real_dash.worker.wait()

    seed_intro_example_data(media_dir=tmp_path / "media")
    intro_dash = DashboardView(ai_manager=MagicMock(), profile_name=INTRO_PROFILE_ID)
    qtbot.addWidget(intro_dash)

    assert isinstance(intro_dash.tour_hub, TourHubWidget)
    assert intro_dash.tour_hub.isVisibleTo(intro_dash)
    assert not intro_dash.onboarding_checklist.isVisibleTo(intro_dash)
    assert set(intro_dash.tour_hub.track_cards.keys()) == set(TOUR_TRACK_IDS)
    if intro_dash.worker and intro_dash.worker.isRunning():
        intro_dash.worker.wait()


def test_tour_track_definitions_views_and_zero_emojis() -> None:
    """Tous les scénarios utilisent des view_id valides, des icônes Phosphor et zéro emoji."""
    valid_views = set(MainWindow.view_registry().keys())
    emoji_pattern = re.compile(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]")

    core_steps = build_tour_track_steps(TOUR_TRACK_CORE)
    assert 4 <= len(core_steps) <= 5
    mcp_steps = [s for s in core_steps if s.target_view_id == "consultant"]
    assert len(mcp_steps) == 1
    assert mcp_steps[0].completion_event == (MCPDataMutatedEvent, MCPPatchRejectedEvent)

    for track_id in TOUR_TRACK_IDS:
        steps = build_tour_track_steps(track_id)
        assert steps
        for step in steps:
            if step.target_view_id is not None:
                assert step.target_view_id in valid_views, f"view_id invalide: {step.target_view_id}"
            assert not emoji_pattern.search(step.title_factory())
            assert not emoji_pattern.search(step.text_factory())


def test_intro_tour_e2e_core_module_progression_persistence_and_reset(
    qtbot: Any,
    mock_db: Any,
    isolated_profiles_dir: Path,
    tmp_path: Path,
    cleanup_qt_widgets: Any,
) -> None:
    """Parcours E2E : auto-lancement, progression réactive Tronc commun + Batch, persistance et reset."""
    pm = ProfileManager()
    pm.create_profile(INTRO_PROFILE_ID)
    seed_initial_data()
    seed_intro_example_data(media_dir=tmp_path / "media")
    ProfileLockService.acquire_lock(INTRO_PROFILE_ID)

    with (
        patch("ankidraft.ui.main_window.AIManager"),
        patch("ankidraft.ui.main_window.MainWindow._init_mcp_daemon"),
        patch("ankidraft.ui.views.dashboard_view.StatsWorker.start"),
    ):
        window = MainWindow(ai_manager=None, profile_name=INTRO_PROFILE_ID)
    qtbot.addWidget(window)
    window.show()

    # 1. Chargement du Dashboard -> TourHub visible en statut 'À faire'
    window._on_view_selected("dashboard")
    dashboard = window._view_widgets["dashboard"]
    assert isinstance(dashboard, DashboardView)
    assert dashboard.tour_hub.status_for_track("core") == "todo"

    # 2. Premier lancement automatique du Tronc commun
    assert window.maybe_auto_start_intro_tour() is True
    assert window._tour_controller is not None
    assert window._tour_controller.companion_card is not None
    assert window._tour_controller.companion_card.isVisible()
    assert load_tour_progress().get("core") == "in_progress"
    assert dashboard.tour_hub.status_for_track("core") == "in_progress"

    # 3. Étape 1 -> 2 : navigation vers Analyse & Audit IA
    assert window._current_view_id == "documents"
    window._on_view_selected("analysis")
    assert window._tour_controller.current_index == 1

    # 4. Étape 2 -> 3 : résolution Wozniak
    event_bus.publish(WozniakAuditResolvedEvent(note_id=1, resolution="applied"))
    assert window._tour_controller.current_index == 2
    assert window._current_view_id == "consultant"

    # 5. Étape 3 -> 4 : décision Garde-Fou MCP (rejet accepté comme validation)
    event_bus.publish(MCPPatchRejectedEvent(patch_id="patch-demo"))
    assert window._tour_controller.current_index == 3
    assert window._current_view_id == "edition"

    # 6. Étape 4 -> 5 : bascule aperçu carte puis export .apkg + Terminer
    event_bus.publish(CardPreviewToggledEvent(visible=True))
    assert window._tour_controller.current_index == 4
    event_bus.publish(PackageExportedEvent(output_path=str(tmp_path / "demo.apkg"), card_count=4))
    window._tour_controller.companion_card.btn_next.click()

    assert load_tour_progress().get("core") == "done"
    assert dashboard.tour_hub.status_for_track("core") == "done"
    # Ne relance plus automatiquement une fois le tronc commun terminé
    assert window.maybe_auto_start_intro_tour() is False

    # 7. Lancement du module complémentaire 'batch' depuis le Hub Dashboard
    dashboard.tour_hub.launch_track("batch")
    assert load_tour_progress().get("batch") == "in_progress"
    event_bus.publish(ViewNavigatedEvent(view_id="batch"))
    assert window._tour_controller.current_index == 1
    event_bus.publish(BatchTaskReviewedEvent(task_uid="demo-intro-batch-review-1", decision="accepted"))
    window._tour_controller.companion_card.btn_next.click()

    progress = SettingModel.get_value(SETTING_TOUR_PROGRESS, {})
    assert isinstance(progress, dict)
    assert progress["core"] == "done"
    assert progress["batch"] == "done"
    assert dashboard.tour_hub.status_for_track("batch") == "done"

    # 8. Réinitialisation de l'exemple d'introduction : purge app/tour_progress_json et remet le Hub à 'À faire'
    with patch("ankidraft.database.seeds.demo_seed.MediaManager") as mock_media_cls:
        mock_media_cls.return_value = mock_media_cls.return_value
        mock_media_cls.return_value.store_media_bytes.return_value = MagicMock(filename="intro_diagram.svg")
        mock_media_cls.return_value.clean_orphaned_media.return_value = 0
        dashboard._on_reset_intro_example()
        if dashboard.worker and dashboard.worker.isRunning():
            dashboard.worker.wait()

        assert SettingModel.get_or_none(SettingModel.key == SETTING_TOUR_PROGRESS) is None
        assert load_tour_progress() == {}
        assert dashboard.tour_hub.status_for_track("core") == "todo"
        assert dashboard.tour_hub.status_for_track("batch") == "todo"

        save_tour_track_status("ai_lab", "in_progress")
        assert load_tour_progress()["ai_lab"] == "in_progress"
        reset_intro_example_data(media_dir=tmp_path / "media")
        assert load_tour_progress() == {}


def test_optional_modules_ai_lab_templates_and_batch_demo_not_dirty(
    qtbot: Any,
    mock_db: Any,
    tmp_path: Path,
    cleanup_qt_widgets: Any,
) -> None:
    """Vérifie ai_lab, templates, start_tour_guide() par défaut et BatchView.is_dirty() hors démo."""
    from ankidraft.ui.views.batch_view import BatchView

    seed_initial_data()
    seed_intro_example_data(media_dir=tmp_path / "media")

    batch = BatchView()
    qtbot.addWidget(batch)
    batch._hydrate_demo_batch_task()
    assert len(batch.queue_tasks_data) == 1
    assert batch.is_dirty() is False

    batch.batch_view_model.add_tasks([{"_queue_uid": "user-task-1", "status": "En attente"}])
    assert batch.is_dirty() is True

    with (
        patch("ankidraft.ui.main_window.AIManager"),
        patch("ankidraft.ui.main_window.MainWindow._init_mcp_daemon"),
        patch("ankidraft.ui.views.dashboard_view.StatsWorker.start"),
    ):
        window = MainWindow(ai_manager=None, profile_name=INTRO_PROFILE_ID)
    qtbot.addWidget(window)

    # Module ai_lab (Agents -> Pipelines -> Tests A/B)
    window.start_tour_guide("ai_lab")
    assert window._tour_controller is not None
    assert window._current_view_id == "agents"
    event_bus.publish(ViewNavigatedEvent(view_id="pipelines"))
    assert window._tour_controller.current_index == 1
    event_bus.publish(ViewNavigatedEvent(view_id="ab-tests"))
    assert window._tour_controller.current_index == 2
    assert window._tour_controller.companion_card is not None
    window._tour_controller.companion_card.btn_next.click()
    assert load_tour_progress()["ai_lab"] == "done"

    # Module templates (Types de note -> Édition -> Aperçu)
    window.start_tour_guide("templates")
    assert window._current_view_id == "card-models"
    event_bus.publish(ViewNavigatedEvent(view_id="edition"))
    assert window._tour_controller.current_index == 1
    event_bus.publish(CardPreviewToggledEvent(visible=True))
    window._tour_controller.companion_card.btn_next.click()
    assert load_tour_progress()["templates"] == "done"

    # Sans module_id : lance le Tronc commun tant qu'il n'est pas terminé
    window.start_tour_guide()
    assert window._current_view_id == "documents"
    window._tour_controller.quit_tour()

    # Une fois le Tronc commun terminé, start_tour_guide() sans module ouvre le Hub Dashboard
    save_tour_track_status("core", "done")
    window.start_tour_guide()
    assert window._current_view_id == "dashboard"
    if isinstance(window._view_widgets.get("dashboard"), DashboardView):
        dash = window._view_widgets["dashboard"]
        if dash.worker and dash.worker.isRunning():
            dash.worker.wait()
