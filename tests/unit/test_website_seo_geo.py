"""Tests unitaires des invariants SEO et GEO du site utilisateur (website/)."""

from __future__ import annotations

import json
from pathlib import Path
import re

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
WEBSITE_DIR = REPO_ROOT / "website"
DOCS_DIR = WEBSITE_DIR / "src" / "content" / "docs"


@pytest.mark.unit
def test_og_banner_and_robots_exist() -> None:
    """Vérifie la présence de la bannière OpenGraph et de robots.txt avec crawlers IA."""
    og_banner = WEBSITE_DIR / "public" / "assets" / "og-banner.svg"
    assert og_banner.is_file()
    svg_text = og_banner.read_text(encoding="utf-8")
    assert 'viewBox="0 0 1200 630"' in svg_text

    robots = WEBSITE_DIR / "public" / "robots.txt"
    assert robots.is_file()
    robots_text = robots.read_text(encoding="utf-8")
    for bot in ("*", "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "PerplexityBot", "Google-Extended"):
        assert f"User-agent: {bot}" in robots_text
    assert "Sitemap: https://ankidraft.app/sitemap-index.xml" in robots_text


@pytest.mark.unit
def test_headers_and_package_json_seo_geo() -> None:
    """Vérifie _headers Cloudflare Pages et l'intégration de generate-llms-txt.mjs dans package.json."""
    headers_text = (WEBSITE_DIR / "public" / "_headers").read_text(encoding="utf-8")
    for path in ("/llms.txt", "/llms-full.txt", "/robots.txt", "/sitemap-index.xml"):
        assert path in headers_text

    pkg = json.loads((WEBSITE_DIR / "package.json").read_text(encoding="utf-8"))
    build_cmd = pkg["scripts"]["build"]
    assert "generate-llms-txt.mjs" in build_cmd
    assert (WEBSITE_DIR / "scripts" / "generate-llms-txt.mjs").is_file()


@pytest.mark.unit
def test_astro_config_and_head_component() -> None:
    """Vérifie la configuration Starlight OpenGraph et le composant Head.astro JSON-LD."""
    astro_cfg = (WEBSITE_DIR / "astro.config.mjs").read_text(encoding="utf-8")
    assert "og:image" in astro_cfg
    assert "twitter:image" in astro_cfg
    assert "./src/components/Head.astro" in astro_cfg

    head_astro = (WEBSITE_DIR / "src" / "components" / "Head.astro").read_text(encoding="utf-8")
    assert "application/ld+json" in head_astro
    for schema_type in ("TechArticle", "HowTo", "FAQPage"):
        assert schema_type in head_astro


@pytest.mark.unit
def test_landing_pages_have_og_and_software_application() -> None:
    """Vérifie les balises OpenGraph, Twitter Cards et JSON-LD SoftwareApplication sur les pages vitrines."""
    root_index = (WEBSITE_DIR / "src" / "pages" / "index.astro").read_text(encoding="utf-8")
    assert "og:title" in root_index
    assert "twitter:card" in root_index
    assert "sitemap-index.xml" in root_index

    for locale in ("fr", "en"):
        page = (WEBSITE_DIR / "src" / "pages" / locale / "index.astro").read_text(encoding="utf-8")
        assert "og:title" in page
        assert "twitter:card" in page
        assert "SoftwareApplication" in page
        assert "sitemap-index.xml" in page


@pytest.mark.unit
def test_all_doc_descriptions_calibrated_for_seo() -> None:
    """Vérifie que 100 % des pages FR/EN ont une description SEO entre 140 et 160 caractères."""
    md_files = sorted(DOCS_DIR.rglob("*.md"))
    assert len(md_files) >= 40
    for md_file in md_files:
        text = md_file.read_text(encoding="utf-8")
        match = re.search(r"^description:\s*(.+)$", text, re.MULTILINE)
        assert match is not None, f"Description manquante dans {md_file}"
        desc = match.group(1).strip().strip('"').strip("'")
        assert 140 <= len(desc) <= 160, f"{md_file}: longueur {len(desc)} hors [140, 160]"
