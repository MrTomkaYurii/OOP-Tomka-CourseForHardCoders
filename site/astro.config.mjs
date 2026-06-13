import { defineConfig } from "astro/config";
import { createReadStream, cpSync, existsSync, mkdirSync, statSync, readFileSync } from "fs";
import { resolve, join, extname } from "path";
import { fileURLToPath } from "url";

const repositoryName = process.env.GITHUB_REPOSITORY?.split("/")[1];
const repositoryOwner = process.env.GITHUB_REPOSITORY_OWNER;
const isGitHubActions = process.env.GITHUB_ACTIONS === "true";
const isUserPagesRepository = repositoryName === `${repositoryOwner}.github.io`;

// Lecture images live in lectures/_assets/_docx (outside site/)
const lectureAssetsDir = resolve(fileURLToPath(import.meta.url), "../../lectures/_assets");
const urlPrefix = "/_assets";

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

/** Astro integration: copy lectures/_assets into dist/ after build */
function copyLectureAssetsOnBuild() {
  return {
    name: "copy-lecture-assets",
    hooks: {
      "astro:build:done": ({ dir }) => {
        const dest = join(fileURLToPath(dir), "_assets");
        if (existsSync(lectureAssetsDir)) {
          mkdirSync(dest, { recursive: true });
          cpSync(lectureAssetsDir, dest, { recursive: true });
        }
      },
    },
  };
}

const basePath = process.env.BASE_PATH;

export default defineConfig({
  output: "static",
  site: repositoryOwner ? `https://${repositoryOwner}.github.io` : "http://localhost:4321",
  base: basePath ?? (isGitHubActions && repositoryName && !isUserPagesRepository ? `/${repositoryName}` : "/"),
  vite: {
    plugins: [blazorRunnerDevPlugin(), lectureAssetsDevPlugin()],
  },
  integrations: [copyLectureAssetsOnBuild()],
});
