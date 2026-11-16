import json
import os
import stat
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest.mock import MagicMock, patch

import docx
import pymupdf
import pytest
from pptx import Presentation

import ankidraft.services.parsing.document_parser as document_parser
from ankidraft.services.parsing.document_parser import DocumentParser
from ankidraft.services.parsing.marker_service import MarkerOptions, MarkerService

pytestmark = pytest.mark.unit


def test_parse_document_file_not_found():
    """Test 1: Si le fichier n'existe pas, ça doit crasher tout de suite."""
    parser = DocumentParser()
    with pytest.raises(FileNotFoundError) as exc_info:
        parser.parse_document("fichier_fantome.pdf")

    assert "est introuvable" in str(exc_info.value)


def test_parse_document_unsupported_format(tmp_path):
    """Test 2: On passe un format exotique non géré (.xyz)."""
    fake_unsupported = tmp_path / "document.xyz"
    fake_unsupported.write_text("fake content")

    parser = DocumentParser()
    with pytest.raises(ValueError) as exc_info:
        parser.parse_document(str(fake_unsupported))

    assert "Format de fichier non supporté : .xyz" in str(exc_info.value)


def test_parse_text_file(tmp_path):
    """Test 3: Vérifie que les fichiers texte sont lus instantanément."""
    fake_md = tmp_path / "cours.md"
    fake_md.write_text("# Titre\nCeci est un cours.", encoding="utf-8")

    parser = DocumentParser()
    mock_callback = MagicMock()
    result = parser.parse_document(str(fake_md), progress_callback=mock_callback)

    assert "Ceci est un cours." in result
    mock_callback.assert_called_with("Lecture du fichier texte immédiate...")


# ==========================================
# TESTS BUREAUTIQUE (DOCX / PPTX)
# ==========================================


@pytest.mark.integration
def test_parse_docx_success(tmp_path):
    """Test 4: Vérifie l'extraction d'un Word et la traduction des styles en Markdown."""
    fake_docx_path = tmp_path / "test_cours.docx"

    # Création d'un vrai document Word en mémoire
    doc = docx.Document()
    doc.add_heading("Le Théorème de Pythagore", level=1)
    doc.add_paragraph("Voici le contenu du théorème.")
    doc.add_heading("Démonstration", level=2)
    doc.save(str(fake_docx_path))

    parser = DocumentParser()
    result = parser.parse_document(str(fake_docx_path))

    # Vérifications du Markdown généré
    assert "# Le Théorème de Pythagore" in result
    assert "Voici le contenu du théorème." in result
    assert "## Démonstration" in result


@pytest.mark.integration
def test_parse_pptx_success(tmp_path):
    """Test 5: Vérifie l'extraction d'un PowerPoint slide par slide avec balise SPLIT."""
    fake_pptx_path = tmp_path / "test_prez.pptx"

    # Création d'une vraie présentation PowerPoint en mémoire
    prs = Presentation()

    # Slide 1
    slide1 = prs.slides.add_slide(prs.slide_layouts[0])
    slide1.shapes.title.text = "Titre Slide 1"
    slide1.placeholders[1].text = "Contenu Slide 1"

    # Slide 2
    slide2 = prs.slides.add_slide(prs.slide_layouts[0])
    slide2.shapes.title.text = "Titre Slide 2"

    prs.save(str(fake_pptx_path))

    parser = DocumentParser()
    result = parser.parse_document(str(fake_pptx_path))

    # Vérifications de la structure générée
    assert "## Diapositive 1" in result
    assert "Titre Slide 1" in result
    assert "Contenu Slide 1" in result
    assert "\n\n[SPLIT]\n\n" in result
    assert "## Diapositive 2" in result
    assert "Titre Slide 2" in result


@patch("ankidraft.services.parsing.document_parser.docx", None)
def test_parse_docx_missing_lib(tmp_path):
    """Test 6: Si l'import de python-docx échoue, on doit lever une erreur claire."""
    fake_docx = tmp_path / "test.docx"
    fake_docx.touch()  # Le fichier doit exister pour passer le premier check

    parser = DocumentParser()
    with pytest.raises(RuntimeError) as exc_info:
        parser.parse_document(str(fake_docx))

    assert "python-docx n'est pas installé" in str(exc_info.value)


