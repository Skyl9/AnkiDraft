from __future__ import annotations

from typing import Any

import pytest

from ankidraft.database.models import SettingModel
from ankidraft.ui.views.dashboard_view import DashboardView, OnboardingChecklistWidget


@pytest.mark.ui
def test_onboarding_checklist_widget_progress_and_collapse(qtbot: Any) -> None:
    widget = OnboardingChecklistWidget()
    qtbot.addWidget(widget)

    widget.update_progress(ai_ready=True, doc_imported=True, cards_created=False, apkg_exported=False)
    assert widget.progress_bar.value() == 2
    assert "2/4" in widget.lbl_progress.text()
    assert widget.steps_container.isVisibleTo(widget) or not widget.is_collapsed

    widget.update_progress(ai_ready=True, doc_imported=True, cards_created=True, apkg_exported=True)
    assert widget.progress_bar.value() == 4
    assert "4/4" in widget.lbl_progress.text()
    assert widget.is_collapsed is True


@pytest.mark.ui
def test_onboarding_checklist_hide_persists_in_setting_model(qtbot: Any, mock_db: Any) -> None:
    view = DashboardView()
    qtbot.addWidget(view)

    assert view.onboarding_checklist is not None
    view.onboarding_checklist.btn_hide.click()

    setting = SettingModel.get_or_none(SettingModel.key == "ui/onboarding_checklist_hidden")
    assert setting is not None
    assert setting.value == "true"

    if view.worker and view.worker.isRunning():
        view.worker.wait()
