"""Tests d'interface pour l'écran d'accueil initial et le cycle de vie du profil Exemple d'introduction."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import Qt

from ankidraft.database.models import NoteModel, SettingModel, StagedPatchModel
from ankidraft.database.seeds.demo_seed import INTRO_PROFILE_ID, seed_intro_example_data
from ankidraft.database.seeds.initial_seed import seed_initial_data
from ankidraft.services.profile_lock_service import ProfileLockService
from ankidraft.services.profile_manager import ProfileManager
from ankidraft.ui.widgets.profile_selector import ProfileItemWidget, ProfileSelectorDialog


@pytest.fixture
def isolated_profiles_dir(tmp_path: Path) -> Any:
    """Isole ProfileManager et ProfileLockService dans tmp_path et libère les verrous."""
    with patch("ankidraft.services.profile_manager.ProfileManager.PROFILES_DIR", tmp_path):
        yield tmp_path
    for prof_name in list(ProfileLockService._active_locks.keys()):
        ProfileLockService.release_lock(prof_name)


@pytest.mark.ui
def test_first_launch_welcome_dialog_offers_three_explicit_choices(
    qtbot: Any,
    cleanup_qt_widgets: Any,
) -> None:
    """FirstLaunchWelcomeDialog expose les 3 portes d'entrée et retourne choix + nom de profil."""
    from ankidraft.ui.dialogs.first_launch_welcome_dialog import FirstLaunchWelcomeDialog

    # Choix 1 : Explorer avec l'Exemple d'introduction (recommandé)
    dlg_explore = FirstLaunchWelcomeDialog()
    qtbot.addWidget(dlg_explore)
    assert "Exemple d'introduction" in dlg_explore.btn_explore.text()
    assert "passe la présentation" in dlg_explore.btn_import.toolTip().lower() or "passe" in dlg_explore.import_hint_lbl.text().lower()
    assert "passe la présentation" in dlg_explore.btn_blank.toolTip().lower() or "passe" in dlg_explore.blank_hint_lbl.text().lower()

    dlg_explore.btn_explore.click()
    assert dlg_explore.result() == dlg_explore.DialogCode.Accepted
    choice, profile_name = dlg_explore.get_selection()
    assert choice == FirstLaunchWelcomeDialog.CHOICE_EXPLORE
    assert profile_name == INTRO_PROFILE_ID

    # Choix 2 : Importer ma collection Anki avec nom personnalisé
    dlg_import = FirstLaunchWelcomeDialog()
    qtbot.addWidget(dlg_import)
    dlg_import.profile_name_input.setText("Médecine 2026")
    dlg_import.btn_import.click()
    assert dlg_import.result() == dlg_import.DialogCode.Accepted
    choice, profile_name = dlg_import.get_selection()
    assert choice == FirstLaunchWelcomeDialog.CHOICE_IMPORT
    assert profile_name == "M_decine_2026"

    # Choix 3 : Espace vierge par défaut
    dlg_blank = FirstLaunchWelcomeDialog()
    qtbot.addWidget(dlg_blank)
    dlg_blank.btn_blank.click()
    assert dlg_blank.result() == dlg_blank.DialogCode.Accepted
    choice, profile_name = dlg_blank.get_selection()
    assert choice == FirstLaunchWelcomeDialog.CHOICE_BLANK
    assert profile_name == "default"


@pytest.mark.ui
def test_resolve_first_launch_action_handles_three_paths(
    qtbot: Any,
    isolated_profiles_dir: Path,
    cleanup_qt_widgets: Any,
) -> None:
    """resolve_first_launch_action crée uniquement le profil choisi et indique l'ouverture import."""
    from ankidraft.__main__ import resolve_first_launch_action
    from ankidraft.ui.dialogs.first_launch_welcome_dialog import FirstLaunchWelcomeDialog

    pm = ProfileManager()

    # Chemin 1 : explore -> crée uniquement intro-example, pas d'import auto
    class _ExploreDlg(FirstLaunchWelcomeDialog):
        def exec(self) -> int:  # type: ignore[override]
            self.choice = self.CHOICE_EXPLORE
            self.selected_profile_name = INTRO_PROFILE_ID
            return int(self.DialogCode.Accepted)

    res = resolve_first_launch_action(pm, dialog_factory=_ExploreDlg)
    assert res == (INTRO_PROFILE_ID, False)
    assert pm.list_profiles() == [INTRO_PROFILE_ID]

    # Chemin 2 : import -> crée le profil personnalisé et demande l'import auto
    class _ImportDlg(FirstLaunchWelcomeDialog):
        def exec(self) -> int:  # type: ignore[override]
            self.choice = self.CHOICE_IMPORT
            self.selected_profile_name = "mon_cours"
            return int(self.DialogCode.Accepted)

    res_import = resolve_first_launch_action(pm, dialog_factory=_ImportDlg)
    assert res_import == ("mon_cours", True)
    assert "mon_cours" in pm.list_profiles()

    # Chemin 3 : blank -> crée l'espace vierge sans import auto
    class _BlankDlg(FirstLaunchWelcomeDialog):
        def exec(self) -> int:  # type: ignore[override]
            self.choice = self.CHOICE_BLANK
            self.selected_profile_name = "espace_vierge"
            return int(self.DialogCode.Accepted)

    res_blank = resolve_first_launch_action(pm, dialog_factory=_BlankDlg)
    assert res_blank == ("espace_vierge", False)
    assert "espace_vierge" in pm.list_profiles()

    # Annulation -> retourne None
    class _CancelDlg(FirstLaunchWelcomeDialog):
        def exec(self) -> int:  # type: ignore[override]
            return int(self.DialogCode.Rejected)

    assert resolve_first_launch_action(pm, dialog_factory=_CancelDlg) is None


