---
name: github-actions-deploy
description: GitHub Actions CI/CD pipeline conventions — semantic release, PR merge flow, conventional commits, and workflow patterns for this project.
---

# GitHub Actions Deploy

## Pipeline overview
- `pr-title.yml` — Validates PR titles match conventional commit format on open/edit/sync.
- `merge.yml` — Squash-merges PRs when `/merge` comment is posted (requires approval).
- `release.yml` — Runs semantic-release on push to `main`, creating tags and GitHub releases.

## PR title format (enforced by CI)
```
<type>(<optional scope>): <description starting with lowercase>
```
Valid types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
Breaking changes: append `!` before colon (e.g., `feat!: redesign user API`).

## Merge flow
1. Open PR with conventional commit title.
2. Get at least one approval.
3. Comment `/merge` on the PR to trigger squash merge.
4. Merge commit uses PR title as the squash commit message.

## Semantic release
- Triggered on every push to `main`.
- Uses Node.js 20 + `npx semantic-release`.
- Reads conventional commit messages to determine version bump (patch/minor/major).
- Creates GitHub releases and tags automatically.
- Requires `GITHUB_TOKEN` with `contents:write`, `issues:write`, `pull-requests:write`.

## Adding a new workflow
- Place in `.github/workflows/<name>.yml`.
- Use least-privilege `permissions` — only request what the workflow needs.
- Pin action versions with `@v4` (major version), not `@main`.
- Never hardcode secrets — use `${{ secrets.* }}` or OIDC.
- For deployment workflows, use GitHub Environments for approval gates and environment-scoped secrets.

## Rollback
- Revert the merge commit on `main` via `git revert` + new PR.
- Semantic-release will not create a new release for `revert:` commits unless they change the public API.
- For infrastructure rollbacks, prefer redeploying the previous known-good tag rather than reverting code.
