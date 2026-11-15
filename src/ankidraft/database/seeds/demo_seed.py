"""Constructeur idempotent du jeu de données « Exemple d'introduction » sans clé API."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from ankidraft.database.models import (
    AuditRecordModel,
    CardModel,
    DeckModel,
    DocumentChunkModel,
    DocumentModel,
    FolderModel,
    MediaModel,
    NoteChunkLinkModel,
    NoteModel,
    NoteTypeModel,
    NoteVersionModel,
    PipelineModel,
    SettingModel,
    StagedBundleModel,
    StagedPatchModel,
    db,
)
from ankidraft.database.note_type_catalog import BASIC_NOTE_TYPE_ALIASES
from ankidraft.repositories.deck_repository import DeckRepository
from ankidraft.repositories.document_repository import DocumentRepository
from ankidraft.services.ai.linter import normalize_linter_suggestion
from ankidraft.services.ai.staged_patch_registry import StagedPatchRegistry
from ankidraft.services.batch.models import (
    BatchGenerationConfig,
    BatchScopeSnapshot,
    BatchSourceBlock,
    BatchTaskSnapshot,
    BatchTaskStatus,
)
from ankidraft.services.cards.card_model_io import CardModelIO
from ankidraft.services.cards.media_manager import MediaManager
from ankidraft.services.cards.note_manager import NoteManager
from ankidraft.services.search.fts_service import FTSService
from ankidraft.utils.i18n import tr
from ankidraft.utils.paths import get_resource_path
from ankidraft.utils.tags import build_document_tags, parse_note_tags

logger = logging.getLogger(__name__)

INTRO_PROFILE_ID = "intro-example"
DEMO_SEED_VERSION = "1"
DEMO_DECK_NAME = "Découverte AnkiDraft::Sciences Cognitives"
DEMO_DOC_TITLE = "Sciences Cognitives — Répétition Espacée et Atomicité"
DEMO_BATCH_TASK_UID = "demo-intro-batch-review-1"

SETTING_IS_INTRO_EXAMPLE = "app/is_intro_example"
SETTING_DEMO_SEED_VERSION = "app/demo_seed_version"
SETTING_DEMO_BATCH_REVIEWED = "app/demo_batch_reviewed"
SETTING_TOUR_PROGRESS = "app/tour_progress_json"


def is_intro_example_profile() -> bool:
    """Retourne True si la base active correspond au profil Exemple d'introduction."""
    try:
        return bool(SettingModel.get_value(SETTING_IS_INTRO_EXAMPLE, False))
    except Exception as exc:
        logger.debug("Lecture de %s ignorée : %s", SETTING_IS_INTRO_EXAMPLE, exc)
        return False


def get_profile_display_name(profile_name: str) -> str:
    """Retourne le libellé affiché pour un identifiant de profil (traduit pour l'exemple)."""
    if profile_name == INTRO_PROFILE_ID:
        return tr("Exemple d'introduction")
    return profile_name


def _load_demo_resource_bytes(filename: str) -> bytes:
    """Charge un fichier ressource embarqué depuis ``src/ankidraft/resources/demo``."""
    path = get_resource_path("src", "ankidraft", "resources", "demo", filename)
    return path.read_bytes()


def _find_basic_note_type() -> NoteTypeModel | None:
    """Retourne le type de note Basique/Basic selon les alias canoniques."""
    for note_type in NoteTypeModel.select():
        if str(note_type.name).strip().casefold() in BASIC_NOTE_TYPE_ALIASES:
            return note_type
    return None


def _ensure_note_type_by_pack(name: str, pack_id: str) -> NoteTypeModel:
    """Retourne un type de note existant ou l'installe depuis le Starter Pack sans doublon."""
    existing = NoteTypeModel.get_or_none(NoteTypeModel.name == name)
    if existing is not None:
        return existing
    installed = CardModelIO.install_starter_pack(pack_id, overwrite=False)
    if installed is None:
        raise RuntimeError(f"Impossible d'installer le type de note requis '{pack_id}'.")
    return installed


def _ensure_demo_note_types() -> tuple[NoteTypeModel, NoteTypeModel, NoteTypeModel]:
    """Garantit la présence des types Basique, Cloze et Maths & KaTeX Minimal."""
    basic = _find_basic_note_type()
    if basic is None:
        from ankidraft.database.note_type_catalog import seed_default_note_types

        seed_default_note_types()
        basic = _find_basic_note_type()
    if basic is None:
        raise RuntimeError("Impossible de trouver ou d'initialiser le type de note Basique.")

    cloze = _ensure_note_type_by_pack("Texte à trous (Cloze)", "cloze")
    katex = _ensure_note_type_by_pack("Maths & KaTeX Minimal", "math_katex")
    return basic, cloze, katex


