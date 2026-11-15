---
title: Installer AnkiDraft
description: "Téléchargez, installez et mettez à jour AnkiDraft sur macOS, Windows et Linux depuis la dernière release officielle, avec vérification Ed25519."
---

AnkiDraft est une application de bureau autonome. Vous n'avez pas besoin d'installer Python ni aucun outil de développement sur votre ordinateur.

## 1. Télécharger l'installateur (dernière version)

Rendez-vous sur la [page d'accueil d'AnkiDraft](https://ankidraft.app/fr/#telecharger) ou directement sur la [dernière release GitHub](https://github.com/Skyl9/AnkiDraft/releases/latest) pour télécharger automatiquement le paquet correspondant à votre système :

| Système | Formats publiés (`releases/latest`) | Configuration requise |
| :--- | :--- | :--- |
| **macOS** | Image disque `.dmg` (Apple Silicon) ou archive `.zip` | macOS 13 (Ventura) ou supérieur, puce Apple Silicon (M1/M2/M3/M4) |
| **Windows** | Installateur `.exe` ou archive portable `.zip` | Windows 10 ou Windows 11 (64 bits) |
| **Linux** | Exécutable portable `.AppImage` ou archive `.tar.gz` | Distribution Linux 64 bits moderne (Ubuntu 22.04+, Fedora, Arch) |

## 2. Procédure par système d'exploitation

### Sur macOS
1. Double-cliquez sur l'image disque `.dmg` téléchargée depuis la [dernière release](https://github.com/Skyl9/AnkiDraft/releases/latest).
2. Faites glisser l'icône de l'application vers le dossier **Applications**.
3. Lancez l'application depuis le Launchpad ou Spotlight.

### Sur Windows
1. Si vous téléchargez l'installateur `.exe`, double-cliquez dessus et suivez l'assistant (aucun droit administrateur n'est requis pour une installation dans votre session).
2. Si vous téléchargez l'archive portable `.zip`, décompressez-la puis lancez l'exécutable principal.

### Sur Linux (AppImage)
1. Rendez le fichier `.AppImage` téléchargé exécutable :
   ```bash
   chmod +x *.AppImage
   ```
2. Lancez l'application en double-cliquant dessus ou en l'exécutant dans votre terminal.

## 3. Où sont stockées vos données ?

Toutes vos données restent localement sur votre disque dur dans le dossier `~/.ankidraft/profiles/<nom_du_profil>/` :
- `ankidraft.db` : votre base de cartes, documents et historiques.
- `media/` : les images et fichiers audio attachés à vos flashcards.

## 4. Mises à jour automatiques

AnkiDraft vérifie automatiquement la disponibilité d'une nouvelle version officielle et vérifie la signature cryptographique (Ed25519) ainsi que l'empreinte SHA-256 avant toute mise à jour.