@pytest.mark.ui
def test_profile_selector_displays_translated_intro_name_and_filters_on_it(
    qtbot: Any,
    isolated_profiles_dir: Path,
    cleanup_qt_widgets: Any,
) -> None:
    """ProfileSelectorDialog dissocie profile_id et display_name et filtre sur le nom affiché."""
    pm = ProfileManager()
    pm.create_profile(INTRO_PROFILE_ID)
    pm.create_profile("default")

    dialog = ProfileSelectorDialog([INTRO_PROFILE_ID, "default"], current_profile="default")
    qtbot.addWidget(dialog)

    intro_card: ProfileItemWidget | None = None
    for i in range(dialog.list_widget.count()):
        item = dialog.list_widget.item(i)
        if item.data(Qt.ItemDataRole.UserRole) == INTRO_PROFILE_ID:
            card = dialog.list_widget.itemWidget(item)
            assert isinstance(card, ProfileItemWidget)
            intro_card = card
            assert card.name == INTRO_PROFILE_ID
            assert card.name_lbl.text() == "Exemple d'introduction"

    assert intro_card is not None

    # Filtrer par le nom traduit ("introduction") doit conserver intro-example et masquer default
    dialog.search_input.setText("introduction")
    for i in range(dialog.list_widget.count()):
        item = dialog.list_widget.item(i)
        if item.data(Qt.ItemDataRole.UserRole) == INTRO_PROFILE_ID:
            assert not item.isHidden()
        else:
            assert item.isHidden()


@pytest.mark.ui
def test_main_window_title_and_kofi_inhibited_in_intro_example(
    qtbot: Any,
    mock_db: Any,
    isolated_profiles_dir: Path,
    tmp_path: Path,
    cleanup_qt_widgets: Any,
) -> None:
    """MainWindow affiche 'Exemple d'introduction' et inhibe Ko-fi en mode découverte et première session."""
    from ankidraft.ui.main_window import MainWindow

    seed_initial_data()
    seed_intro_example_data(media_dir=tmp_path / "media")

    window = MainWindow(ai_manager=MagicMock(), profile_name=INTRO_PROFILE_ID)
    qtbot.addWidget(window)

    assert "Exemple d'introduction" in window.windowTitle()

    with patch("ankidraft.ui.dialogs.support_dialog.SupportDialog.show") as mock_support_show:
        window._check_startup_support_dialog()
        mock_support_show.assert_not_called()

    # Ko-fi également inhibé sur un profil vierge durant sa toute première session d'accueil
    SettingModel.set_value("app/is_intro_example", "false")
    first_window = MainWindow(ai_manager=MagicMock(), profile_name="default", is_first_launch_session=True)
    qtbot.addWidget(first_window)
    with patch("ankidraft.ui.dialogs.support_dialog.SupportDialog.show") as mock_support_show:
        first_window._check_startup_support_dialog()
        mock_support_show.assert_not_called()


