export interface ReleaseAssetInfo {
  name: string;
  url: string;
  sha256?: string;
}

export interface ReleaseInfo {
  version: string;
  publishedAt: string;
  releaseUrl: string;
  macos: ReleaseAssetInfo;
  windows: ReleaseAssetInfo;
  linux: ReleaseAssetInfo;
}

interface GitHubReleaseAsset {
  name?: string;
  browser_download_url?: string;
}

interface GitHubLatestReleaseResponse {
  tag_name?: string;
  published_at?: string;
  html_url?: string;
  assets?: GitHubReleaseAsset[];
}

const REPO = 'Skyl9/AnkiDraft';
const BASE_DOWNLOAD = `https://github.com/${REPO}/releases/latest/download`;
const LATEST_RELEASE_PAGE = `https://github.com/${REPO}/releases/latest`;
const LATEST_RELEASE_API = `https://api.github.com/repos/${REPO}/releases/latest`;

const PLATFORM_KEYWORDS = {
  macos: ['macos-arm64.dmg', '.dmg', 'macos-arm64.zip'],
  windows: ['setup-x64.exe', '.exe', 'windows-x64.zip'],
  linux: ['x86_64.appimage', '.appimage', 'linux-x86_64.tar.gz', '.tar.gz'],
} as const;

const FALLBACK_ASSETS = {
  macos: 'AnkiForge-macos-arm64.dmg',
  windows: 'ankiforge-windows-x64.zip',
  linux: 'AnkiForge-x86_64.AppImage',
} as const;

function pickAsset(
  assets: GitHubReleaseAsset[],
  keywords: readonly string[],
  fallbackName: string,
): ReleaseAssetInfo {
  for (const kw of keywords) {
    const match = assets.find((asset) => {
      const name = (asset.name || '').toLowerCase();
      if (!name || name.endsWith('.sha256') || name.endsWith('.sig') || name.endsWith('.txt')) {
        return false;
      }
      return name.includes(kw);
    });
    if (match?.name) {
      return {
        name: match.name,
        url: `${BASE_DOWNLOAD}/${match.name}`,
      };
    }
  }
  return {
    name: fallbackName,
    url: `${BASE_DOWNLOAD}/${fallbackName}`,
  };
}

export async function getLatestRelease(): Promise<ReleaseInfo> {
  const fallback: ReleaseInfo = {
    version: 'latest',
    publishedAt: new Date().toISOString().slice(0, 10),
    releaseUrl: LATEST_RELEASE_PAGE,
    macos: {
      name: FALLBACK_ASSETS.macos,
      url: `${BASE_DOWNLOAD}/${FALLBACK_ASSETS.macos}`,
    },
    windows: {
      name: FALLBACK_ASSETS.windows,
      url: `${BASE_DOWNLOAD}/${FALLBACK_ASSETS.windows}`,
    },
    linux: {
      name: FALLBACK_ASSETS.linux,
      url: `${BASE_DOWNLOAD}/${FALLBACK_ASSETS.linux}`,
    },
  };

  try {
    const res = await fetch(LATEST_RELEASE_API, {
      headers: {
        Accept: 'application/vnd.github+json',
        'User-Agent': 'AnkiDraft-Website-Builder',
      },
    });
    if (!res.ok) {
      return fallback;
    }
    const data = (await res.json()) as GitHubLatestReleaseResponse;
    const assets = Array.isArray(data.assets) ? data.assets : [];
    const version = (data.tag_name || '').replace(/^v/i, '') || fallback.version;

    return {
      version,
      publishedAt: (data.published_at || fallback.publishedAt).slice(0, 10),
      releaseUrl: data.html_url || fallback.releaseUrl,
      macos: pickAsset(assets, PLATFORM_KEYWORDS.macos, FALLBACK_ASSETS.macos),
      windows: pickAsset(assets, PLATFORM_KEYWORDS.windows, FALLBACK_ASSETS.windows),
      linux: pickAsset(assets, PLATFORM_KEYWORDS.linux, FALLBACK_ASSETS.linux),
    };
  } catch {
    return fallback;
  }
}
