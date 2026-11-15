"""Service de détection, configuration 1-clic des clients MCP externes et diagnostic Ollama."""

from __future__ import annotations

import json
import logging
import os
import shutil
import sys
import urllib.error
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

from ankidraft.services.ai.model_catalog import _is_loopback_url
from ankidraft.utils.i18n import tr

logger = logging.getLogger(__name__)

MCPClientKey = Literal["claude", "agy", "cursor", "claude_code", "windsurf"]
MCPClientState = Literal["not_detected", "unconfigured", "configured", "token_mismatch", "invalid_json"]
OllamaDiagState = Literal["online_models", "online_empty", "installed_stopped", "not_installed", "invalid_url"]

_RECOMMENDED_OLLAMA_MODEL = "qwen2.5:7b"

_CLIENT_DISPLAY_NAMES: dict[str, str] = {
    "claude": "Claude Desktop",
    "agy": "Antigravity CLI (agy)",
    "cursor": "Cursor",
    "claude_code": "Claude Code",
    "windsurf": "Windsurf",
}


@dataclass(frozen=True)
class MCPClientStatus:
    """État de détection et de configuration d'un client MCP externe sur le système."""

    client_key: str
    display_name: str
    config_path: Path | None
    installed: bool
    status: MCPClientState
    detail: str


@dataclass(frozen=True)
class MCPConfigureResult:
    """Résultat d'une opération de configuration automatique 1-clic."""

    client_key: str
    config_path: Path
    backup_path: Path | None
    created: bool


@dataclass(frozen=True)
class OllamaDiagnostic:
    """Résultat structuré du diagnostic guidé de connexion Ollama."""

    status: OllamaDiagState
    title: str
    detail: str
    recommended_command: str = ""
    models: list[str] = field(default_factory=list)


def get_client_config_path(
    client: str,
    *,
    home_dir: Path | None = None,
    cwd: Path | None = None,
    platform: str | None = None,
    appdata_dir: str | None = None,
) -> Path | None:
    """Retourne le chemin canonique du fichier de configuration MCP pour un client donné."""
    home = home_dir if home_dir is not None else Path.home()
    work_dir = cwd if cwd is not None else Path.cwd()
    plat = platform if platform is not None else sys.platform

    if client == "claude":
        if plat == "darwin":
            return home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
        if plat == "win32":
            appdata = appdata_dir if appdata_dir is not None else os.environ.get("APPDATA")
            return Path(appdata) / "Claude" / "claude_desktop_config.json" if appdata else None
        return home / ".config" / "claude" / "claude_desktop_config.json"

    if client == "agy":
        global_cfg = home / ".gemini" / "config" / "mcp_config.json"
        app_cfg = home / ".gemini" / "antigravity" / "mcp_config.json"
        if global_cfg.exists() or (home / ".gemini" / "antigravity-cli").exists() or not app_cfg.exists():
            return global_cfg
        return app_cfg

    if client == "cursor":
        project_cursor = work_dir / ".cursor" / "mcp.json"
        if project_cursor.parent.exists():
            return project_cursor
        return home / ".cursor" / "mcp.json"

    if client == "claude_code":
        project_mcp = work_dir / ".mcp.json"
        if project_mcp.exists():
            return project_mcp
        return home / ".claude.json"

    if client == "windsurf":
        return home / ".codeium" / "windsurf" / "mcp_config.json"

    return None


@dataclass(frozen=True)
class _ClientInstallProbe:
    """Sonde déclarative d'installation d'un client MCP externe."""

    darwin_app: str | None = None
    home_subdir: tuple[str, ...] | None = None
    cli_name: str | None = None
    require_config_file_only: bool = False


_CLIENT_INSTALL_PROBES: dict[str, _ClientInstallProbe] = {
    "claude": _ClientInstallProbe(darwin_app="Claude.app"),
    "agy": _ClientInstallProbe(home_subdir=(".gemini", "antigravity-cli"), cli_name="agy"),
    "cursor": _ClientInstallProbe(darwin_app="Cursor.app", cli_name="cursor"),
    "claude_code": _ClientInstallProbe(home_subdir=(".claude",), cli_name="claude", require_config_file_only=True),
    "windsurf": _ClientInstallProbe(darwin_app="Windsurf.app", home_subdir=(".codeium", "windsurf"), cli_name="windsurf"),
}