def _find_chunk_for_section(chunks: list[DocumentChunkModel], marker: str) -> DocumentChunkModel | None:
    """Retourne le premier fragment dont le fil d'Ariane contient ``marker``."""
    for chunk in chunks:
        if chunk.heading_path and marker in chunk.heading_path:
            return chunk
    return None


def _tags_for_chunk(doc: DocumentModel, chunk: DocumentChunkModel | None, extra: list[str] | None = None) -> list[str]:
    """Construit les tags canoniques de provenance pour relier la note à un fragment."""
    section_name = chunk.heading_path if chunk is not None else None
    return build_document_tags(
        doc_id=doc.id,
        doc_title=doc.title,
        section_name=section_name,
        extra_tags=extra,
    )


def _create_leech_audit(note: NoteModel, rule_broken: str, reason: str, raw_suggestion: dict[str, Any]) -> None:
    """Marque les cartes d'une note comme sangsues et enregistre un audit Wozniak non conforme."""
    CardModel.update(lapses=5, reps=12, ivl=3).where(CardModel.note == note).execute()
    active_v = note.versions.where(NoteVersionModel.is_active == True).first()  # noqa: E712
    if active_v is None:
        return
    normalized = normalize_linter_suggestion(
        raw_suggestion,
        original_content=json.loads(active_v.content),
        rule_name=rule_broken,
    )
    AuditRecordModel.create(
        note=note,
        note_version=active_v,
        is_compliant=False,
        rule_broken=rule_broken,
        reason=reason,
        suggestion=json.dumps(normalized, ensure_ascii=False),
    )


