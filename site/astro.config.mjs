import { defineConfig } from "astro/config";
import { createReadStream, cpSync, existsSync, mkdirSync, statSync, readFileSync } from "fs";
import { resolve, join, extname } from "path";
import { fileURLToPath } from "url";

const repositoryName = process.env.GITHUB_REPOSITORY?.split("/")[1];
const repositoryOwner = process.env.GITHUB_REPOSITORY_OWNER;
const isGitHubActions = process.env.GITHUB_ACTIONS === "true";
const isUserPagesRepository = repositoryName === `${repositoryOwner}.github.io`;

// Lecture images live in lectures/_assets (outside site/)
const lectureAssetsDir = resolve(fileURLToPath(import.meta.url), "../../lectures/_assets");
const urlPrefix = "/_assets";

// Git-workshop images live in git-workshop/_assets (outside site/)
const workshopAssetsDir = resolve(fileURLToPath(import.meta.url), "../../git-workshop/_assets");
const workshopUrlPrefix = "/git-workshop";

const MIME = {
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".svg": "image/svg+xml",
  ".gif": "image/gif",
  ".webp": "image/webp",
};

const runnerDir = resolve(fileURLToPath(import.meta.url), "../public/runner");

/** Vite plugin: serve /runner/ → /runner/index.html (Blazor SPA fallback) */
function blazorRunnerDevPlugin() {
  return {
    name: "blazor-runner-dev",
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        const url = req.url?.split("?")[0] ?? "";
        // Serve index.html for /runner/ so Blazor router works correctly
        if (url === "/runner" || url === "/runner/") {
          const indexPath = join(runnerDir, "index.html");
          if (existsSync(indexPath)) {
            res.setHeader("Content-Type", "text/html");
            createReadStream(indexPath).pipe(res);
            return;
          }
        }
        next();
      });
    },
  };
}

/** Vite plugin: serve lectures/_assets during dev server */
function lectureAssetsDevPlugin() {
  return {
    name: "lecture-assets-dev",
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        const url = req.url?.split("?")[0] ?? "";
        if (!url.startsWith(urlPrefix)) return next();
        const filePath = join(lectureAssetsDir, url.slice(urlPrefix.length));
        if (!existsSync(filePath) || !statSync(filePath).isFile()) return next();
        res.setHeader("Content-Type", MIME[extname(filePath)] ?? "application/octet-stream");
        res.setHeader("Content-Length", statSync(filePath).size);
        createReadStream(filePath).pipe(res);
      });
    },
  };
}

/** Vite plugin: serve git-workshop/_assets during dev server */
function workshopAssetsDevPlugin() {
  return {
    name: "workshop-assets-dev",
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        const url = req.url?.split("?")[0] ?? "";
        if (!url.startsWith(workshopUrlPrefix + "/")) return next();
        const filePath = join(workshopAssetsDir, url.slice(workshopUrlPrefix.length));
        if (!existsSync(filePath) || !statSync(filePath).isFile()) return next();
        res.setHeader("Content-Type", MIME[extname(filePath)] ?? "application/octet-stream");
        res.setHeader("Content-Length", statSync(filePath).size);
        createReadStream(filePath).pipe(res);
      });
    },
  };
}

/** Astro integration: copy lectures/_assets and git-workshop/_assets into dist/ after build */
function copyLectureAssetsOnBuild() {
  return {
    name: "copy-lecture-assets",
    hooks: {
      "astro:build:done": ({ dir }) => {
        const lectDest = join(fileURLToPath(dir), "_assets");
        if (existsSync(lectureAssetsDir)) {
          mkdirSync(lectDest, { recursive: true });
          cpSync(lectureAssetsDir, lectDest, { recursive: true });
        }
        const wsDest = join(fileURLToPath(dir), "git-workshop");
        if (existsSync(workshopAssetsDir)) {
          mkdirSync(wsDest, { recursive: true });
          cpSync(workshopAssetsDir, wsDest, { recursive: true });
        }
      },
    },
  };
}

const basePath = process.env.BASE_PATH;

export default defineConfig({
  output: "static",
  site: "https://tomka.space",
  base: basePath ?? (isGitHubActions && repositoryName && !isUserPagesRepository ? `/${repositoryName}` : "/"),
  vite: {
    plugins: [blazorRunnerDevPlugin(), lectureAssetsDevPlugin(), workshopAssetsDevPlugin()],
  },
  integrations: [copyLectureAssetsOnBuild()],
});
