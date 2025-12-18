# Advent of Code — Solutions (AoC'25)

🎄 **Project:** Personal solutions to Advent of Code puzzles (organized by Day).

## Overview 🔎
This repository contains my personal Python solutions for Advent of Code puzzles. Each day is stored in its own directory (e.g. `Day_1/`, `Day_6/`) and typically contains:

- `main.py` — solution for the day's puzzle
- `input.txt` — *your personal puzzle input* (kept locally)
- optional `test_input.txt` — sample input(s) for quick checks

> Note: Advent of Code puzzles and the site are © Eric Wastl. The site requests that you do not include puzzle text or your personal puzzle inputs in publicly visible repositories. See https://adventofcode.com/ for details.

## Usage ⚙️
- Recommended Python: **3.8+** (use a virtual environment).
- To run a day's solution:

```bash
python Day_6/main.py
# or
cd Day_6 && python main.py
```

- Solutions typically read `input.txt` from the same directory. If you prefer to keep inputs private, provide the input via `stdin` or change the script to read from a different, non-tracked path.

## Tests ✅
Some days include sample or test inputs (e.g., `test_input.txt`). If you want to add automated tests, consider using `pytest` and place tests under a `tests/` folder or alongside modules with the `test_*.py` convention.

## Repository structure
```
AoC'25/
├─ Day_1/
│  ├─ main.py
│  ├─ input.txt
│  └─ ...
├─ Day_2/
│  └─ ...
├─ .gitignore
└─ README.md
```

## Privacy & Publishing ⚠️
If you intend to publish this repository publicly (e.g., GitHub):
- **Remove or omit** your personal `input.txt` files (they are unique to your account and Advent of Code asks that you don't share them).
- Consider adding a `.gitignore` rule or moving inputs to a separate `secrets/` folder that is not tracked.

Recommended `.gitignore` snippets:
```
# Cache and compiled files
__pycache__/
*.py[cod]

# (Optional) Personal AoC inputs
**/input.txt
```

## Contributing ✨
- Keep the same structure (one folder per day).
- If adding solutions, include a short comment in `main.py` explaining the approach and complexity.
- Do not paste puzzle statements or your personal inputs into the repo.

## Attribution & Links 🔗
- Advent of Code: https://adventofcode.com/
- Puzzles & site by Eric Wastl — please follow site guidelines regarding redistribution.

---

## Web UI 🌐
A lightweight **FastAPI** web UI is included at `web/` to browse **years** and **days** and view part outputs. The UI is **responsive** and works well on desktop, tablet, and mobile devices.

**Browsing**
- The index lists all available years (folders named like `2025`, `Y2025`, `2024`, etc.). Year directory names may include a leading `Y` (case-insensitive) — the UI will strip it when showing labels.
- Click a year to view its days, then click a day to run or view the solution.

**Quickstart**
```bash
python -m pip install -r web/requirements.txt
uvicorn web.main:app --reload
# then open http://127.0.0.1:8000
```


## Docker & GitHub deployment (CI)
This repository contains a minimal `Dockerfile` and a GitHub Actions workflow (`.github/workflows/build-and-push.yml`) that builds and publishes a container image to GitHub Container Registry (GHCR) on push to `main`.

Quick notes:
- Image name: `ghcr.io/<owner>/aoc25:latest` and `ghcr.io/<owner>/aoc25:<sha>` (the workflow tags both `latest` and commit SHA).
- The workflow uses the repository's `GITHUB_TOKEN` to authenticate with GHCR; no extra secret is required for GHCR push (the workflow requests `packages: write` permission).

How to use (push & deploy):
1. Commit and push these changes to your GitHub repo (push to `main` will trigger the CI build).
2. Confirm GitHub Actions runs successfully in the Actions tab.
3. The image will be published to GHCR at `ghcr.io/<your-org-or-username>/aoc25:latest`.

Deploying the image to a host:
- Render: create a Web Service and set the start command to `uvicorn web.main:app --host 0.0.0.0 --port $PORT` (or point Render to the GHCR image).
- Fly.io / Cloud Run / Railway / DO App Platform: point to the pushed image or use a provider-specific GitHub Action to deploy.

If you'd like, I can also add a provider-specific GitHub Actions workflow (e.g., auto-deploy to Render/Fly/Cloud Run) — tell me which provider you prefer.

**Quickstart**
```bash
python -m pip install -r web/requirements.txt
# Run with uvicorn (recommended):
uvicorn web.main:app --reload
# or (convenience) run as a module with Python:
python -m web.main
# then open http://127.0.0.1:8000
```

**Input options in the UI**
- **Upload a text file**: use the file picker to upload a `.txt` file and click "Run with custom input".
- **Paste input**: paste the input into the text box and hit Run.

The UI will use the provided input to compute the day's parts; if you reset the page or leave inputs empty, it will fall back to the `Day_<n>/input.txt` file.

**Design & UX improvements**
- The Day page now uses a centered, polished layout with a comfortable max-width for readability (no large fixed side gutters). The content is responsive and adapts across desktop, tablet, and mobile.
- Improvements include: hero header, clearer form controls, centered Run/Reset controls, result copy buttons, a small loading state on Run, and keyboard-accessible controls.

**Note:** the previous Flask-based UI implementation was removed in favor of the async FastAPI app at `web/main.py`. The old file `web/app.py` has been deprecated.

**API**
- `GET /api/day/<n>` — returns JSON: `{"day": n, "part1": ..., "part2": ...}`

> The UI runs locally and uses the same solver code as `main.py`. Do **not** publish your private `input.txt` files.

If you'd like, I can also:
- add `.gitignore` entries to exclude personal `input.txt` files, or
- add a small `run_all.py` runner that executes every day's `main.py` and prints results.