# ==========================================
# TESTS MARKER (PDF)
# ==========================================


@patch("ankidraft.services.parsing.document_parser.MediaManager")
@patch("ankidraft.services.parsing.document_parser.DocumentParser.get_marker_executable", return_value="/usr/local/bin/marker_single")
@patch("subprocess.Popen")
def test_parse_pdf_with_marker_success(mock_popen, mock_get_marker, MockMediaManager, tmp_path):
    """Test 7: Simule l'extraction d'un PDF avec Marker."""
    fake_pdf = tmp_path / "physique.pdf"
    fake_pdf.write_bytes(b"%PDF-1.4 mock pdf content")

    mock_media_instance = MockMediaManager.return_value
    mock_media_instance.process_extracted_folder.return_value = "Markdown final traité avec images"

    def side_effect_popen(cmd, *args, **kwargs):
        out_dir_idx = cmd.index("--output_dir") + 1
        temp_dir = Path(cmd[out_dir_idx])

        marker_folder = temp_dir / "physique"
        marker_folder.mkdir(parents=True, exist_ok=True)
        (marker_folder / "physique.md").write_text("Contenu brut", encoding="utf-8")

        mock_process = MagicMock()
        mock_process.__enter__.return_value = mock_process
        mock_process.stdout.readline.side_effect = ["Loading AI...\n", "Page 1...\n", ""]
        mock_process.returncode = 0
        return mock_process

    mock_popen.side_effect = side_effect_popen

    parser = DocumentParser()
    mock_callback = MagicMock()
    result = parser.parse_document(str(fake_pdf), progress_callback=mock_callback)

    assert result == "Markdown final traité avec images"
    mock_callback.assert_any_call("Loading AI...")


def test_marker_executable_is_found_in_bundle_resources(tmp_path, monkeypatch):
    """Le build autonome peut embarquer marker_single dans Contents/Resources/tools."""
    executable = tmp_path / "Contents" / "MacOS" / "AnkiForge"
    marker = tmp_path / "Contents" / "Resources" / "tools" / "marker_single"
    executable.parent.mkdir(parents=True)
    marker.parent.mkdir(parents=True)
    executable.write_text("", encoding="utf-8")
    marker.write_text("#!/bin/sh", encoding="utf-8")
    marker.chmod(marker.stat().st_mode | stat.S_IXUSR)

    monkeypatch.setattr(document_parser.sys, "executable", str(executable))
    monkeypatch.setattr(document_parser.shutil, "which", lambda _: None)
    monkeypatch.setattr("ankidraft.utils.paths.get_tools_search_dirs", lambda: [])

    assert DocumentParser.get_marker_executable() == str(marker)


def test_marker_executable_is_found_in_persistent_venv(tmp_path, monkeypatch):
    """Le Marker installé depuis une application packagée est résolu dans ~/.ankidraft/tools."""
    # Le nom et le dossier du binaire dépendent de la plateforme (``bin/marker_single``
    # sous POSIX, ``Scripts/marker_single.exe`` sous Windows) : le service fait foi.
    venv_dir = tmp_path / "tools" / "marker" / "venv"
    marker = MarkerService._venv_executable(venv_dir)
    marker.parent.mkdir(parents=True)
    marker.write_text("#!/bin/sh", encoding="utf-8")
    marker.chmod(marker.stat().st_mode | stat.S_IXUSR)

    monkeypatch.setattr("ankidraft.services.parsing.marker_service.get_tools_search_dirs", lambda: [tmp_path / "tools"])
    monkeypatch.setattr(MarkerService, "_is_venv_compatible", lambda _: True)
    monkeypatch.setattr(document_parser.shutil, "which", lambda _: None)
    monkeypatch.setattr(document_parser.sys, "executable", str(tmp_path / "app"))

    assert MarkerService.get_executable() == marker