def _is_client_installed(
    client: str,
    config_path: Path | None,
    *,
    home_dir: Path,
    platform: str,
    which_fn: Callable[[str], str | None],
    applications_dir: Path | None = None,
) -> bool:
    """Détermine de manière heuristique si le client MCP est présent sur l'environnement."""
    probe = _CLIENT_INSTALL_PROBES.get(client)
    if probe is None:
        return False
    if config_path is not None and (config_path.exists() or (not probe.require_config_file_only and config_path.parent.exists())):
        return True
    apps_root = applications_dir if applications_dir is not None else Path("/Applications")
    if platform == "darwin" and probe.darwin_app and (apps_root / probe.darwin_app).exists():
        return True
    if probe.home_subdir and home_dir.joinpath(*probe.home_subdir).exists():
        return True
    return bool(probe.cli_name and which_fn(probe.cli_name) is not None)


def _extract_ankidraft_entry(client: str, parsed: dict[str, Any]) -> dict[str, Any] | None:
    """Extrait la section AnkiDraft depuis un fichier de configuration client parsé."""
    _ = client
    servers = parsed.get("mcpServers")
    if isinstance(servers, dict):
        entry = servers.get("ankidraft")
        if isinstance(entry, dict):
            return entry
    return None


def _entry_matches_token(entry: dict[str, Any], active_token: str | None) -> bool:
    """Vérifie si l'en-tête Authorization Bearer correspond au jeton actif."""
    if not active_token:
        return True
    headers = entry.get("headers")
    if not isinstance(headers, dict):
        return False
    auth = str(headers.get("Authorization", "")).strip()
    return auth == f"Bearer {active_token}"


def detect_mcp_clients(
    *,
    home_dir: Path | None = None,
    cwd: Path | None = None,
    platform: str | None = None,
    active_token: str | None = None,
    which_fn: Callable[[str], str | None] | None = None,
    applications_dir: Path | None = None,
) -> dict[str, MCPClientStatus]:
    """Inspecte les emplacements des principaux clients MCP et retourne leur état."""
    home = home_dir if home_dir is not None else Path.home()
    work_dir = cwd if cwd is not None else Path.cwd()
    plat = platform if platform is not None else sys.platform
    effective_which = which_fn if which_fn is not None else shutil.which

    results: dict[str, MCPClientStatus] = {}
    for client_key, display_name in _CLIENT_DISPLAY_NAMES.items():
        cfg_path = get_client_config_path(client_key, home_dir=home, cwd=work_dir, platform=plat)
        installed = _is_client_installed(
            client_key,
            cfg_path,
            home_dir=home,
            platform=plat,
            which_fn=effective_which,
            applications_dir=applications_dir,
        )

        if cfg_path is not None and cfg_path.exists():
            try:
                raw_text = cfg_path.read_text(encoding="utf-8")
                parsed = json.loads(raw_text) if raw_text.strip() else {}
                if not isinstance(parsed, dict):
                    raise ValueError("Root JSON must be an object")
            except Exception:
                results[client_key] = MCPClientStatus(
                    client_key=client_key,
                    display_name=display_name,
                    config_path=cfg_path,
                    installed=True,
                    status="invalid_json",
                    detail=tr("Fichier JSON existant invalide ou illisible"),
                )
                continue

            entry = _extract_ankidraft_entry(client_key, parsed)
            if entry is None:
                results[client_key] = MCPClientStatus(
                    client_key=client_key,
                    display_name=display_name,
                    config_path=cfg_path,
                    installed=True,
                    status="unconfigured",
                    detail=tr("Client détecté — AnkiDraft non encore configuré"),
                )
            elif not _entry_matches_token(entry, active_token):
                results[client_key] = MCPClientStatus(
                    client_key=client_key,
                    display_name=display_name,
                    config_path=cfg_path,
                    installed=True,
                    status="token_mismatch",
                    detail=tr("Jeton obsolète — mise à jour recommandée"),
                )
            else:
                results[client_key] = MCPClientStatus(
                    client_key=client_key,
                    display_name=display_name,
                    config_path=cfg_path,
                    installed=True,
                    status="configured",
                    detail=tr("Configuré et synchronisé"),
                )
        elif installed:
            results[client_key] = MCPClientStatus(
                client_key=client_key,
                display_name=display_name,
                config_path=cfg_path,
                installed=True,
                status="unconfigured",
                detail=tr("Client détecté — prêt pour configuration 1-clic"),
            )
        else:
            results[client_key] = MCPClientStatus(
                client_key=client_key,
                display_name=display_name,
                config_path=cfg_path,
                installed=False,
                status="not_detected",
                detail=tr("Non détecté sur cet ordinateur"),
            )

    return results


