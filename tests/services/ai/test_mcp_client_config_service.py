"""Tests unitaires du service de détection, configuration MCP 1-clic et diagnostic Ollama."""

from __future__ import annotations

import json
import urllib.error
from pathlib import Path
from typing import Any

import pytest

from ankidraft.services.ai.mcp_client_config_service import (
    configure_client_mcp,
    detect_mcp_clients,
    diagnose_ollama_connection,
    get_client_config_path,
    render_client_snippet,
)

pytestmark = pytest.mark.unit


def test_get_client_config_path_per_os(tmp_path: Path) -> None:
    """Résout les chemins de configuration canoniques selon l'OS."""
    home = tmp_path / "home"
    cwd = tmp_path / "proj"

    assert get_client_config_path("claude", home_dir=home, cwd=cwd, platform="darwin") == (home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json")
    assert get_client_config_path("claude", home_dir=home, cwd=cwd, platform="linux") == (home / ".config" / "claude" / "claude_desktop_config.json")
    assert get_client_config_path("agy", home_dir=home, cwd=cwd, platform="darwin") == (home / ".gemini" / "config" / "mcp_config.json")
    # Repli Antigravity 2.0 App si seul ~/.gemini/antigravity/mcp_config.json existe
    app_only_home = tmp_path / "home_app_only"
    app_agy_cfg = app_only_home / ".gemini" / "antigravity" / "mcp_config.json"
    app_agy_cfg.parent.mkdir(parents=True)
    app_agy_cfg.write_text('{"mcpServers": {}}', encoding="utf-8")
    assert get_client_config_path("agy", home_dir=app_only_home, cwd=cwd, platform="darwin") == app_agy_cfg
    assert get_client_config_path("claude_code", home_dir=home, cwd=cwd, platform="darwin") == (home / ".claude.json")
    assert get_client_config_path("windsurf", home_dir=home, cwd=cwd, platform="darwin") == (home / ".codeium" / "windsurf" / "mcp_config.json")


def test_detect_mcp_clients_identifies_installed_and_configured_states(tmp_path: Path) -> None:
    """Détecte les clients présents, configurés, désynchronisés ou JSON invalides."""
    home = tmp_path / "home"
    cwd = tmp_path / "proj"
    home.mkdir(parents=True)
    cwd.mkdir(parents=True)

    # Claude Desktop configuré avec le bon jeton
    claude_cfg = home / ".config" / "claude" / "claude_desktop_config.json"
    claude_cfg.parent.mkdir(parents=True)
    claude_cfg.write_text(
        json.dumps(
            {
                "mcpServers": {
                    "ankidraft": {
                        "url": "http://127.0.0.1:8765/mcp",
                        "headers": {"Authorization": "Bearer tok_ok"},
                    }
                }
            }
        ),
        encoding="utf-8",
    )

    # Cursor installé via dossier .cursor mais sans ankidraft
    (home / ".cursor").mkdir(parents=True)

    # Windsurf avec mauvais jeton
    windsurf_cfg = home / ".codeium" / "windsurf" / "mcp_config.json"
    windsurf_cfg.parent.mkdir(parents=True)
    windsurf_cfg.write_text(
        json.dumps(
            {
                "mcpServers": {
                    "ankidraft": {
                        "serverUrl": "http://127.0.0.1:8765/mcp",
                        "headers": {"Authorization": "Bearer ancien_jeton"},
                    }
                }
            }
        ),
        encoding="utf-8",
    )

    # Claude Code avec JSON corrompu
    (home / ".claude.json").write_text("{json invalide", encoding="utf-8")

    statuses = detect_mcp_clients(
        home_dir=home,
        cwd=cwd,
        platform="linux",
        active_token="tok_ok",
        which_fn=lambda cmd: "/usr/local/bin/agy" if cmd == "agy" else None,
    )

    assert statuses["claude"].installed is True
    assert statuses["claude"].status == "configured"

    assert statuses["cursor"].installed is True
    assert statuses["cursor"].status == "unconfigured"

    assert statuses["windsurf"].installed is True
    assert statuses["windsurf"].status == "token_mismatch"

    assert statuses["claude_code"].installed is True
    assert statuses["claude_code"].status == "invalid_json"

    assert statuses["agy"].installed is True
    assert statuses["agy"].status == "unconfigured"


def test_configure_client_mcp_merges_existing_servers_and_creates_backup(tmp_path: Path) -> None:
    """Fusionne ankidraft sans écraser les autres serveurs MCP et crée un .bak préalable."""
    home = tmp_path / "home"
    cfg_path = home / ".config" / "claude" / "claude_desktop_config.json"
    cfg_path.parent.mkdir(parents=True)
    original_data = {
        "globalShortcut": "Ctrl+Space",
        "mcpServers": {
            "filesystem": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem"]},
            "ankidraft": {"url": "http://127.0.0.1:8765/mcp", "headers": {"Authorization": "Bearer old"}},
        },
    }
    cfg_path.write_text(json.dumps(original_data, indent=2), encoding="utf-8")

    result = configure_client_mcp(
        "claude",
        url="http://127.0.0.1:8765/mcp",
        token="new_secret_token",
        config_path=cfg_path,
    )

    assert result.config_path == cfg_path
    assert result.created is False
    assert result.backup_path is not None
    assert result.backup_path.exists()
    assert json.loads(result.backup_path.read_text(encoding="utf-8")) == original_data

    merged = json.loads(cfg_path.read_text(encoding="utf-8"))
    assert merged["globalShortcut"] == "Ctrl+Space"
    assert merged["mcpServers"]["filesystem"] == original_data["mcpServers"]["filesystem"]
    assert merged["mcpServers"]["ankidraft"]["headers"]["Authorization"] == "Bearer new_secret_token"


def test_configure_client_mcp_refuses_corrupted_json_without_overwriting(tmp_path: Path) -> None:
    """Refuse proprement de réécrire un fichier de config JSON corrompu."""
    cfg_path = tmp_path / "mcp.json"
    cfg_path.write_text("{not valid json", encoding="utf-8")

    with pytest.raises(ValueError, match="JSON"):
        configure_client_mcp(
            "cursor",
            url="http://127.0.0.1:8765/mcp",
            token="tok",
            config_path=cfg_path,
        )

    assert cfg_path.read_text(encoding="utf-8") == "{not valid json"


def test_configure_client_mcp_creates_new_file_for_agy_and_claude_code(tmp_path: Path) -> None:
    """Crée un fichier neuf proprement formaté lorsque la config cible n'existe pas."""
    # Antigravity (agy) fusionne proprement dans mcpServers sans écraser les autres serveurs
    agy_path = tmp_path / ".gemini" / "config" / "mcp_config.json"
    agy_path.parent.mkdir(parents=True)
    agy_path.write_text(json.dumps({"mcpServers": {"maquette_studio": {"disabled": True}}}), encoding="utf-8")
    res_agy = configure_client_mcp("agy", url="http://127.0.0.1:8765/mcp", token="tok_agy", config_path=agy_path)
    assert res_agy.created is False
    assert res_agy.backup_path is not None
    assert res_agy.backup_path.exists()
    parsed_agy = json.loads(agy_path.read_text(encoding="utf-8"))
    assert parsed_agy["mcpServers"]["maquette_studio"] == {"disabled": True}
    assert parsed_agy["mcpServers"]["ankidraft"]["url"] == "http://127.0.0.1:8765/mcp"
    assert parsed_agy["mcpServers"]["ankidraft"]["headers"]["Authorization"] == "Bearer tok_agy"
    assert detect_mcp_clients(home_dir=tmp_path, cwd=tmp_path, active_token="tok_agy")["agy"].status == "configured"
    assert detect_mcp_clients(home_dir=tmp_path, cwd=tmp_path, active_token="autre_tok")["agy"].status == "token_mismatch"

    cc_snippet = render_client_snippet("claude_code", url="http://127.0.0.1:8765/mcp", token="tok_cc")
    assert "claude mcp add" in cc_snippet
    assert "tok_cc" in cc_snippet

    cc_path = tmp_path / ".claude.json"
    res_cc = configure_client_mcp("claude_code", url="http://127.0.0.1:8765/mcp", token="tok_cc", config_path=cc_path)
    assert res_cc.created is True
    parsed_cc = json.loads(cc_path.read_text(encoding="utf-8"))
    assert parsed_cc["mcpServers"]["ankidraft"]["type"] == "http"

    ws_path = tmp_path / ".codeium" / "windsurf" / "mcp_config.json"
    res_ws = configure_client_mcp("windsurf", url="http://127.0.0.1:8765/mcp", token="tok_ws", config_path=ws_path)
    assert res_ws.created is True
    parsed_ws = json.loads(ws_path.read_text(encoding="utf-8"))
    assert parsed_ws["mcpServers"]["ankidraft"]["serverUrl"] == "http://127.0.0.1:8765/mcp"


def test_detect_mcp_clients_darwin_apps_and_not_detected(tmp_path: Path) -> None:
    """Détecte les .app macOS via applications_dir injectable et gère les clients absents."""
    home = tmp_path / "home"
    cwd = tmp_path / "proj"
    apps = tmp_path / "Applications"
    home.mkdir(parents=True)
    cwd.mkdir(parents=True)
    apps.mkdir(parents=True)

    (apps / "Claude.app").mkdir()
    (apps / "Windsurf.app").mkdir()

    statuses = detect_mcp_clients(
        home_dir=home,
        cwd=cwd,
        platform="darwin",
        which_fn=lambda cmd: "/usr/bin/claude" if cmd == "claude" else None,
        applications_dir=apps,
    )
    assert statuses["claude"].installed is True
    assert statuses["claude"].status == "unconfigured"
    assert statuses["windsurf"].installed is True
    assert statuses["claude_code"].installed is True
    assert statuses["cursor"].installed is False
    assert statuses["cursor"].status == "not_detected"
    assert statuses["agy"].installed is False
    assert get_client_config_path("inconnu", home_dir=home, cwd=cwd, platform="darwin") is None


def test_diagnose_ollama_connection_all_cases() -> None:
    """Distingue modèles présents, 0 modèle (recommandation), installé arrêté, non installé et anti-SSRF."""

    class _FakeResp:
        def __init__(self, payload: dict[str, Any]) -> None:
            self._data = json.dumps(payload).encode("utf-8")

        def read(self) -> bytes:
            return self._data

        def __enter__(self) -> _FakeResp:
            return self

        def __exit__(self, *args: Any) -> None:
            pass

    # 1. Anti-SSRF
    diag_ssrf = diagnose_ollama_connection("https://evil.example.com:11434")
    assert diag_ssrf.status == "invalid_url"

    # 2. En ligne avec modèles
    diag_ok = diagnose_ollama_connection(
        "http://localhost:11434",
        urlopen_fn=lambda req, timeout=1.2: _FakeResp({"models": [{"name": "qwen2.5:7b"}]}),
    )
    assert diag_ok.status == "online_models"
    assert diag_ok.models == ["qwen2.5:7b"]

    # 3. En ligne avec 0 modèle
    diag_empty = diagnose_ollama_connection(
        "http://localhost:11434",
        urlopen_fn=lambda req, timeout=1.2: _FakeResp({"models": []}),
    )
    assert diag_empty.status == "online_empty"
    assert "qwen2.5:7b" in diag_empty.recommended_command

    # 4. Installé mais service arrêté
    def _fail_conn(*args: Any, **kwargs: Any) -> Any:
        raise urllib.error.URLError("Connection refused")

    diag_stopped = diagnose_ollama_connection(
        "http://localhost:11434",
        urlopen_fn=_fail_conn,
        which_fn=lambda cmd: "/usr/local/bin/ollama" if cmd == "ollama" else None,
        extra_binary_paths=[],
    )
    assert diag_stopped.status == "installed_stopped"
    assert diag_stopped.recommended_command == "ollama serve"

    # 5. Non installé
    diag_missing = diagnose_ollama_connection(
        "http://localhost:11434",
        urlopen_fn=_fail_conn,
        which_fn=lambda _cmd: None,
        extra_binary_paths=[],
    )
    assert diag_missing.status == "not_installed"