def test_marker_installer_uses_external_python_and_persistent_venv(tmp_path, monkeypatch):
    commands: list[list[str]] = []
    tools_dir = tmp_path / "tools"
    monkeypatch.setattr("ankidraft.services.parsing.marker_service.get_tools_search_dirs", lambda: [tools_dir])
    monkeypatch.setattr(MarkerService, "_find_python", lambda: "/usr/local/bin/python3")
    monkeypatch.setattr(MarkerService, "_find_uv", lambda: None)
    monkeypatch.setattr(MarkerService, "_is_python_compatible", lambda _: True)

    class FakeProcess:
        stdout = ()

        def wait(self):
            return 0

    # Disposition du venv décrite par le service : ``bin/python``/``marker_single``
    # sous POSIX, ``Scripts/python.exe``/``marker_single.exe`` sous Windows.
    venv_dir = tools_dir / "marker" / "venv"
    python_path = MarkerService._venv_python(venv_dir)
    marker_path = MarkerService._venv_executable(venv_dir)

    def fake_popen(command, **_):
        commands.append(command)
        python_path.parent.mkdir(parents=True, exist_ok=True)
        python_path.write_text("#!/bin/sh")
        marker_path.write_text("#!/bin/sh")
        marker_path.chmod(marker_path.stat().st_mode | stat.S_IXUSR)
        return FakeProcess()

    monkeypatch.setattr("ankidraft.services.parsing.marker_service.subprocess.Popen", fake_popen)
    executable = marker_path

    assert MarkerService.install() == executable
    assert commands[0][:3] == ["/usr/local/bin/python3", "-m", "venv"]
    assert commands[1][1:4] == ["-m", "pip", "install"]


@patch("ankidraft.services.parsing.document_parser.DocumentParser.get_marker_executable", return_value="/usr/local/bin/marker_single")
@patch("subprocess.Popen")
def test_parse_pdf_marker_crash(mock_popen, mock_get_marker, tmp_path):
    """Test 8: Vérifie ce qui se passe si l'IA plante."""
    fake_pdf = tmp_path / "crash.pdf"
    fake_pdf.write_bytes(b"%PDF")

    def side_effect_popen(*args, **kwargs):
        mock_process = MagicMock()
        mock_process.__enter__.return_value = mock_process
        mock_process.stdout.readline.side_effect = ["Fatal Error", ""]
        mock_process.returncode = 1
        return mock_process

    mock_popen.side_effect = side_effect_popen

    parser = DocumentParser()
    with pytest.raises(RuntimeError) as exc_info:
        parser.parse_document(str(fake_pdf))

    assert "Marker a échoué avec le code erreur 1" in str(exc_info.value)


@patch("ankidraft.services.parsing.document_parser.DocumentParser.get_marker_executable", return_value="/usr/local/bin/marker_single")
@patch("subprocess.Popen")
def test_parse_pdf_no_md_generated(mock_popen, mock_get_marker, tmp_path):
    """Test 9: L'IA dit qu'elle a fini, mais le .md n'est pas là !"""
    fake_pdf = tmp_path / "vide.pdf"
    fake_pdf.write_bytes(b"%PDF")

    def side_effect_popen(*args, **kwargs):
        mock_process = MagicMock()
        mock_process.__enter__.return_value = mock_process
        mock_process.stdout.readline.side_effect = [""]
        mock_process.returncode = 0
        return mock_process

    mock_popen.side_effect = side_effect_popen

    parser = DocumentParser()
    with pytest.raises(FileNotFoundError) as exc_info:
        parser.parse_document(str(fake_pdf))

    assert "Marker n'a pas généré de fichier .md" in str(exc_info.value)


@patch("ankidraft.services.parsing.document_parser.DocumentParser.get_marker_executable", return_value=None)
@patch("pypdf.PdfReader")
def test_parse_pdf_pypdf_fallback_success(mock_reader_cls, mock_get_marker, tmp_path):
    """Test 10: Vérifie le fallback pypdf si Marker n'est pas installé."""
    fake_pdf = tmp_path / "simple.pdf"
    fake_pdf.write_bytes(b"%PDF-1.4 simple")

    mock_page1 = MagicMock()
    mock_page1.extract_text.return_value = "Première page de cours"
    mock_page2 = MagicMock()
    mock_page2.extract_text.return_value = "Deuxième page de cours"

    mock_reader = MagicMock()
    mock_reader.pages = [mock_page1, mock_page2]
    mock_reader_cls.return_value = mock_reader

    parser = DocumentParser()
    mock_callback = MagicMock()
    result = parser.parse_document(str(fake_pdf), progress_callback=mock_callback)

    assert "## Page 1" in result
    assert "Première page de cours" in result
    assert "## Page 2" in result
    assert "Deuxième page de cours" in result
    mock_callback.assert_any_call("Extraction PDF native en cours (pypdf)...")


