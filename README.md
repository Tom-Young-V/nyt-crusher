# NYT Crusher (Daily Games Helper)

**NYT Crusher** is a local, privacy-friendly puzzle-solving stack that combines a **Chrome extension** with a **Python Flask "solver server"**. The extension reads the live game board from the browser DOM, sends a compact game state to the local server over HTTP (`localhost`), and then uses the server's computed moves to drive the UI automatically (click/drag/swaps).

This repo showcases hands-on engineering across:
* browser automation + DOM state extraction (JavaScript)
* algorithmic puzzle solving (Python)
* API design between a frontend extension and a local backend (Flask/CORS)
* LLM-based assistance and fine-tuning LLMs for solving Connections

---

## High-level Architecture

1. **Chrome Extension**
   * `manifest.json` registers a keyboard command and injects content scripts into supported puzzle pages.
   * `background.js` routes the command to the correct content script, then forwards the board state to the Python server.
   * `Scripts/waffleContent.js` and `Scripts/squaredleContent.js` extract board state and replay the server's solution via synthesized pointer/mouse events.

2. **Python Flask Solver Server**
   * `app.py` exposes HTTP endpoints used by the extension:
     * `POST /solveWaffle`
     * `POST /solveSquaredle`
   * The server instantiates the relevant solver class(s), computes the next move(s)/solution, and returns JSON back to the extension.

3. **Solver Modules (Algorithmic Core)**
   * `Waffle Solver/waffleSolver.py`: constraint-based recursion + pruning, then swap-sequence construction.
   * `Squaredle Solver/grid.py` + `wordStrand.py`: DFS-style grid search with aggressive word-constraint filtering.
   * Additional solvers exist in-repo for Wordle/Connections/Spelling Bee, intended for experimentation and offline solving.

---

## Supported Targets (Currently Wired in the Extension)

The extension is set up to solve:
* **Waffle** (`https://wafflegame.net/*`)
* **Squaredle** (`https://squaredle.app/*`)

Wordle/Connections/NYT Mini solvers are included as code modules, but integrating them into the live extension requires additional wiring (content scripts + server endpoints).

---

## Technical Highlights (What This Repo Demonstrates)

### 1. Real-time state extraction from the browser
Instead of hardcoding puzzle answers, the extension reconstructs game state directly from the DOM:
* Waffle: captures the board tile HTML and current "swaps left", then converts UI state into the server's expected representation.
* Squaredle: extracts the ordered letter grid and maintains mappings from letter indices to DOM nodes so the solution can be replayed deterministically.

### 2. Decoupled system design: frontend UI automation <-> backend computation
The backend doesn't know about the browser, only the solver classes (e.g., `WaffleSolver`, `Grid` for Squaredle). This separation makes the algorithm testable offline and keeps the UI layer relatively thin.

### 3. Information-driven decision making (Wordle solver module)
The Wordle solver (`Wordle Solver/wordleSolver.py`) computes the **expected information gain** ("narrowing factor") for candidate guesses by:
* enumerating possible color outcomes for each guess
* weighting by the induced partition sizes of remaining candidates
* ranking words by best expected reduction

### 4. Constraint solving + pruning (Waffle solver module)
The Waffle solver performs:
* **recursive partial solving** using candidate word lists filtered by grid patterns (regex-based constraints)
* **intersection consistency checks** to ensure yellow letters align across intersecting words
* detection of failure modes (no solution / multiple solutions)
* swap sequence generation by simulating and minimizing remaining edits (via state caching keyed by a simplified grid signature)

### 5. Grid search for word formation (Squaredle solver module)
The Squaredle solver implements a graph-style traversal:
* precomputes "neighbor" indexes including diagonals
* builds word strands incrementally (copy-on-write recursion)
* filters candidate continuations using regex patterns based on remaining letters
* stores and returns full word paths as `(word, indexes)` so the extension can replay the path.

### 6. LLM integration utilities for Connections
Under `Connections Solver/Connections ChatGPT/`, the repo includes:
* prompt-based category suggestion via the OpenAI API (`chatGPTRequests.py`)
* dataset formatting utilities and fine-tuning support scripts (`Fine Tuning Data Sets/`)
* token counting / dataset sanity checks using `tiktoken`

This is structured as "research scaffolding" for LLM-assisted strategy, complementing the more deterministic solvers.

---

## How to Run (End-to-end: Extension + Local Solver)

### 1. Start the local Flask server
From the repository root:
```bash
python3 app.py
```
The server listens on `http://127.0.0.1:5000/`.

### 2. Load the Chrome extension
1. Open `chrome://extensions`
2. Enable **Developer mode**
3. Click **Load unpacked**
4. Select this repo folder (the one containing `manifest.json`)

### 3. Solve a puzzle
1. Open one of the supported pages:
   * `https://wafflegame.net/` (daily or deluxe)
   * `https://squaredle.app/`
2. Press the extension command: **Ctrl+Shift+9** or press the logo added by the extension in the top right corner of the webpage
3. The extension will:
   * extract the board state
   * POST it to the Flask endpoint
   * apply the returned next move(s) through simulated pointer events
   * automatically click the divs on the website and complete the game in record time

---

## Running / Using Solvers Offline (For Development)

The repo is organized by game, so you can experiment with solver classes directly in Python:
* `Waffle Solver/waffleSolver.py`
* `Squaredle Solver/grid.py` / `Squaredle Solver/squaredleSolver.py`
* `Wordle Solver/wordleSolver.py`
* `Connections Solver/connectionsSolver.py`

Some scripts include optional debug output and "testing harnesses" for algorithm iteration (e.g., `solverTesting.py` style files).

---

## Dependencies (By Feature)

The exact dependencies vary by which solver/scraper you run:
* Core local server: `flask`, `flask-cors`
* Browser automation + scraping utilities (Connections/Waffle archiving):
  * `selenium`
  * `beautifulsoup4`
  * Requires a Chrome installation (and typically a matching ChromeDriver)
* LLM utilities (Connections ChatGPT):
  * `openai`
  * `tiktoken`
  * `numpy`

If you only run the extension with Waffle/Squaredle, you mainly need the Flask server dependencies.

---

## Repo Layout (Quick Map)

* `app.py`: Flask server + API endpoints
* `manifest.json`, `background.js`: Chrome extension wiring
* `Scripts/`: content scripts used by the extension
  * `waffleContent.js`
  * `squaredleContent.js`
* `Waffle Solver/`: Waffle solver + optional Selenium-based puzzle grid scraping
* `Squaredle Solver/`: Squaredle solver (DFS/grid search) + word list assets
* `Wordle Solver/`: Wordle solver (expected information gain ranking)
* `Connections Solver/`: Connections scraping + (optional) LLM prompting/fine-tuning helpers
* `Spelling Bee/`: word-finding utilities

---

## Notes / Security Considerations

* `app.py` enables permissive CORS for development. For production/internship demos, it's better to restrict origins to the Chrome extension scheme.
* The solver server is local (`localhost`). Game state is computed on-device and returned as small JSON payloads.

---

## What I'd Show in an Internship Interview

If you want to highlight "engineering depth" beyond the puzzle domain, I'd point reviewers to:
* the **frontend/backend contract** (`background.js` <-> `app.py`) and how it drives a deterministic automation loop
* the **solver implementations** that treat the puzzle as a constraint/search problem rather than pattern-matching answers
* the ability to build tooling around the core system (scrapers, offline solvers, and dataset utilities for LLM experimentation)