def _seed_demo_notes(
    doc: DocumentModel,
    chunks: list[DocumentChunkModel],
    deck: DeckModel,
    basic_type: NoteTypeModel,
    cloze_type: NoteTypeModel,
    katex_type: NoteTypeModel,
    diagram_filename: str,
) -> tuple[list[NoteModel], NoteModel]:
    """Crée les ~10 notes d'exemple (Basique, Cloze, KaTeX, 2 sangsues) et retourne la note cible du patch MCP."""
    c_sec1 = _find_chunk_for_section(chunks, "1.")
    c_sec2 = _find_chunk_for_section(chunks, "2.")

    created_notes: list[NoteModel] = []

    # Section 1 : Répétition espacée (couverte)
    sec1_basic_specs = [
        (
            "Quel est l'objectif central de la répétition espacée ?",
            "Planifier chaque révision juste avant le moment probable de l'oubli pour maximiser la consolidation mnésique.",
        ),
        (
            "Qu'est-ce que l'effet de test (testing effect) ?",
            "Le fait que la récupération active d'une information en mémoire renforce davantage sa rétention que la relecture passive.",
        ),
        (
            "Que montre l'évolution de la courbe d'oubli après plusieurs rappels espacés ?",
            f'Chaque rappel réussi augmente la stabilité $S$ et aplatit la courbe d\'oubli.<br><img src="{diagram_filename}" alt="Courbe de rétention">',
        ),
    ]
    for front, back in sec1_basic_specs:
        created_notes.append(
            NoteManager.create_note(
                note_type=basic_type,
                deck=deck,
                content_dict={"Recto": front, "Verso": back},
                tags=_tags_for_chunk(doc, c_sec1, ["demo", "sciences-cognitives"]),
                source="demo",
            )
        )

    # Notes Cloze liées à la section 1
    cloze_specs = [
        (
            "La {{c1::répétition espacée}} force le cerveau à effectuer un {{c2::effort de récupération actif}} plutôt qu'une relecture passive.",
            "Principe fondateur de l'apprentissage par flashcards.",
        ),
        (
            "À chaque rappel réussi, la {{c1::stabilité mnésique S}} augmente, permettant d'allonger l'{{c2::intervalle}} suivant.",
            "Lien direct avec la courbe d'Ebbinghaus.",
        ),
    ]
    for texte, extra in cloze_specs:
        created_notes.append(
            NoteManager.create_note(
                note_type=cloze_type,
                deck=deck,
                content_dict={"Texte": texte, "Remarques extra": extra},
                tags=_tags_for_chunk(doc, c_sec1, ["demo", "cloze"]),
                source="demo",
            )
        )

    # Section 2 : Modèle mathématique & KaTeX (couverte)
    # Note : le gabarit Maths & KaTeX Minimal enveloppe déjà {{Enonce_Formule}} dans $$...$$.
    katex_specs = [
        (
            "Loi exponentielle d'oubli (stabilité S, temps t)",
            r"R(t) = e^{-\frac{t}{S}}",
            r"$t \ge 0$ (temps écoulé), $S > 0$ (stabilité en jours)",
            r"Lorsque $t = S$, la probabilité de rappel vaut $e^{-1} \approx 36{,}8\%$.",
        ),
        (
            "Calcul de l'intervalle optimal I pour une rétention cible",
            r"I = -S \cdot \ln(R_{\text{cible}})",
            r"$0 < R_{\text{cible}} < 1$ (rétention visée, ex. $0{,}90$), $S > 0$",
            r"En inversant $R(I) = e^{-I/S} = R_{\text{cible}}$, on obtient $\ln(R_{\text{cible}}) = -I/S$.",
        ),
    ]
    for theorem, formula, hyp, demo in katex_specs:
        created_notes.append(
            NoteManager.create_note(
                note_type=katex_type,
                deck=deck,
                content_dict={
                    "Theoreme": theorem,
                    "Enonce_Formule": formula,
                    "Hypotheses": hyp,
                    "Demonstration": demo,
                },
                tags=_tags_for_chunk(doc, c_sec2, ["demo", "katex"]),
                source="demo",
            )
        )

    # Note cible du patch MCP en attente (Garde-Fou Two-Phase Commit)
    mcp_target_note = NoteManager.create_note(
        note_type=basic_type,
        deck=deck,
        content_dict={
            "Recto": "Que vaut la rétention cible usuelle dans les algorithmes FSRS ?",
            "Verso": "Environ 90 % (à affiner selon le compromis charge / mémorisation).",
        },
        tags=_tags_for_chunk(doc, c_sec2, ["demo"]),
        source="demo",
    )
    created_notes.append(mcp_target_note)

    # 2 cartes sangsues volontairement mal formulées + AuditRecordModel Wozniak
    leech_1 = NoteManager.create_note(
        note_type=basic_type,
        deck=deck,
        content_dict={
            "Recto": "Explique tout sur la répétition espacée, l'effet de test, la courbe d'Ebbinghaus, la stabilité S et comment régler FSRS.",
            "Verso": "La répétition espacée planifie les rappels, l'effet de test améliore la trace, S mesure la vitesse d'oubli et FSRS vise 0,90.",
        },
        tags=_tags_for_chunk(doc, c_sec1, ["demo", "leech"]),
        source="demo",
    )
    _create_leech_audit(
        leech_1,
        rule_broken="Règle 4 : Information minimale (Atomicité)",
        reason="La carte regroupe 5 concepts distincts dans une même question ; la scinder réduit la charge cognitive.",
        raw_suggestion={
            "subcards": [
                {
                    "Recto": "Que mesure la stabilité S d'une carte mémoire ?",
                    "Verso": "La durée nécessaire pour que la probabilité de rappel diminue selon la courbe d'oubli.",
                },
                {
                    "Recto": "Pourquoi l'effet de test surpasse-t-il la relecture ?",
                    "Verso": "Parce que l'effort de récupération active consolide davantage la trace mnésique.",
                },
            ]
        },
    )
    created_notes.append(leech_1)

    leech_2 = NoteManager.create_note(
        note_type=basic_type,
        deck=deck,
        content_dict={
            "Recto": "Citer sans ordre précis les facteurs qui influencent l'oubli et l'espacement.",
            "Verso": "Stabilité, difficulté intrinsèque, intervalle écoulé, qualité du rappel, interférence sémantique.",
        },
        tags=_tags_for_chunk(doc, c_sec2, ["demo", "leech"]),
        source="demo",
    )
    _create_leech_audit(
        leech_2,
        rule_broken="Règle 9 : Éviter les énumérations ouvertes",
        reason="Une énumération non ordonnée de 5 éléments génère une hésitation chronique ; privilégier un critère ciblé.",
        raw_suggestion={
            "Recto": "Quel couple de variables pilote l'évolution d'une carte après notation dans les modèles modernes ?",
            "Verso": "La difficulté intrinsèque et la stabilité mémorielle.",
        },
    )
    created_notes.append(leech_2)

    return created_notes, mcp_target_note