def _build_client_entry(client: str, url: str, token: str) -> dict[str, Any]:
    """Construit l'entrée JSON attendue pour AnkiDraft selon le schéma du client."""
    headers = {"Authorization": f"Bearer {token}"}
    if client == "claude_code":
        return {"type": "http", "url": url, "headers": headers}
    if client == "windsurf":
        return {"serverUrl": url, "headers": headers}
    return {"url": url, "headers": headers}


def render_client_file_template(client: str, *, url: str, token: str | None) -> str:
    """Génère un contenu JSON initial valide lorsqu'un fichier de configuration doit être créé."""
    effective_token = token or "VOTRE_JETON_BEARER"
    payload: dict[str, Any] = {"mcpServers": {"ankidraft": _build_client_entry(client, url, effective_token)}}
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def render_client_snippet(client: str, *, url: str, token: str | None) -> str:
    """Génère le bloc JSON ou la commande CLI prête à copier pour un client MCP."""
    effective_token = token or "VOTRE_JETON_BEARER"
    if client in ("claude", "agy", "cursor", "windsurf"):
        payload: dict[str, Any] = {"mcpServers": {"ankidraft": _build_client_entry(client, url, effective_token)}}
        return json.dumps(payload, indent=2, ensure_ascii=False)
    if client == "claude_code":
        return f'claude mcp add --transport http ankidraft "{url}" \\\n  --header "Authorization: Bearer {effective_token}"'
    if client == "curl":
        return (
            f'curl -X POST "{url}" \\\n'
            f'  -H "Authorization: Bearer {effective_token}" \\\n'
            '  -H "Content-Type: application/json" \\\n'
            '  -d \'{"jsonrpc": "2.0", "method": "tools/list", "params": {}, "id": 1}\''
        )
    return ""


