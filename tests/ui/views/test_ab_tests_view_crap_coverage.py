"""Tests headless pytest-qt pour ABTestsView._on_run_ab_test et ses helpers (résorption CRAP)."""

from __future__ import annotations

import uuid
from typing import Any
from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QThreadPool
from pytestqt.qtbot import QtBot

from ankidraft.database.models import (
    DeckModel,
    LLMConfigModel,
    NoteTypeModel,
    PersonaModel,
    PipelineModel,
    PipelineStepModel,
)
from ankidraft.services.ai.state import PipelineRunState
from ankidraft.ui.views.ab_tests_view.view import ABTestsView

pytestmark = pytest.mark.ui


def _seed_ab_entities() -> dict[str, Any]:
    """Crée les entités Peewee requises pour tester les 3 modes du laboratoire A/B."""
    uid = uuid.uuid4().hex[:6]
    deck = DeckModel.create(name=f"Deck_AB_{uid}")
    nt = NoteTypeModel.create(
        name=f"NT_AB_{uid}",
        fields_schema='["Recto", "Verso"]',
        templates='[{"name": "C1", "qfmt": "{{Recto}}", "afmt": "{{Verso}}"}]',
    )
    eng_a = LLMConfigModel.create(
        display_name=f"EngA_{uid}",
        provider="openai",
        model_id="gpt-4o-mini",
        api_key="enc_a",
    )
    eng_b = LLMConfigModel.create(
        display_name=f"EngB_{uid}",
        provider="anthropic",
        model_id="claude-3-5-haiku",
        api_key="enc_b",
    )
    pers_a = PersonaModel.create(name=f"PersA_{uid}", system_prompt="Prompt A")
    pers_b = PersonaModel.create(name=f"PersB_{uid}", system_prompt="Prompt B")
    pipe_a = PipelineModel.create(name=f"PipeA_{uid}")
    pipe_b = PipelineModel.create(name=f"PipeB_{uid}")
    PipelineStepModel.create(pipeline=pipe_a, persona=pers_a, step_type="LLM_PROMPT", step_order=1)
    PipelineStepModel.create(pipeline=pipe_b, persona=pers_b, step_type="LLM_PROMPT", step_order=1)
    return {
        "deck": deck,
        "nt": nt,
        "eng_a": eng_a,
        "eng_b": eng_b,
        "pers_a": pers_a,
        "pers_b": pers_b,
        "pipe_a": pipe_a,
        "pipe_b": pipe_b,
    }


def _create_ab_view(qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, ai_manager: Any | None = None) -> tuple[ABTestsView, MagicMock]:
    """Instancie ABTestsView avec QThreadPool.globalInstance().start mocké."""
    mock_pool = MagicMock()
    monkeypatch.setattr(QThreadPool, "globalInstance", staticmethod(lambda: mock_pool))
    view = ABTestsView(ai_manager=ai_manager)
    qtbot.addWidget(view)
    return view, mock_pool


