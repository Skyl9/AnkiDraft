import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://ankidraft.app',
  output: 'static',
  integrations: [
    starlight({
      title: {
        fr: 'AnkiDraft',
        en: 'AnkiDraft',
      },
      favicon: '/assets/icons/ankidraft.svg',
      logo: {
        src: './public/assets/icons/ankidraft.svg',
        alt: 'AnkiDraft',
      },
      description:
        "L'atelier de création et d'audit de flashcards Anki assisté par IA.",
      defaultLocale: 'en',
      locales: {
        fr: {
          label: 'Français',
          lang: 'fr',
        },
        en: {
          label: 'English',
          lang: 'en',
        },
      },
      social: {
        github: 'https://github.com/Skyl9/AnkiDraft',
      },
      head: [
        {
          tag: 'meta',
          attrs: {
            name: 'google-site-verification',
            content: 'aoyROBDMk0qbvP7PuiHXrvPdCRpsJeLWc904iaDzvBc',
          },
        },
        {
          tag: 'meta',
          attrs: {
            property: 'og:image',
            content: 'https://ankidraft.app/assets/og-banner.svg',
          },
        },
        {
          tag: 'meta',
          attrs: {
            property: 'og:image:alt',
            content: 'AnkiDraft — Studio de création et d’audit de flashcards Anki assisté par IA',
          },
        },
        {
          tag: 'meta',
          attrs: {
            name: 'twitter:image',
            content: 'https://ankidraft.app/assets/og-banner.svg',
          },
        },
      ],
      components: {
        Head: './src/components/Head.astro',
      },
      customCss: ['./src/styles/custom.css'],
      sidebar: [
        {
          label: 'Premiers pas',
          translations: { en: 'Getting Started' },
          autogenerate: { directory: 'getting-started' },
        },
        {
          label: "Parcours & Cas d'Usage",
          translations: { en: 'Workflows & Use Cases' },
          autogenerate: { directory: 'workflows' },
        },
        {
          label: 'Sources & Import',
          translations: { en: 'Sources & Import' },
          autogenerate: { directory: 'sources' },
        },
        {
          label: 'Cartes & Édition',
          translations: { en: 'Cards & Editing' },
          autogenerate: { directory: 'cards' },
        },
        {
          label: 'Synchronisation Anki',
          translations: { en: 'Anki Sync' },
          autogenerate: { directory: 'anki-sync' },
        },
        {
          label: 'Configuration IA',
          translations: { en: 'AI Setup' },
          autogenerate: { directory: 'ai-setup' },
        },
        {
          label: 'Guides & Aide',
          translations: { en: 'Guides & Help' },
          autogenerate: { directory: 'guides' },
        },
      ],
    }),
  ],
});