# ==========================================
# TESTS NOTEBOOKS JUPYTER (.ipynb)
# ==========================================


def _build_notebook(cells):
    """Construit un dictionnaire notebook Jupyter v4 minimal."""
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {},
        "cells": cells,
    }


def test_parse_ipynb_success(tmp_path):
    """Un notebook mixte (markdown + code) est converti en Markdown structuré."""
    notebook = _build_notebook(
        [
            {"cell_type": "markdown", "metadata": {}, "source": "# Les boucles Python\n\nLe `for` en Python."},
            {
                "cell_type": "code",
                "metadata": {},
                "execution_count": 3,
                "source": ["total = 0\n", "for i in range(4):\n", "    total += i\n", "print(total)"],
                "outputs": [
                    {"output_type": "stream", "name": "stdout", "text": ["6\n"]},
                    {"output_type": "execute_result", "data": {"text/plain": ["6"]}, "metadata": {}, "execution_count": 3},
                ],
            },
            {"cell_type": "code", "metadata": {}, "execution_count": None, "source": "def carre(x):\n    return x**2", "outputs": []},
        ]
    )

    fake_ipynb = tmp_path / "cours.ipynb"
    fake_ipynb.write_text(json.dumps(notebook), encoding="utf-8")

    parser = DocumentParser()
    result = parser.parse_document(str(fake_ipynb))

    assert "# Les boucles Python" in result
    assert "## Cellule 2 (exécution #3)" in result
    assert "```python" in result
    assert "for i in range(4):" in result
    assert "### Résultat" in result
    assert "> 6" in result
    assert "## Cellule 3" in result
    assert "def carre(x):" in result


def test_parse_ipynb_invalid_json(tmp_path):
    """Un notebook non-JSON doit lever une erreur claire."""
    fake_ipynb = tmp_path / "casse.ipynb"
    fake_ipynb.write_text("{pas du json", encoding="utf-8")

    parser = DocumentParser()
    with pytest.raises(ValueError) as exc_info:
        parser.parse_document(str(fake_ipynb))

    assert "JSON invalide" in str(exc_info.value)


def test_parse_ipynb_non_notebook_json(tmp_path):
    """Un JSON valide mais sans liste de cellules n'est pas un notebook."""
    fake_ipynb = tmp_path / "faux.ipynb"
    fake_ipynb.write_text('{"title": "nimporte quoi"}', encoding="utf-8")

    parser = DocumentParser()
    with pytest.raises(ValueError) as exc_info:
        parser.parse_document(str(fake_ipynb))

    assert "notebook Jupyter valide" in str(exc_info.value)


def test_parse_ipynb_skips_images_and_errors(tmp_path):
    """Les sorties non textuelles sont ignorées, les erreurs sont restituées."""
    notebook = _build_notebook(
        [
            {
                "cell_type": "code",
                "metadata": {},
                "execution_count": 1,
                "source": "1/0",
                "outputs": [
                    {"output_type": "display_data", "data": {"image/png": "fake", "text/plain": ["IGNOREE"]}, "metadata": {}},
                    {"output_type": "error", "ename": "ZeroDivisionError", "evalue": "division by zero", "traceback": [], "metadata": {}},
                ],
            }
        ]
    )

    fake_ipynb = tmp_path / "erreur.ipynb"
    fake_ipynb.write_text(json.dumps(notebook), encoding="utf-8")

    parser = DocumentParser()
    result = parser.parse_document(str(fake_ipynb))

    assert "ZeroDivisionError" in result
    assert "division by zero" in result
    assert "IGNOREE" not in result


# ==========================================
# TESTS CODE PYTHON (.py)
# ==========================================