def configure_client_mcp(
    client: str,
    *,
    url: str,
    token: str,
    config_path: Path | None = None,
    home_dir: Path | None = None,
    cwd: Path | None = None,
    platform: str | None = None,
) -> MCPConfigureResult:
    """Configure un client MCP en fusionnant l'entrée AnkiDraft après sauvegarde .bak préalable.

    Lève ValueError si le fichier cible existe et contient du JSON invalide ou non-objet,
    afin de ne jamais corrompre une configuration existante.
    """
    target_path = config_path or get_client_config_path(client, home_dir=home_dir, cwd=cwd, platform=platform)
    if target_path is None:
        raise ValueError(tr("Aucun chemin de configuration disponible pour le client '%1'.", client))

    created = not target_path.exists()
    backup_path: Path | None = None
    existing_data: dict[str, Any] = {}

    if not created:
        raw_content = target_path.read_text(encoding="utf-8")
        if raw_content.strip():
            try:
                parsed = json.loads(raw_content)
            except json.JSONDecodeError as exc:
                raise ValueError(tr("Le fichier JSON existant est invalide (%1) : %2", target_path.name, str(exc))) from exc
            if not isinstance(parsed, dict):
                raise ValueError(tr("Le fichier JSON existant (%1) doit contenir un objet racine.", target_path.name))
            existing_data = parsed

        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = target_path.with_name(f"{target_path.name}.bak.{stamp}")
        shutil.copy2(target_path, backup_path)

    servers_raw = existing_data.get("mcpServers")
    servers: dict[str, Any] = dict(servers_raw) if isinstance(servers_raw, dict) else {}
    servers["ankidraft"] = _build_client_entry(client, url, token)
    updated_data: dict[str, Any] = {**existing_data, "mcpServers": servers}

    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(json.dumps(updated_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    logger.info("Client MCP '%s' configuré dans %s (backup=%s)", client, target_path, backup_path)
    return MCPConfigureResult(
        client_key=client,
        config_path=target_path,
        backup_path=backup_path,
        created=created,
    )


def _default_ollama_binary_paths() -> list[Path]:
    """Retourne les emplacements usuels du binaire/application Ollama selon l'OS."""
    home = Path.home()
    if sys.platform == "darwin":
        return [
            Path("/Applications/Ollama.app"),
            home / "Applications" / "Ollama.app",
            Path("/usr/local/bin/ollama"),
            Path("/opt/homebrew/bin/ollama"),
        ]
    if sys.platform == "win32":
        local_app = os.environ.get("LOCALAPPDATA", "")
        paths = [Path(local_app) / "Programs" / "Ollama" / "ollama.exe"] if local_app else []
        return paths
    return [Path("/usr/local/bin/ollama"), Path("/usr/bin/ollama"), home / ".local" / "bin" / "ollama"]


def _is_ollama_binary_present(
    which_fn: Callable[[str], str | None],
    extra_binary_paths: list[Path] | None,
) -> bool:
    if which_fn("ollama") is not None:
        return True
    candidates = extra_binary_paths if extra_binary_paths is not None else _default_ollama_binary_paths()
    return any(p.exists() for p in candidates)


def diagnose_ollama_connection(
    base_url: str,
    *,
    urlopen_fn: Callable[..., Any] | None = None,
    which_fn: Callable[[str], str | None] | None = None,
    extra_binary_paths: list[Path] | None = None,
) -> OllamaDiagnostic:
    """Teste la connectivité au serveur Ollama local et produit un diagnostic guidé en français."""
    effective_which = which_fn if which_fn is not None else shutil.which
    cleaned_url = base_url.strip().rstrip("/")
    if not (cleaned_url.startswith("http://") or cleaned_url.startswith("https://")):
        cleaned_url = f"http://{cleaned_url}"

    if not _is_loopback_url(cleaned_url):
        return OllamaDiagnostic(
            status="invalid_url",
            title=tr("URL non locale (anti-SSRF)"),
            detail=tr("Par sécurité, l'adresse Ollama doit pointer vers localhost ou 127.0.0.1."),
        )

    opener = urlopen_fn if urlopen_fn is not None else urllib.request.urlopen
    req = urllib.request.Request(f"{cleaned_url}/api/tags", headers={"User-Agent": "AnkiDraft"})

    try:
        with opener(req, timeout=1.2) as resp:  # nosec B310  # boucle locale vérifiée ci-dessus
            data = json.loads(resp.read().decode("utf-8"))
        raw_models = data.get("models", []) if isinstance(data, dict) else []
        models = [str(m.get("name")) for m in raw_models if isinstance(m, dict) and m.get("name")]

        if not models:
            return OllamaDiagnostic(
                status="online_empty",
                title=tr("En ligne (0 modèle)"),
                detail=tr(
                    "Ollama est actif mais aucun modèle n'est téléchargé — modèle léger recommandé : %1",
                    _RECOMMENDED_OLLAMA_MODEL,
                ),
                recommended_command=f"ollama pull {_RECOMMENDED_OLLAMA_MODEL}",
                models=[],
            )

        return OllamaDiagnostic(
            status="online_models",
            title=tr("%1 modèle(s) détecté(s)", len(models)),
            detail=tr("Ollama est opérationnel avec %1 modèle(s) prêt(s) à l'emploi.", len(models)),
            models=models,
        )
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
        logger.debug("Diagnostic Ollama hors ligne sur %s : %s", cleaned_url, exc)
        if _is_ollama_binary_present(effective_which, extra_binary_paths):
            return OllamaDiagnostic(
                status="installed_stopped",
                title=tr("Service arrêté"),
                detail=tr("Ollama est installé sur cet ordinateur mais le service ne répond pas. Lancez l'application Ollama ou exécutez « ollama serve »."),
                recommended_command="ollama serve",
            )
        return OllamaDiagnostic(
            status="not_installed",
            title=tr("Non installé"),
            detail=tr("Ollama n'est pas détecté sur cet ordinateur. Installez-le sur ollama.com ou utilisez une clé API Cloud."),
        )


__all__ = [
    "MCPClientKey",
    "MCPClientState",
    "MCPClientStatus",
    "MCPConfigureResult",
    "OllamaDiagState",
    "OllamaDiagnostic",
    "configure_client_mcp",
    "detect_mcp_clients",
    "diagnose_ollama_connection",
    "get_client_config_path",
    "render_client_file_template",
    "render_client_snippet",
]
