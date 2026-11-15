---
title: Importer des Pages Web et Articles
description: Capturez le contenu utile d'un article en ligne ou d'une documentation web en Markdown propre sans publicités ni menus superflus sur votre poste.
---

Vous révisez à partir d'articles encyclopédiques, de blogs techniques ou de cours publiés en ligne ? L'importateur web d'AnkiDraft extrait uniquement le contenu pédagogique pertinent.

## 1. Capturer une ou plusieurs pages web

1. Dans **My Documents** (<kbd>Alt+7</kbd>), cliquez sur l'icône **Importer depuis le Web / YouTube** (ou sur **Importer depuis le Web** dans l'état vide).
2. Collez une ou plusieurs URLs (`https://...`, **une par ligne**) puis choisissez le dossier de destination.
3. Ajustez les options selon l'article :
   - **Télécharger les images** : enregistre les illustrations dans les médias du profil et les lie dans le Markdown.
   - **Fusionner les articles multi-pages** : suit automatiquement les liens `page suivante` (`rel=next`, de 1 à 10 pages, 3 par défaut).
   - **Rendu JavaScript si page dynamique (SPA)** : utilise le moteur Web intégré (sans cookies persistants) lorsque la page charge son texte en JavaScript.
4. Prévisualisez le contenu nettoyé (menus, bandeaux et publicités supprimés, formules MathML converties en LaTeX, extraction dédiée pour Wikipédia) puis importez.

## 2. Sites protégés et limites techniques

- AnkiDraft applique une limite de **10 Mo** par page et signale clairement les blocages rencontrés (authentification `HTTP 401`, paywall `HTTP 402`, protection anti-bot / Cloudflare `HTTP 403`).
- Les cours hébergés derrière un portail universitaire authentifié ou un paywall doivent être enregistrés localement (ex. *Imprimer en PDF* depuis votre navigateur) puis importés comme PDF dans **My Documents**.