def _seed_pending_mcp_patch(target_note: NoteModel) -> None:
    """Crée une proposition de patch en attente dans le Garde-Fou MCP si aucune n'existe."""
    if StagedPatchModel.select().where(StagedPatchModel.status == "pending").exists():
        return
    active_v = target_note.versions.where(NoteVersionModel.is_active == True).first()  # noqa: E712
    original_dict = json.loads(active_v.content) if active_v else {}
    original_tags = parse_note_tags(target_note.tags)
    modified_tags = [*original_tags, *(["katex"] if "katex" not in original_tags else [])]
    StagedPatchRegistry.create_patch(
        patch_type="note_update",
        target_id=target_note.id,
        original_version_id=active_v.id if active_v else None,
        diff_payload={
            "title": "Préciser la formule d'intervalle optimal pour R_cible = 0,90",
            "explanation": "L'agent MCP propose d'ancrer la réponse sur la formule exacte du cours (Section 2).",
            "model_name": target_note.note_type.name,
            "original": original_dict,
            "modified": {
                "Recto": "Pour $R_{\\text{cible}} = 0{,}90$, quelle formule donne l'intervalle optimal $I$ ?",
                "Verso": "$$I = -S \\cdot \\ln(0{,}90) \\approx 0{,}105 \\cdot S$$",
            },
            "original_tags": original_tags,
            "modified_tags": modified_tags,
        },
    )


def seed_intro_example_data(media_dir: Path | None = None) -> dict[str, int]:
    """Peuple de façon idempotente le profil Exemple d'introduction sans clé API.

    Args:
        media_dir: Dossier média explicite (utile pour les tests d'isolation).

    Returns:
        Résumé des compteurs créés ou présents en base.
    """
    diagram_bytes = _load_demo_resource_bytes("intro_diagram.svg")
    course_md = _load_demo_resource_bytes("intro_course.md").decode("utf-8")

    with db.atomic():
        SettingModel.set_value(SETTING_IS_INTRO_EXAMPLE, "true", category="app")

        already_seeded = str(SettingModel.get_value(SETTING_DEMO_SEED_VERSION, "")) == DEMO_SEED_VERSION
        if already_seeded and DocumentModel.select().where(DocumentModel.title == DEMO_DOC_TITLE).exists():
            return {
                "documents": DocumentModel.select().count(),
                "decks": DeckModel.select().count(),
                "notes": NoteModel.select().count(),
                "staged_patches": StagedPatchModel.select().where(StagedPatchModel.status == "pending").count(),
            }

        basic_type, cloze_type, katex_type = _ensure_demo_note_types()

        media_mgr = MediaManager(media_dir=media_dir)
        diagram_media = media_mgr.store_media_bytes(
            diagram_bytes,
            original_name="intro_diagram.svg",
            mime_type="image/svg+xml",
        )

        doc_repo = DocumentRepository()
        existing_doc = doc_repo.get_document_by_title(DEMO_DOC_TITLE)
        doc = existing_doc or doc_repo.save_imported_document(
            title=DEMO_DOC_TITLE,
            content=course_md,
            file_type="md",
        )
        chunks = doc_repo.get_chunks_for_document(doc.id)

        deck_repo = DeckRepository()
        deck = deck_repo.get_or_create_deck_hierarchical(
            DEMO_DECK_NAME,
            description="Paquet de démonstration guidée pour découvrir Smart Coverage, Wozniak et le Garde-Fou MCP.",
        )

        notes, mcp_target_note = _seed_demo_notes(
            doc=doc,
            chunks=chunks,
            deck=deck,
            basic_type=basic_type,
            cloze_type=cloze_type,
            katex_type=katex_type,
            diagram_filename=str(diagram_media.filename),
        )
        _seed_pending_mcp_patch(mcp_target_note)

        SettingModel.set_value(SETTING_DEMO_SEED_VERSION, DEMO_SEED_VERSION, category="app")

    logger.info("Jeu de données Exemple d'introduction amorcé (%d notes).", len(notes))
    return {
        "documents": DocumentModel.select().count(),
        "decks": DeckModel.select().count(),
        "notes": NoteModel.select().count(),
        "staged_patches": StagedPatchModel.select().where(StagedPatchModel.status == "pending").count(),
    }


