import { defineConfig } from "astro/config";

const isGitHubPages = process.env.GITHUB_ACTIONS === "true";

export default defineConfig({
  output: "static",
  site: process.env.PUBLIC_SITE_URL ?? "https://spinning-arrow.sunaybhat.me",
  base: process.env.PUBLIC_BASE_PATH ?? (isGitHubPages ? "/spinning-arrow" : "/"),
});
