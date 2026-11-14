"""Tests de validation des parcours utilisateurs bilingues, cas d'usage MCP et glossaire."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pytest
from PySide6.QtCore import QUrl
from PySide6.QtGui import QTextDocument

from ankidraft.services.documentation.doc_service import (
    AppDocumentationService,
    get_feature_quick_help,
    strip_yaml_frontmatter,
)
from ankidraft.ui.dialogs.doc_reader_dialog import DocReaderDialog
from ankidraft.utils.paths import get_project_root, get_user_docs_path

WORKFLOW_REL_PATHS = (
    "workflows/medecine-sciences-pdf.md",
    "workflows/langues-et-audio-tts.md",
    "workflows/cours-video-youtube-audio.md",
    "workflows/zero-cle-api-agent-mcp.md",
    "workflows/sauvetage-et-hygiene-anki-mcp.md",
)

ALL_TARGET_DOCS = (
    "getting-started/quickstart.md",
    *WORKFLOW_REL_PATHS,
    "guides/glossaire.md",
)

REQUIRED_MCP_TOOLS = (
    "diagnose_domain_knowledge_gaps",
    "get_flagged_cards",
    "propose_card_split",
    "propose_card_refactor",
    "generate_card_audio",
    "create_notes_batch",
    "write_mcp_artifact",
    "propose_note_type_refactor",
    "trigger_pipeline_run",
)

REQUIRED_HYBRID_ASSETS = (
    "getting-started/assets/arbre_decision_workflow.svg",
    "workflows/assets/mcp_two_phase_commit.svg",
    "workflows/assets/screen_documents.png",
    "workflows/assets/screen_creation.png",
    "workflows/assets/screen_edition.png",
    "workflows/assets/screen_analysis.png",
    "workflows/assets/screen_consultant.png",
)


@pytest.mark.unit
def test_starlight_sidebar_declares_workflows_section() -> None:
    """La configuration Starlight doit exposer la section Parcours & Cas d'Usage en haut de la sidebar."""
    astro_cfg = get_project_root() / "website" / "astro.config.mjs"
    content = astro_cfg.read_text(encoding="utf-8")

    assert "directory: 'workflows'" in content
    assert "Parcours & Cas d'Usage" in content
    assert "Workflows & Use Cases" in content


@pytest.mark.unit
@pytest.mark.parametrize("lang", ["fr", "en"])
@pytest.mark.parametrize("rel_path", ALL_TARGET_DOCS)
def test_bilingual_docs_parity_seo_and_pure_markdown(lang: str, rel_path: str) -> None:
    """Chaque page parcours/glossaire/quickstart existe en FR et EN, sans MDX ni Mermaid, avec description 140-160 car."""
    doc_file = get_user_docs_path(lang) / rel_path
    assert doc_file.is_file(), f"Page manquante : {doc_file}"

    raw_text = doc_file.read_text(encoding="utf-8")
    meta, body = strip_yaml_frontmatter(raw_text)

    title = meta.get("title", "").strip()
    description = meta.get("description", "").strip()
    assert title, f"Titre YAML manquant dans {doc_file}"
    assert 140 <= len(description) <= 160, f"Description SEO hors plage [140, 160] ({len(description)} car.) dans {doc_file}: {description!r}"

    assert "```mermaid" not in body, f"Bloc mermaid interdit dans {doc_file} (incompatible DocReaderDialog)"
    assert not re.search(r"^\s*import\s+.+\s+from\s+", body, flags=re.MULTILINE), f"Import MDX/JSX interdit dans {doc_file}"


@pytest.mark.unit
@pytest.mark.parametrize("lang", ["fr", "en"])
def test_quickstart_has_decision_tree_and_studio_vs_mcp_comparison(lang: str) -> None:
    """Le guide quickstart doit aiguiller vers les 5 parcours et comparer Studio intégré vs Agent MCP externe."""
    quickstart = (get_user_docs_path(lang) / "getting-started" / "quickstart.md").read_text(encoding="utf-8")
    assert "assets/arbre_decision_workflow.svg" in quickstart
    for wf in WORKFLOW_REL_PATHS:
        stem = Path(wf).stem
        assert stem in quickstart, f"Lien vers le parcours '{stem}' manquant dans quickstart ({lang})"
    assert "Studio" in quickstart
    assert "MCP" in quickstart


@pytest.mark.unit
@pytest.mark.parametrize("lang", ["fr", "en"])
def test_workflows_cover_mcp_tools_and_hygiene_scenarios(lang: str) -> None:
    """L'ensemble des 5 parcours doit documenter les outils MCP réels et les campagnes d'hygiène."""
    docs_dir = get_user_docs_path(lang)
    combined = "\n".join((docs_dir / wf).read_text(encoding="utf-8") for wf in WORKFLOW_REL_PATHS)
    for tool_name in REQUIRED_MCP_TOOLS:
        assert tool_name in combined, f"Outil MCP '{tool_name}' absent des parcours ({lang})"


