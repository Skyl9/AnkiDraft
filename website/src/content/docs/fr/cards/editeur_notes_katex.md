---
title: Éditeur de Notes, Formules KaTeX et Textes à Trous
description: Rédigez et mettez en forme vos flashcards avec aperçu mathématique KaTeX en direct, occlusions Cloze, médias et historique complet des révisions.
---

La vue **Édition & Navigateur** (<kbd>Alt+3</kbd>) réunit la navigation dans vos paquets et l'édition complète de vos notes avec prévisualisation Anki en temps réel (<kbd>Ctrl+P</kbd> pour afficher/masquer l'aperçu, <kbd>Ctrl+Alt+T</kbd> pour basculer entre **📝 Notes** et **🗂️ Cartes**).

## 1. Écrire des formules mathématiques et chimiques (KaTeX)

AnkiDraft affiche instantanément vos équations LaTeX sans attendre l'export vers Anki :
- **Insertion rapide** : utilisez le bouton **Formule KaTeX** de la barre d'outils ou le raccourci <kbd>Ctrl+M</kbd>.
- **Formule en ligne** : entourez votre expression de `\( ... \)` ou `$ ... $` (ex. `$E = mc^2$`).
- **Formule en bloc centré** : utilisez `\[ ... \]` ou `$$ ... $$`.
- **Autocomplétion LaTeX** : tapez `\` suivi des premières lettres d'un symbole (`\alpha`, `\frac`, `\sum`) pour afficher la liste des commandes disponibles.

## 2. Textes à trous (Cloze), médias et barre personnalisable

Les cartes à trous sont idéales pour mémoriser une définition précise ou un terme clé :
1. Sélectionnez le mot ou l'expression à masquer dans votre texte.
2. Cliquez sur **Trou Cloze** ou appuyez sur <kbd>Ctrl+Shift+C</kbd> pour insérer automatiquement l'indice suivant `{{c1::votre texte}}` (avec indice optionnel `{{c1::réponse::indice}}`).
3. La barre d'outils propose aussi la mise en forme HTML, les blocs de code, les liens (<kbd>Ctrl+K</kbd>), l'insertion d'images (ou glisser-déposer direct dans un champ) et la personnalisation des boutons via `...`.
4. Chaque champ possède également un bouton **TTS** pour générer sa prononciation audio, et les notes liées à un cours affichent le bouton **Voir le cours ➔** pour rouvrir le passage source exact.

:::tip[Schémas et diagrammes interactifs]
Pour masquer directement les légendes d'une figure médicale ou technique, passez par le [Masquage d'Images Intelligent (Image Occlusion IA)](/fr/cards/image-occlusion/).
:::

## 3. Édition groupée, drapeaux et actions en masse

- **Édition groupée atomique** (<kbd>Ctrl+Shift+E</kbd>) & **Rechercher / remplacer ciblé** (<kbd>Ctrl+Alt+F</kbd>) : ajoutez/retirez des tags (tout en préservant les tags de provenance `source:`, `section:`, `page:`) ou modifiez un champ sur tout un lot (*Remplacer par*, *Suffixer*, *Préfixer*, *Rechercher et remplacer*).
- **Actions rapides de navigation & tri** : posez des drapeaux Anki (<kbd>Ctrl+0</kbd> à <kbd>Ctrl+7</kbd>), suspendez/réactivez (<kbd>Ctrl+J</kbd> ou <kbd>!</kbd>), déplacez vers un paquet (<kbd>Ctrl+D</kbd>), changez de type de note (<kbd>Ctrl+Shift+M</kbd>), nettoyez vos tags (**Hygiène et fusion des tags…**) ou lancez l'**Édition groupée IA** / **Auto-Tagging** sur une sélection.

## 4. Historique de révision (Time Machine)

Vous avez modifié une carte par erreur ? Chaque enregistrement (<kbd>Ctrl+S</kbd>) conserve une version dans l'historique local de la note : cliquez sur **Historique** ou appuyez sur <kbd>Ctrl+H</kbd> pour ouvrir la **Machine à Remonter le Temps**, comparer et restaurer une version antérieure en un clic.