def test_parse_python_success(tmp_path):
    """Un fichier .py structuré est converti en Markdown organisé par AST, code préservé."""
    fake_py = tmp_path / "collections.py"
    fake_py.write_text(
        '"""Outils de statistiques."""\n'
        "\n"
        "def moyenne(valeurs):\n"
        '    """Calcule la moyenne."""\n'
        "    return sum(valeurs) / len(valeurs)\n"
        "\n"
        "class Statistiques:\n"
        '    """Agrégateur statistique."""\n'
        "\n"
        "    def __init__(self, valeurs):\n"
        "        self.valeurs = valeurs\n"
        "\n"
        "    async def etendue(self):\n"
        '        """Retourne l\'étendue."""\n'
        "        return max(self.valeurs) - min(self.valeurs)\n",
        encoding="utf-8",
    )

    parser = DocumentParser()
    result = parser.parse_document(str(fake_py))

    assert "Outils de statistiques." in result
    assert "### def moyenne" in result
    assert "Calcule la moyenne." in result
    assert "return sum(valeurs) / len(valeurs)" in result
    assert "## class Statistiques" in result
    assert "Agrégateur statistique." in result
    assert "### def __init__" in result
    assert "async def etendue" in result
    assert "return max(self.valeurs) - min(self.valeurs)" in result


def test_parse_python_syntax_error_fallback(tmp_path):
    """Un .py invalide est conservé en un seul bloc de code sans crasher."""
    fake_py = tmp_path / "corrompu.py"
    fake_py.write_text("def casse(:\n    pass", encoding="utf-8")

    parser = DocumentParser()
    result = parser.parse_document(str(fake_py))

    assert "```python" in result
    assert "def casse(:" in result


def test_parse_python_plain_module_keeps_code(tmp_path):
    """Un module sans classe ni fonction reste disponible en bloc de code."""
    fake_py = tmp_path / "script.py"
    fake_py.write_text("IMPORT_MATHS = True\n\nprint('hello')\n", encoding="utf-8")

    parser = DocumentParser()
    result = parser.parse_document(str(fake_py))

    assert "```python" in result
    assert "IMPORT_MATHS = True" in result
    assert "print('hello')" in result


# ==========================================
# TESTS INJECTION MARKER_OPTIONS
# ==========================================


@patch("ankidraft.services.parsing.document_parser.MediaManager")
@patch("ankidraft.services.parsing.document_parser.DocumentParser.get_marker_executable", return_value="/usr/local/bin/marker_single")
@patch("subprocess.Popen")
def test_parse_pdf_with_marker_options_explicit(mock_popen, mock_get_marker, MockMediaManager, tmp_path):
    """Vérifie la transmission fidèle des options explicites MarkerOptions à la CLI et à l'environnement."""
    fake_pdf = tmp_path / "cours_opt.pdf"
    fake_pdf.write_bytes(b"%PDF-1.4 mock pdf content")

    mock_media_instance = MockMediaManager.return_value
    mock_media_instance.process_extracted_folder.return_value = "Markdown avec options explicites"

    captured_calls: list[dict] = []

    def side_effect_popen(cmd, *args, **kwargs):
        captured_calls.append({"cmd": cmd, "kwargs": kwargs})
        out_dir_idx = cmd.index("--output_dir") + 1
        temp_dir = Path(cmd[out_dir_idx])
        marker_folder = temp_dir / "cours_opt"
        marker_folder.mkdir(parents=True, exist_ok=True)
        (marker_folder / "cours_opt.md").write_text("Contenu brut", encoding="utf-8")

        mock_process = MagicMock()
        mock_process.__enter__.return_value = mock_process
        mock_process.stdout.readline.side_effect = [""]
        mock_process.returncode = 0
        return mock_process

    mock_popen.side_effect = side_effect_popen

    options = MarkerOptions(
        page_range="2-5",
        force_ocr=True,
        highres_image_dpi=240,
        device="cpu",
        extra_cli_args=["--languages", "fr,en"],
    )

    parser = DocumentParser()
    result = parser.parse_document(str(fake_pdf), marker_options=options)

    assert result == "Markdown avec options explicites"
    assert len(captured_calls) == 1

    call = captured_calls[0]
    cmd = call["cmd"]
    env = call["kwargs"].get("env", {})

    # Vérification des arguments CLI
    assert cmd[0] == "/usr/local/bin/marker_single"
    assert cmd[1] == str(fake_pdf)
    assert "--output_dir" in cmd
    assert "--paginate_output" in cmd
    assert "--page_range" in cmd
    assert cmd[cmd.index("--page_range") + 1] == "2-5"
    assert "--force_ocr" in cmd
    assert "--highres_image_dpi" in cmd
    assert cmd[cmd.index("--highres_image_dpi") + 1] == "240"
    assert "--languages" in cmd
    assert cmd[cmd.index("--languages") + 1] == "fr,en"

    # Vérification de l'environnement matériel injecté
    assert env.get("TORCH_DEVICE") == "cpu"


