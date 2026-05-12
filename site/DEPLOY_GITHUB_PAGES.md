# Deploy to GitHub Pages

The course site is deployed by GitHub Actions from `.github/workflows/deploy-site.yml`.

## Repository settings

1. Push the repository to GitHub.
2. Open **Settings** -> **Pages**.
3. In **Build and deployment**, set **Source** to **GitHub Actions**.
4. Push to `main` or run the workflow manually from **Actions**.

## How it works

The workflow:

1. Installs dependencies in `site/` with `npm ci`.
2. Builds Astro with `npm run build`.
3. Publishes `site/dist` to GitHub Pages.

For a repository named `OOP-Tomka-CourseForHardCoders`, Astro automatically uses:

```txt
/OOP-Tomka-CourseForHardCoders/
```

as the production base path on GitHub Pages, while local development keeps `/`.

## Local check

Run from `site/`:

```bash
npm install
npm run build
```
