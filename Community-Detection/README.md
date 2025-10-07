🧠 Community Detection using Spectral Decomposition and Louvain Algorithm
📋 Overview

This project implements and compares two popular community detection algorithms — Spectral Decomposition and Louvain Algorithm — on real-world graph datasets.
The goal is to identify meaningful clusters (communities) within large-scale social networks such as Facebook and Bitcoin transaction graphs, and analyze their structural properties.

🚀 Features

Implementation of Spectral Clustering based on Fiedler vectors from Laplacian matrix.

Custom automated stopping criterion for spectral decomposition using gap-based heuristic.

Louvain algorithm implementation for modularity-based community detection.

Built-in visualization module to plot:

Sorted Fiedler vectors

Adjacency matrices (sorted by detected communities)

Graph partitions and community layouts

Performance comparison between Spectral and Louvain algorithms.

📊 Results Summary
Dataset	Algorithm	Communities Detected	Runtime (s)	Key Observation
Facebook	Spectral	14	110.58	Larger, interpretable groups
Facebook	Louvain	101	32.12	More granular, modular communities
Bitcoin	Spectral	2	224.99	Slow due to dense connectivity
Bitcoin	Louvain	455	47.51	Fast and efficient clustering

Conclusion:
Louvain algorithm performs faster (4–5×) and produces more refined community structures, while spectral decomposition provides more interpretable coarse-level communities.

🧩 Algorithms Used
🔹 1. Spectral Decomposition

Compute Adjacency Matrix (A)

Compute Graph Laplacian (L = D - A)

Find the Fiedler Vector (second smallest eigenvector of L)

Split nodes based on sign of Fiedler vector values

Recursively apply until stopping criteria met:

If community size < 100 → stop splitting

If max gap < threshold × average gap → stop splitting

🔹 2. Louvain Algorithm

Initialize each node as its own community

Move nodes between communities to maximize modularity gain

Aggregate nodes in the same community and repeat

Stop when modularity gain no longer improves

🗂️ Project Structure
Community-Detection/
│
├── Community_Sachin.py          # Main source code
├── Community-Sachin.pdf         # Project report and observations
├── data/
│   ├── facebook_combined.txt    # Facebook social graph data
│   └── soc-sign-bitcoinotc.csv  # Bitcoin trust network data
├── README.md                    # This file
└── requirements.txt             # Dependencies (optional)

🧠 Key Functions
Function	Description
import_facebook_data(path)	Loads undirected Facebook edge list
import_bitcoin_data(path)	Loads weighted Bitcoin trust network
getAdjMat(edgeList)	Generates adjacency matrix
getLaplacianMatrix(adjMat)	Computes graph Laplacian
getFreidel(lapMat)	Calculates and sorts Fiedler vector
spectralDecomposition()	Runs full spectral community detection
louvain_one_iter()	Runs single iteration of Louvain algorithm
createSortedAdjMat()	Reorders adjacency matrix based on communities
showAdjMatrix()	Visualizes adjacency matrices using matplotlib
⚙️ Installation & Usage
1️⃣ Clone the repository
git clone https://github.com/<your-username>/Community-Detection.git
cd Community-Detection

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Prepare datasets

Place the following files inside a data/ folder:

facebook_combined.txt

soc-sign-bitcoinotc.csv

4️⃣ Run the project
python Community_Sachin.py

📈 Visualization Outputs

The script generates:

Sorted Fiedler vector scatter plots

Adjacency matrix heatmaps

Community-colored graph layouts

All visualizations are interactive and appear sequentially during execution.

📘 References

Newman, M. E. J. Modularity and community structure in networks, PNAS (2006)

Luxburg, U. von. A tutorial on spectral clustering, Statistics and Computing (2007)

👨‍💻 Author

Sachin Tanwar
M.Tech AI, SR: 26120
Lowe’s India — Data Scientist
