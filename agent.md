# Agent Development Protocol (Codex + Claude Code)

This file defines the required workflow for AI coding agents working in this repository.

## 1) Scope and Repository Boundaries

- Primary project repository:
  - D:/document/Obsidian/vaults/J-Workspace/AGI/Agents/projects/QuantDinger
- Frontend source repository (local-only, do not push):
  - D:/app/QuantDinger-Vue

Mandatory rule:
- Frontend source code changes must be made in D:/app/QuantDinger-Vue.
- The D:/app/QuantDinger-Vue repository is local-only for development and build. Do not push that repository.
- Only push changes in QuantDinger project repo when explicitly requested.

## 2) Frontend Change Workflow

When a frontend feature/style/i18n change is requested, follow exactly:

1. Modify source code in:
   - D:/app/QuantDinger-Vue/src
2. Build frontend:
   - cd D:/app/QuantDinger-Vue
   - npm run build
3. Sync built artifacts into project repo:
   - from D:/app/QuantDinger-Vue/dist
   - to D:/document/Obsidian/vaults/J-Workspace/AGI/Agents/projects/QuantDinger/frontend/dist
4. Update running frontend container:
   - docker cp frontend/dist/. quantdinger-frontend:/usr/share/nginx/html/
   - docker-compose restart quantdinger-frontend
5. Verify in browser:
   - http://localhost:8888
   - hard refresh (Ctrl+Shift+R)

## 3) Docker Deployment Location

Frontend static files served by nginx are located at:
- Container path: /usr/share/nginx/html

Project-side deploy source path:
- D:/document/Obsidian/vaults/J-Workspace/AGI/Agents/projects/QuantDinger/frontend/dist

## 4) Git Rules

- Never stage or push unrelated files.
- Use selective add for requested files only.
- If user asks "only push X", include only X path changes in commit.
- Commit message format (recommended):
  - feat(scope): ...
  - fix(scope): ...
  - docs(scope): ...

Before push, always run:
- git status --short
- git show --name-only --pretty=format:%H -1

## 5) Validation Checklist (Required)

Before declaring done for code changes:

- Build success confirmed (no build errors).
- Container restarted or rebuilt as required.
- UI/API behavior verified for changed scope.
- No unintended file changes included in commit.

## 6) UI/Styling Tasks

For UI readability fixes (color contrast, labels, spacing):

- Prioritize contrast and legibility over decorative effects.
- Keep both light and dark theme readability.
- Verify label truncation/overflow behavior.
- Prefer minimal, targeted CSS changes in component scope.

## 7) Communication Format for Agents

When reporting results, include:

1. What changed
2. Where changed (path list)
3. Build/deploy actions performed
4. Verification status
5. What was pushed (commit hash)

If any step cannot be executed, state the blocker and the exact next command needed.

## 8) Related Documentation

For detailed reference in this repo:
- FRONTEND_QUICK_REFERENCE.md
- FRONTEND_MODIFICATION_GUIDE.md
- FRONTEND_REPOSITORY_MAP.md
- DEPLOYMENT_SCRIPTS.md
- FRONTEND_MODIFICATION_RULES.md
