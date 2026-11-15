---
title: "Glossaire Utilisateur : Les Concepts Clés Expliqués Simplement"
description: "Comprenez facilement chaque concept clé d'AnkiDraft (Wozniak, Cloze, Smart Coverage, DAG, RAG, MCP, Garde-Fou) grâce à des exemples Avant / Après."
---

AnkiDraft rassemble des outils puissants issus de l'ingénierie pédagogique et de l'IA locale. Ce glossaire traduit chaque terme technique en français simple, accompagné d'un exemple concret **Avant / Après**.

---

## 1. Atome de connaissance & 20 règles de Wozniak

Principe issu des travaux de Piotr Wozniak (créateur de SuperMemo) : une flashcard efficace ne teste **qu'une seule idée courte et sans ambiguïté** (règle d'information minimale). Le Linter d'AnkiDraft détecte automatiquement les cartes trop longues ou floues.

- **Avant** : *Recto :* « Expliquez le cycle de Krebs (étapes, enzymes limitantes, bilan énergétique en ATP/NADH/FADH2). » ➔ Trop long, impossible à noter sereinement en révision.
- **Après** : 3 cartes courtes et indépendantes : (1) « Quelle enzyme catalyse l'étape limitante du cycle de Krebs ? », (2) « Combien de NADH produit 1 tour du cycle de Krebs ? », (3) « Où se déroule le cycle de Krebs dans la cellule ? ».

---

## 2. Texte à trous (Cloze Deletion)

Format de carte (`{{c1::mot caché}}`) où l'on masque un terme clé au cœur d'une phrase pour le mémoriser directement en contexte (<kbd>Ctrl+Shift+C</kbd>).

- **Avant** : « Définition de l'osmose ? » / « Passage d'un solvant à travers une membrane semi-perméable du milieu le moins concentré vers le plus concentré. »
- **Après** : « Lors de l'osmose, le solvant traverse une membrane semi-perméable du milieu {{c1::hypotonique (moins concentré)}} vers le milieu {{c2::hypertonique (plus concentré)}}. »

---

## 3. Couverture documentaire intelligente (Smart Coverage)

Indicateur qui relie chaque carte générée à la section exacte du cours dont elle provient. Il mesure en temps réel quels chapitres de votre PDF sont déjà couverts par des cartes et lesquels restent à ficher.

- **Avant** : Relire 180 pages de cours en se demandant si l'on n'a pas oublié le sous-chapitre 3.4 lors de la création manuelle de cartes.
- **Après** : La jauge *Smart Coverage* affiche `Chapitre 3 : 82 % couvert — Section 3.4 (0 carte)` et propose de générer uniquement ce passage manquant.

---

## 4. Délimitation de portée : Écarter vs Neutraliser

Deux actions non destructives pour filtrer un document sans jamais supprimer ses pages ([Cibler les chapitres](/fr/sources/scope-and-slices/)) :
- **Écarter** : exclut temporairement un chapitre hors-programme de la génération IA.
- **Neutraliser** : retire un élément purement structurel (couverture, sommaire, remerciements) du dénominateur de la jauge *Smart Coverage*.

- **Avant** : Un livre de 300 pages incluant 30 pages d'index et de bibliographie bloque votre couverture à 90 % maximum, ou l'IA génère des cartes absurdes sur les noms d'éditeurs.
- **Après** : Index neutralisé, bibliographie écartée ➔ votre couverture reflète **100 % des chapitres utiles** et zéro carte parasite n'est créée.

---

## 5. Pipeline de génération (DAG)

Enchaînement automatisé d'étapes configurables (ex. : extraire les passages clés ➔ synthétiser en Markdown propre ➔ rédiger des cartes ➔ ajouter l'audio TTS ➔ afficher pour revue humaine).

- **Avant** : Copier un chapitre dans un chat, demander des cartes, reformater manuellement les formules LaTeX, puis générer le son carte par carte.
- **Après** : Cliquez sur **Tester le DAG** dans l'éditeur de Pipelines pour simuler la chaîne étape par étape, ou sur **Générer** dans le Studio de Création pour produire automatiquement des cartes prêtes à relire.

---

## 6. Recherche sémantique locale (RAG)

Indexation 100 % locale sur votre ordinateur permettant à l'IA de retrouver les passages pertinents d'un cours par leur **sens** (et pas seulement par mot-clé exact) avant de rédiger ou vérifier une carte.

