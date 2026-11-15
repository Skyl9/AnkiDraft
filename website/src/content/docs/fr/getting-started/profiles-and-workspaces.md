---
title: Gérer ses Profils et sa Collection
description: Créez des profils d'étude isolés dans AnkiDraft, gérez vos bases SQLite et dossiers médias locaux et protégez vos données par sauvegarde locale.
---

AnkiDraft vous permet d'isoler complètement plusieurs collections grâce aux **profils utilisateurs**.

## 1. Pourquoi utiliser plusieurs profils ?

Chaque profil possède sa propre base de données (`ankidraft.db`), son dossier `media/`, sa zone `staging/` et ses sauvegardes `backups/`. C'est l'outil idéal pour **découper votre travail par grand paquet ou par grande période** :
- **Séparer vos fiches personnelles de vos années de cours** (ex. *Fiches personnelles / Langues*, *L1 Médecine*, *L2 Médecine*, *Préparation concours*).
- **Éviter de vous perdre dans vos documents** : les supports importés (manuels PDF, polycopiés, transcriptions vidéo) sont souvent assez volumineux. Isoler chaque grand domaine dans son propre profil garde votre bibliothèque claire, légère et facile à parcourir.

## 2. Créer, transférer ou changer de profil

1. Cliquez sur **`Profil : <nom>`** tout en bas de la barre latérale (ou utilisez le sélecteur au démarrage : *Espaces de Travail & Profils*).
2. Saisissez un nom explicite et cliquez sur **+ Créer** pour ouvrir un nouvel espace indépendant, ou sélectionnez un profil existant pour basculer.
3. AnkiDraft verrouille automatiquement le profil actif (`ProfileLockService`) afin d'éviter toute corruption si deux instances sont ouvertes.
4. Utilisez **Transférer...** pour copier sélectivement des paquets, étiquettes, types de notes ou albums d'images depuis un autre profil vers votre profil courant, ou **Supprimer cet espace** pour retirer un ancien profil inutilisé (hors profil actif verrouillé).

## 3. Sauvegardes automatiques

AnkiDraft crée automatiquement des instantanés horodatés de votre base SQLite dans le sous-dossier `backups/` du profil (jusqu'à 5 sauvegardes récentes conservées au démarrage, ainsi qu'un instantané avant chaque opération sensible comme le remplacement de la collection par une archive `.colpkg`).
