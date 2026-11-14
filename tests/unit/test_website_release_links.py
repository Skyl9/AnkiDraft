"""Tests de non-régression pour les liens de téléchargement dynamiques du site vitrine."""

from __future__ import annotations

import re

import pytest

from ankidraft.services.documentation.doc_service import strip_yaml_frontmatter
from ankidraft.utils.paths import get_project_root

pytestmark = pytest.mark.unit

WEBSITE_ROOT = get_project_root() / "website"


def test_release_lib_resolves_latest_github_assets_without_predefined_version() -> None:
    """Vérifie que website/src/lib/release.ts interroge GitHub releases/latest sans figer pyproject.toml."""
    release_ts = (WEBSITE_ROOT / "src" / "lib" / "release.ts").read_text(encoding="utf-8")

    assert "readPyprojectVersion" not in release_ts
    assert "pyproject.toml" not in release_ts
    assert "'1.0.5'" not in release_ts
    assert "https://api.github.com/repos/${REPO}/releases/latest" in release_ts
    assert "https://github.com/${REPO}/releases/latest/download" in release_ts
    assert "data.assets" in release_ts
    assert "AnkiForge-macos-arm64.dmg" in release_ts
    assert "ankiforge-windows-x64.zip" in release_ts
    assert "AnkiForge-x86_64.AppImage" in release_ts


@pytest.mark.parametrize("lang", ["fr", "en"])
def test_landing_pages_expose_dynamic_latest_release_hooks(lang: str) -> None:
    """Vérifie que les pages d'accueil FR et EN actualisent dynamiquement les liens depuis releases/latest."""
    index_astro = (WEBSITE_ROOT / "src" / "pages" / lang / "index.astro").read_text(encoding="utf-8")

    assert 'id="primary-dl"' in index_astro
    for os_key in ("macos", "windows", "linux"):
        assert f'data-dl-os="{os_key}"' in index_astro
        assert f'data-dl-table="{os_key}"' in index_astro

    assert "https://api.github.com/repos/Skyl9/AnkiDraft/releases/latest" in index_astro
    assert "https://github.com/Skyl9/AnkiDraft/releases/latest/download/" in index_astro


@pytest.mark.parametrize("lang", ["fr", "en"])
def test_installation_guide_links_to_latest_release_and_has_valid_seo(lang: str) -> None:
    """Vérifie que installation.md FR/EN pointe vers releases/latest et garde une description calibrée."""
    install_md = (WEBSITE_ROOT / "src" / "content" / "docs" / lang / "getting-started" / "installation.md").read_text(encoding="utf-8")
    meta, body = strip_yaml_frontmatter(install_md)

    description = meta.get("description", "")
    assert 140 <= len(description) <= 160, f"Description SEO hors plage (140-160) dans {lang}/installation.md : {len(description)}"
    assert "https://github.com/Skyl9/AnkiDraft/releases/latest" in body
    assert not re.search(r"AnkiDraft-Setup-x64\.exe(?!.*zip)", body), f"Le tableau {lang} doit aussi mentionner l'archive portable .zip"