def test_ab_tests_view_empty_source_aborts_run(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Refuse de lancer le test A/B si le texte source est vide."""
    _seed_ab_entities()
    view, mock_pool = _create_ab_view(qtbot, monkeypatch)
    view.source_editor.set_content("")

    view._on_run_ab_test()

    mock_pool.start.assert_not_called()
    assert view.orchestrator_a is None
    assert view.orchestrator_b is None


def test_ab_tests_view_run_mode_0_engines_and_completion(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Mode 0 (Moteurs) : instancie 2 providers/orchestrateurs avec persona commune et gère la complétion."""
    entities = _seed_ab_entities()
    fake_ai_manager = MagicMock()
    fake_ai_manager.create_provider_from_config.side_effect = lambda cfg: f"provider:{cfg.display_name}"

    view, mock_pool = _create_ab_view(qtbot, monkeypatch, ai_manager=fake_ai_manager)
    view.source_editor.set_content("La mitochondrie produit l'ATP par phosphorylation oxydative.")
    view.deck_field.set_value(entities["deck"].name, entities["deck"])
    view.model_field.set_value(entities["nt"].name, entities["nt"])
    view.mode_combo.setCurrentIndex(0)
    view.field_a.set_value(entities["eng_a"].display_name, entities["eng_a"])
    view.field_b.set_value(entities["eng_b"].display_name, entities["eng_b"])
    view.persona_field.set_value(entities["pers_a"].name, entities["pers_a"])
    view.chk_independent.setChecked(True)
    view.temp_slider_a.setValue(40)
    view.tok_slider_a.setValue(512)
    view.temp_slider_b.setValue(80)
    view.tok_slider_b.setValue(1024)

    view._on_run_ab_test()

    assert mock_pool.start.call_count == 2
    assert view.orchestrator_a is not None
    assert view.orchestrator_b is not None
    assert view.orchestrator_a._ai_provider == f"provider:{entities['eng_a'].display_name}"
    assert view.orchestrator_b._ai_provider == f"provider:{entities['eng_b'].display_name}"
    assert view.orchestrator_a._steps_override is not None and len(view.orchestrator_a._steps_override) == 1
    assert view.orchestrator_a.state.get_variable("target_deck") == entities["deck"].name
    assert not view.btn_run.isEnabled()

    # Simule la fin des deux branches
    state_a = PipelineRunState(initial_prompt="p")
    state_a.set_variable("generated_cards", [{"Recto": "Q_A", "Verso": "R_A"}])
    state_b = PipelineRunState(initial_prompt="p")
    state_b.set_variable("generated_cards", [{"Recto": "Q_B", "Verso": "R_B"}])

    view._on_finished_a(state_a)
    view._on_finished_b(state_b)

    assert view.btn_run.isEnabled()
    assert len(view.cards_a) == 1
    assert len(view.cards_b) == 1
    view.close()


def test_ab_tests_view_run_mode_1_personas_and_provider_error_resilience(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Mode 1 (Personas) : construit les étapes par persona et tolère une erreur d'instanciation provider."""
    entities = _seed_ab_entities()
    broken_ai_manager = MagicMock()
    broken_ai_manager.create_provider_from_config.side_effect = RuntimeError("Clé API absente")

    view, mock_pool = _create_ab_view(qtbot, monkeypatch, ai_manager=broken_ai_manager)
    view.source_editor.set_content("L'algorithme de Dijkstra calcule les plus courts chemins.")
    view.mode_combo.setCurrentIndex(1)
    view.global_engine_field.set_value(entities["eng_a"].display_name, entities["eng_a"])
    view.field_a.set_value(entities["pers_a"].name, entities["pers_a"])
    view.field_b.set_value(entities["pers_b"].name, entities["pers_b"])

    view._on_run_ab_test()

    assert mock_pool.start.call_count == 2
    assert view._persona_cfg_a == entities["pers_a"]
    assert view._persona_cfg_b == entities["pers_b"]
    assert view.orchestrator_a is not None and view.orchestrator_a._ai_provider is None
    assert view.orchestrator_a._steps_override is not None and view.orchestrator_a._steps_override[0].persona_id == entities["pers_a"].id
    assert view.orchestrator_b is not None and view.orchestrator_b._steps_override is not None
    assert view.orchestrator_b._steps_override[0].persona_id == entities["pers_b"].id

    view._on_error_a("Erreur A")
    view._on_error_b("Erreur B")
    assert view.btn_run.isEnabled()
    view.close()


def test_ab_tests_view_run_mode_2_pipelines(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Mode 2 (Pipelines) : transmet les pipeline_id A et B sans surcharger steps."""
    entities = _seed_ab_entities()
    view, mock_pool = _create_ab_view(qtbot, monkeypatch)
    view.source_editor.set_content("Le théorème de Pythagore relie les côtés d'un triangle rectangle.")
    view.mode_combo.setCurrentIndex(2)
    view.global_engine_field.set_value(entities["eng_a"].display_name, entities["eng_a"])
    view.field_a.set_value(entities["pipe_a"].name, entities["pipe_a"])
    view.field_b.set_value(entities["pipe_b"].name, entities["pipe_b"])

    view._on_run_ab_test()

    assert mock_pool.start.call_count == 2
    assert view._pipeline_cfg_a == entities["pipe_a"]
    assert view._pipeline_cfg_b == entities["pipe_b"]
    assert view.orchestrator_a is not None
    assert view.orchestrator_a.pipeline_id == entities["pipe_a"].id
    assert view.orchestrator_a._steps_override is None
    assert view.orchestrator_b is not None
    assert view.orchestrator_b.pipeline_id == entities["pipe_b"].id
    assert view.orchestrator_b._steps_override is None
    view._elapsed_timer.stop()
    view.close()