- **Avant** : Envoyer un polycopié entier dans un prompt (lent, coûteux, et source d'erreurs ou d'hallucinations).
- **Après** : Le RAG local extrait uniquement les 3 paragraphes qui parlent réellement de la question posée et cite la page exacte.

---

## 7. Serveur MCP (Model Context Protocol)

Protocole ouvert intégré à AnkiDraft qui permet à votre assistant externe (Claude Desktop, Claude Code, Cursor, Antigravity) de lire vos cours et vos paquets localement sans clé API supplémentaire.

- **Avant** : Copier-coller des paquets texte entre Anki, votre PDF et Claude dans le navigateur.
- **Après** : Vous écrivez directement dans Claude *« Audite mon paquet Cardiologie et prépare les cartes manquantes sur le chapitre 4 »* : Claude interroge AnkiDraft en direct.

---

## 8. Garde-Fou & Lot en attente (Staged Bundle / Validation en 2 temps)

Sas de sécurité obligatoire : aucune proposition IA (création, modification, scission ou suppression) n'est écrite directement dans votre base. Tout arrive sous forme de **lot en attente** avec aperçu Avant / Après jusqu'à votre clic sur **Appliquer**.

- **Avant** : Crainte qu'un script ou une IA n'écrase accidentellement 200 cartes de votre collection.
- **Après** : Chaque proposition est inspectée visuellement ligne par ligne dans le Garde-Fou ; vous gardez le contrôle total en un clic.

---

## 9. Diagnostic de lacunes & les 3 pathologies cognitives

Analyse intelligente (`diagnose_domain_knowledge_gaps`) qui compare l'ensemble de vos paquets (tous decks confondus) à un sujet d'étude pour déceler 3 défauts :
- **Type 1 (Absence)** : notion clé présente dans le cours mais absente de vos cartes.
- **Type 2 (Non-atomicité)** : carte fourre-tout contenant plusieurs faits à scinder.
- **Type 3 (Liant bilingue)** : mélange confus de deux langues dans le même énoncé ou paire sans contexte.

- **Avant** : Découvrir la veille de l'examen que 3 notions majeures manquent ou que des cartes de médecine sont réparties dans deux paquets séparés.
- **Après** : Le diagnostic rassemble toutes les cartes liées au domaine et dresse la liste exacte des notions à ajouter ou scinder.

---

## 10. Périmètre Studio vs Périmètre Collection Anki (`.apkg` vs `.colpkg`)

AnkiDraft sépare vos ressources d'atelier (**Périmètre Studio** : PDF, transcriptions, index RAG, prompts) de vos cartes synchronisées (**Périmètre Collection Anki**).
- `.apkg` : ajoute ou met à jour un paquet ciblé.
- `.colpkg` : aligne toute la collection sur l'état exact d'Anki (supprime les cartes effacées dans Anki tout en gardant vos PDF intactes).

- **Avant** : Importer une sauvegarde Anki complète écrasait vos notes de travail ou recréait d'anciennes cartes supprimées (« cartes zombies »).
- **Après** : Le ré-import `.colpkg` synchronise votre historique Anki sans toucher à vos cours, et élimine les cartes zombies ([Cycle de Vie Distribué](/fr/guides/cycle_de_vie_distribue/)).

---

## 11. Fusion intelligente (Smart Merge)

Comparateur visuel à 3 panneaux (**Base locale**, **Résultat fusionné interactif**, **Base entrante .apkg**) inspiré des outils de développement : lors de l'import d'un `.apkg` modifié par quelqu'un d'autre, seuls les conflits réels de texte sont soumis à votre choix.

- **Avant** : Écraser à l'aveugle vos corrections personnelles ou perdre les ajouts d'un camarade lors de l'import d'un paquet partagé.
- **Après** : Vous choisissez champ par champ quelle version conserver, en préservant les médias et le planning de révision.

---

## 12. Carte sangsue (Leech)

Terme Anki désignant une carte sur laquelle vous échouez de façon répétée lors des révisions (généralement parce qu'elle est trop longue, mal formulée ou ressemble à une autre carte).

- **Avant** : Revoir la même carte frustrante 8 fois par mois sans jamais la retenir.
- **Après** : AnkiDraft repère automatiquement la sangsue grâce aux compteurs d'échecs synchronisés et vous propose de la scinder ou de la reformuler avec un indice distinctif.
