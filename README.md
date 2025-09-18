\# TSP Genetic Algorithm



A time-limited genetic algorithm (GA) for solving the Traveling Salesman Problem.  

Scales to ~200 cities, with runtime caps of 60–300 seconds depending on difficulty.



\## Features

\- Population-based GA with crossover, mutation, and elitism

\- Runtime-based stopping criterion (`--time-limit`)

\- Parameter tuning for easy/medium/hard/complex cases

\- Supports up to 200 cities



\## Quickstart

```bash

python -m venv .venv \&\& .\\.venv\\Scripts\\activate  # Windows

pip install -r requirements.txt



\# Example run

python src/main.py --input data/cities\_100.txt --time-limit 120



