# Music Artist Community Detection

An academic network analysis project that groups music artists by genre similarity and compares **Girvan–Newman** with **Louvain** community detection.

Built with Python, pandas and NetworkX, with an HTML/JavaScript visualization using vis-network.

## Analysis pipeline

1. Clean artist names, follower counts and genre lists from `nodes.csv`.
2. Keep artists with at least three genres and select up to 400 by follower count.
3. Build an undirected graph using genre-set Jaccard similarity as the edge weight, with a threshold of **0.6**.
4. Remove isolated nodes and compare divisive Girvan–Newman partitions with weighted Louvain communities.
5. Inspect communities in the console or explore the CSV-driven browser demo.

The retained graph may have fewer than 400 nodes after isolated artists are removed. Genre similarity represents shared labels, not a verified collaboration or musical influence relationship.

## Run the analysis

Requires Python 3 and a virtual environment:

```sh
git clone https://github.com/Hanyer001/Entrega-3-Redes.git
cd Entrega-3-Redes
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pandas networkx
python main.py
```

On Windows, create the environment with `py -m venv .venv` and activate it with `.venv\Scripts\Activate.ps1` in PowerShell.

The repository already includes `top_400_artists_gn.csv`. Run `main.py` from the repository root: it requests at least five Girvan–Newman communities and lets Louvain determine its partition. Girvan–Newman can take longer because it repeatedly computes edge betweenness. Louvain has no fixed seed in this implementation, so partitions can vary between runs.

## Open the visualization

From the repository root:

```sh
python -m http.server 8000 --bind 127.0.0.1
```

Open [http://127.0.0.1:8000/demo.html](http://127.0.0.1:8000/demo.html). The demo fetches `top_400_artists_gn.csv` and loads vis-network from a CDN, so use HTTP and an internet connection for that dependency.

## Files and outputs

| File | Purpose |
| --- | --- |
| `limpieza.py` | Regenerates the cleaned CSV and a GML graph connecting artists that share any genre. |
| `grafo.py` | Builds the weighted graph with the Jaccard threshold and removes isolates. |
| `girvan_newman.py` | Divisive community detection, stopping at the requested partition size. |
| `louvain.py` | Weighted modularity-based community detection. |
| `main.py` | Runs both algorithms and prints community summaries. |
| `exportar_datos.py` | Generates `graph_data.json` with graph data, Girvan–Newman steps and Louvain results. |
| `demo.html` | Browser visualization using the cleaned CSV. |

Optional commands:

```sh
python limpieza.py
python exportar_datos.py
```

`limpieza.py` overwrites the cleaned CSV and GML output. Its shared-genre GML graph differs from the Jaccard-threshold graph used by `main.py`. The JSON exporter is a separate analysis output; the current demo reads the CSV directly.

## Scope

This is an exploratory coursework project. The dependency versions are not pinned and there is no automated test suite. Reproducible comparisons should record package versions, algorithm parameters and random seeds, along with the input dataset and its provenance.