@patch("ankidraft.services.parsing.document_parser.MediaManager")
@patch("ankidraft.services.parsing.document_parser.DocumentParser.get_marker_executable", return_value="/usr/local/bin/marker_single")
@patch("subprocess.Popen")
def test_parse_pdf_with_marker_options_from_env(mock_popen, mock_get_marker, MockMediaManager, tmp_path, monkeypatch):
    """Vérifie que les variables ANKIFORGE_MARKER_* sont résolues automatiquement par défaut."""
    fake_pdf = tmp_path / "cours_env.pdf"
    fake_pdf.write_bytes(b"%PDF-1.4 mock pdf content")

    monkeypatch.setenv("ANKIFORGE_MARKER_PAGE_RANGE", "1-3")
    monkeypatch.setenv("ANKIFORGE_MARKER_DISABLE_OCR", "1")
    monkeypatch.setenv("ANKIFORGE_MARKER_DEVICE", "mps")

    mock_media_instance = MockMediaManager.return_value
    mock_media_instance.process_extracted_folder.return_value = "Markdown depuis variables env"

    captured_calls: list[dict] = []

    def side_effect_popen(cmd, *args, **kwargs):
        captured_calls.append({"cmd": cmd, "kwargs": kwargs})
        out_dir_idx = cmd.index("--output_dir") + 1
        temp_dir = Path(cmd[out_dir_idx])
        marker_folder = temp_dir / "cours_env"
        marker_folder.mkdir(parents=True, exist_ok=True)
        (marker_folder / "cours_env.md").write_text("Contenu brut", encoding="utf-8")

        mock_process = MagicMock()
        mock_process.__enter__.return_value = mock_process
        mock_process.stdout.readline.side_effect = [""]
        mock_process.returncode = 0
        return mock_process

    mock_popen.side_effect = side_effect_popen

    parser = DocumentParser()
    result = parser.parse_document(str(fake_pdf))  # marker_options=None -> résolu via from_env()

    assert result == "Markdown depuis variables env"
    assert len(captured_calls) == 1

    call = captured_calls[0]
    cmd = call["cmd"]
    env = call["kwargs"].get("env", {})

    assert "--page_range" in cmd
    assert cmd[cmd.index("--page_range") + 1] == "1-3"
    assert "--disable_ocr" in cmd
    assert env.get("TORCH_DEVICE") == "mps"


@patch("ankidraft.services.parsing.document_parser.MediaManager")
@patch("ankidraft.services.parsing.document_parser.DocumentParser.get_marker_executable", return_value="/usr/local/bin/marker_single")
@patch("subprocess.Popen")
def test_parse_pdf_with_marker_default_retrocompatibility(mock_popen, mock_get_marker, MockMediaManager, tmp_path, monkeypatch):
    """Vérifie la rétrocompatibilité stricte et l'injection par défaut de TORCH_DEVICE sans option explicite."""
    fake_pdf = tmp_path / "cours_retro.pdf"
    fake_pdf.write_bytes(b"%PDF-1.4 mock pdf content")

    # Nettoyage préventif des variables ANKIFORGE_MARKER_*
    for key in list(os.environ.keys()):
        if key.startswith("ANKIFORGE_MARKER_"):
            monkeypatch.delenv(key, raising=False)

    mock_media_instance = MockMediaManager.return_value
    mock_media_instance.process_extracted_folder.return_value = "Markdown retro"

    captured_calls: list[dict] = []

    def side_effect_popen(cmd, *args, **kwargs):
        captured_calls.append({"cmd": cmd, "kwargs": kwargs})
        out_dir_idx = cmd.index("--output_dir") + 1
        temp_dir = Path(cmd[out_dir_idx])
        marker_folder = temp_dir / "cours_retro"
        marker_folder.mkdir(parents=True, exist_ok=True)
        (marker_folder / "cours_retro.md").write_text("Contenu brut", encoding="utf-8")

        mock_process = MagicMock()
        mock_process.__enter__.return_value = mock_process
        mock_process.stdout.readline.side_effect = [""]
        mock_process.returncode = 0
        return mock_process

    mock_popen.side_effect = side_effect_popen

    parser = DocumentParser()
    result = parser.parse_document(str(fake_pdf))

    assert result == "Markdown retro"
    assert len(captured_calls) == 1

    call = captured_calls[0]
    cmd = call["cmd"]
    env = call["kwargs"].get("env", {})

    assert cmd[0] == "/usr/local/bin/marker_single"
    assert cmd[1] == str(fake_pdf)
    assert "--output_dir" in cmd
    assert "--paginate_output" in cmd
    assert "--page_range" not in cmd
    assert "--force_ocr" not in cmd
    assert "--disable_ocr" not in cmd
    assert "TORCH_DEVICE" in env