def reset_intro_example_data(media_dir: Path | None = None) -> dict[str, int]:
    """Purge atomiquement les données de l'exemple d'introduction puis les régénère à neuf."""
    with db.atomic():
        StagedPatchModel.delete().execute()
        StagedBundleModel.delete().execute()
        AuditRecordModel.delete().execute()
        NoteChunkLinkModel.delete().execute()
        CardModel.delete().execute()
        NoteVersionModel.delete().execute()
        NoteModel.delete().execute()
        DeckModel.delete().execute()
        DocumentChunkModel.delete().execute()
        DocumentModel.delete().execute()
        FolderModel.delete().execute()
        MediaModel.delete().execute()
        SettingModel.delete().where(
            SettingModel.key.in_(
                [
                    SETTING_DEMO_SEED_VERSION,
                    SETTING_DEMO_BATCH_REVIEWED,
                    SETTING_TOUR_PROGRESS,
                ]
            )
        ).execute()

    FTSService.rebuild_fts()

    try:
        MediaManager(media_dir=media_dir).clean_orphaned_media()
    except Exception as err:
        logger.debug("Nettoyage des médias orphelins ignoré lors de la réinitialisation : %s", err)

    return seed_intro_example_data(media_dir=media_dir)


def build_demo_batch_snapshot() -> BatchTaskSnapshot | None:
    """Construit en mémoire une tâche Batch pré-générée au statut ``REVIEW`` pour la Section 3."""
    if not is_intro_example_profile():
        return None
    if bool(SettingModel.get_value(SETTING_DEMO_BATCH_REVIEWED, False)):
        return None

    doc = DocumentModel.get_or_none(DocumentModel.title == DEMO_DOC_TITLE)
    deck = DeckModel.get_or_none(DeckModel.name == DEMO_DECK_NAME)
    note_type = _find_basic_note_type()
    if doc is None or deck is None or note_type is None:
        return None

    chunks = list(DocumentChunkModel.select().where(DocumentChunkModel.document == doc))
    sec3_chunk = _find_chunk_for_section(chunks, "3.")
    if sec3_chunk is None:
        return None

    pipeline = PipelineModel.select().order_by(PipelineModel.id.asc()).first()
    pipeline_id = int(pipeline.id) if pipeline is not None else 1
    pipeline_name = str(pipeline.name) if pipeline is not None else "Standard"

    fields_schema = tuple(json.loads(note_type.fields_schema)) if note_type.fields_schema else ("Recto", "Verso")
    templates = tuple(json.loads(note_type.templates)) if note_type.templates else ()

    block = BatchSourceBlock(
        kind="section",
        label=str(sec3_chunk.heading_path or "3. Interférence sémantique et atomicité des cartes"),
        content=str(sec3_chunk.content),
        ordinal=0,
        page_number=sec3_chunk.page_number,
        heading_path=sec3_chunk.heading_path,
        source_id=doc.id,
        chunk_id=sec3_chunk.id,
    )
    scope = BatchScopeSnapshot(
        document_id=doc.id,
        document_title=doc.title,
        selection_mode="sections",
        blocks=(block,),
        scope_title="Section 3 — Atomicité & Interférence",
    )
    config = BatchGenerationConfig(
        pipeline_id=pipeline_id,
        pipeline_name=pipeline_name,
        llm_id=0,
        llm_config={"provider": "demo", "model": "precomputed"},
        deck_id=deck.id,
        deck_name=deck.name,
        model_id=note_type.id,
        model_name=note_type.name,
        note_type_fields=fields_schema,
        note_type_templates=templates,
        auto_validation=False,
    )
    demo_cards: list[dict[str, Any]] = [
        {
            "Recto": "Pourquoi l'information minimale (atomicité) réduit-elle le risque de cartes sangsues ?",
            "Verso": "Parce qu'une question focalisée sur un fait unique limite la charge cognitive et stabilise le rappel.",
            "_source_chunk_id": sec3_chunk.id,
            "_source_heading_path": sec3_chunk.heading_path,
            "_staging_status": "pending",
        },
        {
            "Recto": "Comment prévenir l'interférence sémantique entre deux notions proches ?",
            "Verso": "En ajoutant un indice discriminant explicite et en séparant les questions plutôt que de les fusionner.",
            "_source_chunk_id": sec3_chunk.id,
            "_source_heading_path": sec3_chunk.heading_path,
            "_staging_status": "pending",
        },
    ]
    return BatchTaskSnapshot(
        task_id=DEMO_BATCH_TASK_UID,
        scope=scope,
        config=config,
        task_index=0,
        status=BatchTaskStatus.REVIEW,
        cards=demo_cards,
    )
