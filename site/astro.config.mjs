import { defineConfig } from "astro/config";

const repositoryName = process.env.GITHUB_REPOSITORY?.split("/")[1];
const repositoryOwner = process.env.GITHUB_REPOSITORY_OWNER;
const isGitHubActions = process.env.GITHUB_ACTIONS === "true";
const isUserPagesRepository = repositoryName === `${repositoryOwner}.github.io`;

export default defineConfig({
  output: "static",
  site: repositoryOwner ? `https://${repositoryOwner}.github.io` : "http://localhost:4321",
  base: isGitHubActions && repositoryName && !isUserPagesRepository ? `/${repositoryName}` : "/",
});