# ==========================================
# TESTS PYMUPDF NATIF (PDF)
# ==========================================


def _make_png_bytes(width: int, height: int) -> bytes:
    """Construit des octets PNG synthétiques aux dimensions exactes via PyMuPDF."""
    pix = pymupdf.Pixmap(pymupdf.csRGB, pymupdf.IRect(0, 0, width, height), False)
    pix.clear_with(200)
    return bytes(pix.tobytes("png"))


def test_parse_pdf_pymupdf_text_and_admissible_figures_interleaved(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Extrait texte et figures admissibles d'un vrai PDF synthétique en les triant selon y0."""
    pdf_path = tmp_path / "cours_figures.pdf"
    doc = pymupdf.open()
    page1 = doc.new_page(width=595, height=842)
    page1.insert_text((50, 60), "Titre introductif haut de page")
    page1.insert_image(pymupdf.Rect(50, 140, 250, 340), stream=_make_png_bytes(200, 200))
    page1.insert_image(pymupdf.Rect(50, 360, 70, 380), stream=_make_png_bytes(20, 20))
    page1.insert_text((50, 460), "Paragraphe sous la figure")

    page2 = doc.new_page(width=595, height=842)
    page2.insert_text((50, 80), "Contenu de la page deux")
    doc.save(str(pdf_path))
    doc.close()

    stored_calls: list[tuple[bytes, str, str]] = []
    mock_media_manager = MagicMock()

    def _fake_store(data: bytes, original_name: str, mime_type: str | None = None) -> SimpleNamespace:
        stored_calls.append((data, original_name, str(mime_type)))
        return SimpleNamespace(filename=f"hash_{len(stored_calls)}.png")

    mock_media_manager.store_media_bytes.side_effect = _fake_store
    monkeypatch.setattr(DocumentParser, "get_marker_executable", staticmethod(lambda: None))

    progress_messages: list[str] = []
    parser = DocumentParser(media_manager=mock_media_manager)
    result = parser.parse_document(str(pdf_path), progress_callback=progress_messages.append)

    assert "## Page 1" in result
    assert "## Page 2" in result
    assert "\n\n[SPLIT]\n\n" in result
    assert "![Figure 1 (Page 1)](hash_1.png)" in result
    assert "<!-- media_bboxes:" in result
    assert len(stored_calls) == 1
    assert stored_calls[0][1] == "page_1_figure_1.png"

    # Vérifie l'ordre vertical y0 : titre -> figure -> paragraphe
    idx_top = result.index("Titre introductif haut de page")
    idx_fig = result.index("![Figure 1 (Page 1)](hash_1.png)")
    idx_bottom = result.index("Paragraphe sous la figure")
    assert idx_top < idx_fig < idx_bottom

    assert "Extraction PDF native en cours (PyMuPDF)..." in progress_messages
    assert "Lecture de la page 1 / 2..." in progress_messages
    assert "Lecture de la page 2 / 2..." in progress_messages


def test_parse_pdf_pymupdf_cancelled_raises_interrupted(tmp_path: Path) -> None:
    """Lève InterruptedError immédiatement si check_cancel retourne True."""
    pdf_path = tmp_path / "cancel.pdf"
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Texte")
    doc.save(str(pdf_path))
    doc.close()

    parser = DocumentParser(media_manager=MagicMock())
    with pytest.raises(InterruptedError, match="annulée"):
        parser._parse_pdf_with_pymupdf(pdf_path, check_cancel=lambda: True)


def test_parse_pdf_pymupdf_empty_raises_value_error(tmp_path: Path) -> None:
    """Lève ValueError si le PDF ne contient ni texte ni figure exploitable."""
    pdf_path = tmp_path / "vide.pdf"
    doc = pymupdf.open()
    doc.new_page()
    doc.save(str(pdf_path))
    doc.close()

    parser = DocumentParser(media_manager=MagicMock())
    with pytest.raises(ValueError, match="Aucun texte extractible"):
        parser._parse_pdf_with_pymupdf(pdf_path)


def test_parse_pdf_pymupdf_missing_fitz_raises_runtime_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Lève RuntimeError explicite lorsque PyMuPDF (fitz) n'est pas disponible."""
    monkeypatch.setattr(document_parser, "fitz", None)
    parser = DocumentParser(media_manager=MagicMock())

    with pytest.raises(RuntimeError, match="pymupdf"):
        parser._parse_pdf_with_pymupdf(tmp_path / "absent.pdf")


def test_parse_pdf_pymupdf_handles_text_fallback_and_image_edge_cases(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Couvre les repli texte simple, erreurs d'extraction d'image, bboxes invalides et close() défaillant."""

    class _FallbackTextPage:
        def get_text(self, mode: str | None = None) -> Any:
            if mode == "blocks":
                raise RuntimeError("blocks error")
            return "Texte issu du repli simple"

        def get_image_info(self, xrefs: bool = True) -> list[dict[str, Any]]:
            raise RuntimeError("image info error")

    class _ImageEdgeCasePage:
        def get_text(self, mode: str | None = None) -> list[tuple[Any, ...]]:
            return [
                (0, 10, 100, 20, "Bloc texte normal", 0, 0),
                (0, 20, 100, 30, "   ", 1, 0),
                (0, 30, 100, 40, "Bloc image ignoré", 2, 1),
            ]

        def get_image_info(self, xrefs: bool = True) -> list[dict[str, Any]]:
            return [
                {"width": 10, "height": 10, "xref": 1},  # Trop petite
                {"width": 200, "height": 200, "xref": None},  # Sans xref
                {"width": 200, "height": 200, "xref": 2},  # extract_image lève une erreur
                {"width": 200, "height": 200, "xref": 3},  # extract_image sans octets
                {"width": 200, "height": 200, "xref": 4, "bbox": ("bad", "bbox")},  # store_media_bytes -> None
                {"width": 200, "height": 200, "xref": 5, "bbox": ("bad", "y")},  # bbox non numérique mais stocké
                {"width": 200, "height": 200, "xref": 6, "bbox": (10, 25, 210, 225)},  # JPEG valide sans filename puis valide
            ]

    class _FakeDoc:
        def __init__(self) -> None:
            self._pages = [_FallbackTextPage(), _ImageEdgeCasePage()]

        def __len__(self) -> int:
            return len(self._pages)

        def __iter__(self) -> Any:
            return iter(self._pages)

        def extract_image(self, xref: int) -> dict[str, Any] | None:
            if xref == 2:
                raise OSError("corrupted xref")
            if xref == 3:
                return {"ext": "png", "image": b""}
            if xref == 4:
                return {"ext": "png", "image": b"img4"}
            if xref == 5:
                return {"ext": "jpg", "image": b"img5"}
            if xref == 6:
                return {"ext": "jpg", "image": b"img6"}
            return None

        def close(self) -> None:
            raise OSError("close failed")

    fake_fitz = SimpleNamespace(open=lambda _path: _FakeDoc())
    monkeypatch.setattr(document_parser, "fitz", fake_fitz)

    mock_media_manager = MagicMock()
    mock_media_manager.store_media_bytes.side_effect = [
        None,
        SimpleNamespace(filename="fig_bad_bbox.jpg"),
        SimpleNamespace(filename="fig_valid.jpg"),
    ]

    parser = DocumentParser(media_manager=mock_media_manager)
    result = parser._parse_pdf_with_pymupdf(tmp_path / "edge.pdf")

    assert "Texte issu du repli simple" in result
    assert "Bloc texte normal" in result
    assert "Bloc image ignoré" not in result
    assert "![Figure 1 (Page 2)](fig_bad_bbox.jpg)" in result
    assert "![Figure 2 (Page 2)](fig_valid.jpg)" in result
    assert '"fig_valid.jpg": "10.0,25.0,210.0,225.0"' in result
    assert mock_media_manager.store_media_bytes.call_args_list[1].kwargs["mime_type"] == "image/jpeg"
