# Community Detection using Spectral Decomposition and Louvain Algorithm

## Overview
This project implements and compares two popular **community detection** techniques — **Spectral Decomposition** and the **Louvain algorithm** — on real-world graph datasets.  
It is designed to identify meaningful clusters (communities) within large-scale social networks such as Facebook and Bitcoin transaction/trust graphs, and to visualize and compare the resulting community structures.

---

## Features
- Spectral clustering using the **Fiedler vector** of the Laplacian.
- Custom automated stopping criterion for spectral decomposition (gap-based heuristic).
- Implementation of the **Louvain** modularity-based community detection algorithm.
- Built-in visualizations:
  - Sorted Fiedler vector plots
  - Adjacency matrix heatmaps (sorted by communities)
  - Community-colored network layouts
- Runtime and community-size comparison between both algorithms.

---

## Quick Results (summary)
| Dataset  | Algorithm | Communities Detected | Approx. Runtime (s) |
|----------|-----------|----------------------|---------------------:|
| Facebook | Spectral  | 14                   | 110.58              |
| Facebook | Louvain   | 101                  | 32.12               |
| Bitcoin  | Spectral  | 2                    | 224.99              |
| Bitcoin  | Louvain   | 455                  | 47.51               |

> **Observation:** Louvain is significantly faster (roughly 4–5× faster on these datasets) and produces finer-grained communities. Spectral decomposition gives coarser, more interpretable partitions but is slower.

---

## Algorithms & Stopping Criteria

### Spectral Decomposition
1. Build adjacency matrix `A`.
2. Compute Laplacian `L = D - A`.
3. Compute the **Fiedler vector** (the eigenvector corresponding to the second-smallest eigenvalue of `L`).
4. Partition nodes by sign (or ordering) of Fiedler vector values.
5. Recursively split subgraphs using an automated stopping rule:
   - Do not split if community size < 100.
   - If a split would create a partition with size < 20, avoid that split.
   - Use a gap-based heuristic on the sorted Fiedler vector: split only if `max_gap > a * avg_gap` (where `a` is an empirically chosen constant).

### Louvain Algorithm
1. Initialize each node in its own community.
2. Iteratively move nodes between communities to maximize modularity gain.
3. Aggregate communities and repeat until no modularity improvement is possible.
4. Return final partitioning.

---

## Project Structure