@pytest.mark.ui
def test_dashboard_sandbox_banner_reset_and_one_click_leave_deletes_intro(
    qtbot: Any,
    mock_db: Any,
    isolated_profiles_dir: Path,
    tmp_path: Path,
    cleanup_qt_widgets: Any,
) -> None:
    """Bandeau Découverte : réinitialisation atomique et bascule + suppression de intro-example."""
    from ankidraft.ui.main_window import MainWindow
    from ankidraft.ui.views.dashboard_view import DashboardView

    pm = ProfileManager()
    pm.create_profile(INTRO_PROFILE_ID)
    seed_initial_data()
    seed_intro_example_data(media_dir=tmp_path / "media")

    # 1. Bandeau visible sur DashboardView en mode découverte + réinitialisation
    dashboard = DashboardView(ai_manager=MagicMock(), profile_name=INTRO_PROFILE_ID)
    qtbot.addWidget(dashboard)
    assert dashboard.intro_banner.isVisibleTo(dashboard)

    SettingModel.set_value("app/demo_batch_reviewed", "true")
    patch_row = StagedPatchModel.get(StagedPatchModel.status == "pending")
    patch_row.status = "rejected"
    patch_row.save()
    assert NoteModel.select().count() >= 8

    with patch("ankidraft.database.seeds.demo_seed.MediaManager") as mock_media_cls:
        mock_media_cls.return_value = mock_media_cls.return_value
        mock_media_cls.return_value.store_media_bytes.return_value = MagicMock(filename="intro_diagram.svg")
        mock_media_cls.return_value.clean_orphaned_media.return_value = 0
        dashboard._on_reset_intro_example()

    assert SettingModel.get_or_none(SettingModel.key == "app/demo_batch_reviewed") is None
    assert StagedPatchModel.select().where(StagedPatchModel.status == "pending").count() == 1
    if dashboard.worker and dashboard.worker.isRunning():
        dashboard.worker.wait()

    # 2. MainWindow : réinitialisation sur le DashboardView monté sans le détruire ni perdre le verrou
    acquired, _ = ProfileLockService.acquire_lock(INTRO_PROFILE_ID)
    assert acquired is True
    window = MainWindow(ai_manager=MagicMock(), profile_name=INTRO_PROFILE_ID)
    qtbot.addWidget(window)
    assert "Exemple d'introduction" in window.windowTitle()

    window._on_view_selected("dashboard")
    mounted_dash = window._view_widgets["dashboard"]
    assert isinstance(mounted_dash, DashboardView)
    with patch("ankidraft.database.seeds.demo_seed.MediaManager") as mock_media_cls:
        mock_media_cls.return_value = mock_media_cls.return_value
        mock_media_cls.return_value.store_media_bytes.return_value = MagicMock(filename="intro_diagram.svg")
        mock_media_cls.return_value.clean_orphaned_media.return_value = 0
        mounted_dash._on_reset_intro_example()
    assert window._view_widgets["dashboard"] is mounted_dash
    assert INTRO_PROFILE_ID in ProfileLockService._active_locks
    if mounted_dash.worker and mounted_dash.worker.isRunning():
        mounted_dash.worker.wait()

    # 3. Garde-fou : si la bascule échoue (verrou sur cible), intro-example n'est PAS supprimé
    with (
        patch("ankidraft.services.profile_lock_service.ProfileLockService.acquire_lock", return_value=(False, None)),
        patch("PySide6.QtWidgets.QMessageBox.warning"),
    ):
        window.leave_intro_example_profile(target_profile="profil_verrouille", delete_intro=True)
    assert window.profile_name == INTRO_PROFILE_ID
    assert INTRO_PROFILE_ID in pm.list_profiles()

    # 4. MainWindow : bascule d'abord vers 'mon_espace', puis suppression d'intro-example
    window.leave_intro_example_profile(target_profile="mon_espace", delete_intro=True)
    assert window.profile_name == "mon_espace"
    assert "mon_espace" in window.windowTitle()
    assert "mon_espace" in pm.list_profiles()
    assert INTRO_PROFILE_ID not in pm.list_profiles()


@pytest.mark.ui
def test_onboarding_checklist_exposes_explore_intro_link_on_real_profile(
    qtbot: Any,
    mock_db: Any,
    cleanup_qt_widgets: Any,
) -> None:
    """OnboardingChecklistWidget propose le lien d'accès à l'Exemple d'introduction sur un vrai profil."""
    from ankidraft.ui.views.dashboard_view import DashboardView

    seed_initial_data()
    dashboard = DashboardView(ai_manager=MagicMock(), profile_name="default")
    qtbot.addWidget(dashboard)

    assert not dashboard.intro_banner.isVisibleTo(dashboard)
    assert dashboard.onboarding_checklist.btn_explore_intro.isVisibleTo(dashboard.onboarding_checklist)

    with qtbot.waitSignal(dashboard.explore_intro_example_requested, timeout=1000):
        dashboard.onboarding_checklist.btn_explore_intro.click()

    if dashboard.worker and dashboard.worker.isRunning():
        dashboard.worker.wait()
