# TSP — Genetic Algorithm

A simple, self-contained Genetic Algorithm (GA) solver for the Traveling Salesman Problem (TSP) on 2D points.

The solver reads a list of city coordinates, evolves a population of routes, and prints the best route length and its path.

---

## Quickstart

# 1) (Optional) Create a virtual environment
python -m venv .venv
# Windows
.\.venv\Scripts\activate

# 2) Install dependencies
# This project uses only the Python standard library (no extra packages).
# If you later add numpy/matplotlib, list them in requirements.txt and:
# pip install -r requirements.txt

# 3) Run
python src/main.py

---

## Data

Place your input under `data/input.txt` (relative to the project root):

data/
  input.txt

**`input.txt` format (example):**

137 199 93  
120 199 34  
199 173 30  
175 53 76  
144 39 130  
173 101 186  
153 196 97  

- One city per line.  
- Each line is three integers: `id x y` (your current script uses `id` + 2D coords).  
- Whitespace separated.  

> If your original format differs, update the parser in `src/main.py` accordingly.

---

## How paths are resolved (no “can’t find file” issues)

`src/main.py` resolves the data path like this:

from pathlib import Path

here = Path(__file__).resolve().parent.parent  
data_file = here / "data" / "input.txt"

with open(data_file, "r") as file:  
    lines = file.readlines()

This makes `python src/main.py` work no matter where you launch it from.

---

## Typical Output

576.125  
137 199 93  
120 199 34  
199 173 30  
175 53 76  
144 39 130  
173 101 186  
153 196 97  

- First line: best route length (total distance).  
- Following lines: the route (in visiting order).  

---

## Repo Layout

src/  
  main.py            # GA solver (selection, crossover, mutation, evolution loop)  
data/  
  input.txt          # your city list (not tracked by git)  
README.md  
LICENSE  
.gitignore  

**.gitignore (suggested)**

# venv  
.venv/  
# bytecode  
__pycache__/  
# editors  
.vscode/  
.idea/  
# data (if you don’t want to commit raw inputs)  
data/  
!data/.gitkeep  

Create an empty `data/.gitkeep` if you want the folder present without committing actual datasets.

---

## Notes / Next steps

- If you want deterministic runs, set a fixed seed at the top of `main.py`:  

  import random  
  random.seed(42)  

- Consider exporting the final route to a file (e.g., `outputs/best_route.txt`) for easier grading/sharing.  
- If you later add plotting, save a PNG of the best tour to `assets/`.  

---

## License

MIT License. See `LICENSE` for details.