@pytest.mark.unit
@pytest.mark.parametrize("lang", ["fr", "en"])
def test_glossary_has_twelve_concepts_and_before_after_examples(lang: str) -> None:
    """Le glossaire utilisateur doit vulgariser au moins 12 concepts avec exemples Avant / Après."""
    glossary_path = get_user_docs_path(lang) / "guides" / "glossaire.md"
    _, body = strip_yaml_frontmatter(glossary_path.read_text(encoding="utf-8"))

    headings = re.findall(r"^#{2,3}\s+", body, flags=re.MULTILINE)
    assert len(headings) >= 12, f"Le glossaire ({lang}) ne contient que {len(headings)} sections (< 12)"

    if lang == "fr":
        assert len(re.findall(r"\bAvant\b", body)) >= 10
        assert len(re.findall(r"\bAprès\b", body)) >= 10
    else:
        assert len(re.findall(r"\bBefore\b", body)) >= 10
        assert len(re.findall(r"\bAfter\b", body)) >= 10


@pytest.mark.unit
@pytest.mark.parametrize("lang", ["fr", "en"])
@pytest.mark.parametrize("asset_rel", REQUIRED_HYBRID_ASSETS)
def test_hybrid_svg_and_png_assets_exist_and_are_valid(lang: str, asset_rel: str) -> None:
    """Les captures PySide6 PNG et schémas vectoriels SVG doivent exister en FR et EN et être valides."""
    asset_file = get_user_docs_path(lang) / asset_rel
    assert asset_file.is_file(), f"Illustration manquante : {asset_file}"
    raw = asset_file.read_bytes()
    assert len(raw) > 200, f"Illustration trop petite ou vide : {asset_file}"

    if asset_rel.endswith(".png"):
        assert raw.startswith(b"\x89PNG\r\n\x1a\n"), f"Signature PNG invalide : {asset_file}"
    else:
        text = raw.decode("utf-8")
        assert "<svg" in text and "</svg>" in text, f"Contenu SVG invalide : {asset_file}"


@pytest.mark.unit
def test_doc_service_indexes_workflows_and_quick_help() -> None:
    """AppDocumentationService doit classer workflows/ dans la bonne catégorie et exposer glossaire/parcours."""
    AppDocumentationService._instances.clear()
    svc_fr = AppDocumentationService.get_instance(language="fr", scope="user")
    svc_en = AppDocumentationService.get_instance(language="en", scope="user")

    fr_workflow_topics = [t for t in svc_fr.get_topics() if t.path.startswith("workflows/")]
    en_workflow_topics = [t for t in svc_en.get_topics() if t.path.startswith("workflows/")]

    assert len(fr_workflow_topics) == 5
    assert len(en_workflow_topics) == 5
    assert all(t.category == "Parcours & Cas d'Usage" for t in fr_workflow_topics)
    assert all(t.category == "Workflows & Use Cases" for t in en_workflow_topics)

    quick_glossary = get_feature_quick_help("glossaire")
    quick_workflows = get_feature_quick_help("parcours")
    assert "guides/glossaire.md" in quick_glossary
    assert "getting-started/quickstart.md" in quick_workflows


@pytest.mark.ui
def test_doc_reader_dialog_opens_workflows_and_glossary_with_images(qtbot: Any) -> None:
    """DocReaderDialog doit ouvrir un parcours et le glossaire hors-ligne en résolvant les illustrations locales."""
    dlg_hygiene = DocReaderDialog.open_guide("sauvetage-et-hygiene-anki-mcp.md")
    qtbot.addWidget(dlg_hygiene)
    html_hygiene = dlg_hygiene.text_browser.toHtml()
    assert "get_flagged_cards" in html_hygiene
    assert "diagnose_domain_knowledge_gaps" in html_hygiene

    img_analysis = dlg_hygiene.text_browser.document().resource(
        QTextDocument.ResourceType.ImageResource,
        QUrl("assets/screen_analysis.png"),
    )
    assert img_analysis is not None, "La capture assets/screen_analysis.png doit être résolue dans DocReaderDialog"

    dlg_mcp = DocReaderDialog.open_guide("zero-cle-api-agent-mcp.md")
    qtbot.addWidget(dlg_mcp)
    img_svg = dlg_mcp.text_browser.document().resource(
        QTextDocument.ResourceType.ImageResource,
        QUrl("assets/mcp_two_phase_commit.svg"),
    )
    assert img_svg is not None, "Le schéma SVG assets/mcp_two_phase_commit.svg doit être résolu dans DocReaderDialog"

    dlg_glossary = DocReaderDialog.open_guide("glossaire.md")
    qtbot.addWidget(dlg_glossary)
    plain_glossary = dlg_glossary.text_browser.toPlainText()
    assert "Wozniak" in plain_glossary
    assert "MCP" in plain_glossary
