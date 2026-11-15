import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const websiteDir = path.resolve(__dirname, '..');
const docsDir = path.join(websiteDir, 'src', 'content', 'docs');
const publicDir = path.join(websiteDir, 'public');

const SITE_URL = 'https://ankidraft.app';

const CATEGORIES = [
  { dir: 'getting-started', labelFr: 'Premiers pas', labelEn: 'Getting Started' },
  { dir: 'workflows', labelFr: "Parcours & Cas d'Usage", labelEn: 'Workflows & Use Cases' },
  { dir: 'sources', labelFr: 'Sources & Import', labelEn: 'Sources & Import' },
  { dir: 'cards', labelFr: 'Cartes & Édition', labelEn: 'Cards & Editing' },
  { dir: 'anki-sync', labelFr: 'Synchronisation Anki', labelEn: 'Anki Sync' },
  { dir: 'ai-setup', labelFr: 'Configuration IA', labelEn: 'AI Setup' },
  { dir: 'guides', labelFr: 'Guides & Aide', labelEn: 'Guides & Help' },
];

function walkMarkdownFiles(dirPath) {
  if (!fs.existsSync(dirPath)) return [];
  const entries = fs.readdirSync(dirPath, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const fullPath = path.join(dirPath, entry.name);
    if (entry.isDirectory()) {
      files.push(...walkMarkdownFiles(fullPath));
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      files.push(fullPath);
    }
  }
  return files.sort();
}

function parseFrontmatter(raw) {
  const match = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/);
  if (!match) {
    return { title: '', description: '', body: raw };
  }
  const fmBlock = match[1];
  const body = match[2];
  let title = '';
  let description = '';
  for (const line of fmBlock.split(/\r?\n/)) {
    const tMatch = line.match(/^title:\s*(.+)$/);
    if (tMatch) title = tMatch[1].trim().replace(/^['"]|['"]$/g, '');
    const dMatch = line.match(/^description:\s*(.+)$/);
    if (dMatch) description = dMatch[1].trim().replace(/^['"]|['"]$/g, '');
  }
  return { title, description, body };
}

function cleanBody(body) {
  return body
    .replace(/!\[[^\]]*\]\([^)]+\)/g, '')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

function collectLocaleDocs(locale) {
  const localeDir = path.join(docsDir, locale);
  const files = walkMarkdownFiles(localeDir);
  return files.map((filePath) => {
    const relPath = path.relative(localeDir, filePath).replace(/\\/g, '/');
    const slug = relPath.replace(/\.md$/, '');
    const category = slug.includes('/') ? slug.split('/')[0] : 'other';
    const raw = fs.readFileSync(filePath, 'utf8');
    const { title, description, body } = parseFrontmatter(raw);
    return {
      locale,
      slug,
      category,
      url: `${SITE_URL}/${locale}/${slug}/`,
      title: title || slug,
      description,
      body: cleanBody(body),
    };
  });
}

function buildLlmsTxt(frDocs, enDocs) {
  const lines = [
    '# AnkiDraft',
    '',
    '> AnkiDraft is a local-first, AI-assisted flashcard creation and quality-auditing studio for the Anki ecosystem (macOS, Windows, Linux).',
    '',
    '## Value Proposition & Use Cases',
    '- Turn PDF textbooks, YouTube videos, audio lectures, and web pages into atomic Anki flashcards.',
    '- Audit and improve existing decks against Piotr Wozniak’s 20 rules of formulating knowledge.',
    '- Run 100% locally with SQLite, local RAG, and Ollama, or connect cloud LLMs (OpenAI, Anthropic, Gemini) and MCP clients (Claude Desktop, Cursor).',
    '- Export clean `.apkg` packages with stable IDs for Anki Desktop, AnkiWeb, and AnkiMobile.',
    '',
    '## Documentation (English)',
  ];

  for (const cat of CATEGORIES) {
    const docs = enDocs.filter((d) => d.category === cat.dir);
    if (docs.length === 0) continue;
    lines.push('', `### ${cat.labelEn}`);
    for (const d of docs) {
      lines.push(`- [${d.title}](${d.url}): ${d.description}`);
    }
  }

  lines.push('', '## Documentation (Français)');
  for (const cat of CATEGORIES) {
    const docs = frDocs.filter((d) => d.category === cat.dir);
    if (docs.length === 0) continue;
    lines.push('', `### ${cat.labelFr}`);
    for (const d of docs) {
      lines.push(`- [${d.title}](${d.url}): ${d.description}`);
    }
  }

  lines.push('');
  return lines.join('\n');
}

function buildLlmsFullTxt(frDocs, enDocs) {
  const sections = [
    '# AnkiDraft — Full Documentation Corpus (EN & FR)',
    '',
    'Source: https://ankidraft.app',
    '',
  ];

  for (const doc of [...enDocs, ...frDocs]) {
    sections.push('---', '');
    sections.push(`# [${doc.locale.toUpperCase()}] ${doc.title}`);
    sections.push(`URL: ${doc.url}`);
    if (doc.description) {
      sections.push(`Description: ${doc.description}`);
    }
    sections.push('', doc.body, '');
  }

  return sections.join('\n');
}

const frDocs = collectLocaleDocs('fr');
const enDocs = collectLocaleDocs('en');

fs.mkdirSync(publicDir, { recursive: true });
fs.writeFileSync(path.join(publicDir, 'llms.txt'), buildLlmsTxt(frDocs, enDocs), 'utf8');
fs.writeFileSync(path.join(publicDir, 'llms-full.txt'), buildLlmsFullTxt(frDocs, enDocs), 'utf8');
process.stdout.write(`Generated llms.txt and llms-full.txt (${enDocs.length} EN, ${frDocs.length} FR docs)\n`);
