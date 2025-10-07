# 🧠 Community Detection using Spectral Decomposition and Louvain Algorithm

## 📋 Overview
This project implements and compares two popular **community detection algorithms** — **Spectral Decomposition** and **Louvain Algorithm** — on real-world graph datasets.  
The goal is to identify meaningful clusters (communities) within large-scale social networks such as **Facebook** and **Bitcoin** transaction graphs, and analyze their structural properties.

---

## 🚀 Features
- Implementation of **Spectral Clustering** based on **Fiedler vectors** from Laplacian matrix.  
- Custom **automated stopping criterion** for spectral decomposition using gap-based heuristic.  
- **Louvain algorithm** implementation for modularity-based community detection.  
- Built-in **visualization module** to plot:
  - Sorted Fiedler vectors  
  - Adjacency matrices (sorted by detected communities)  
  - Graph partitions and community layouts  
- **Performance comparison** between Spectral and Louvain algorithms.  

---

## 📊 Results Summary

| Dataset | Algorithm | Communities Detected | Runtime (s) | Key Observation |
|----------|------------|----------------------|--------------|------------------|
| Facebook | Spectral | 14 | 110.58 | Larger, interpretable groups |
| Facebook | Louvain | 101 | 32.12 | More granular, modular communities |
| Bitcoin | Spectral | 2 | 224.99 | Slow due to dense connectivity |
| Bitcoin | Louvain | 455 | 47.51 | Fast and efficient clustering |

> **Conclusion:**  
> Louvain algorithm performs faster (4–5×) and produces more refined community structures, while spectral decomposition provides more interpretable coarse-level communities.

---

## 🧩 Algorithms Used

### 🔹 Spectral Decomposition
1. Compute **Adjacency Matrix (A)**  
2. Compute **Graph Laplacian (L = D - A)**  
3. Find the **Fiedler Vector** (second smallest eigenvector of L)  
4. Split nodes based on sign of Fiedler vector values  
5. Recursively apply until stopping criteria met:
   - If community size < 100 → stop splitting  
   - If max gap < threshold × average gap → stop splitting  

### 🔹 Louvain Algorithm
1. Initialize each node as its own community  
2. Move nodes between communities to **maximize modularity gain**  
3. Aggregate nodes in the same community and repeat  
4. Stop when modularity gain no longer improves  

---

## 🗂️ Project Structure
Community-Detection/
│
├── Community_Sachin.py # Main source code
├── Community-Sachin.pdf # Project report and observations
├── data/
│ ├── facebook_combined.txt # Facebook social graph data
│ └── soc-sign-bitcoinotc.csv # Bitcoin trust network data
└── README.md 


## 👨‍💻 Author

### **Sachin Tanwar**
**Data Scientist | Lowe’s India**  
*M.Tech in Artificial Intelligence (SR No: 26120)*  
📍 **Bangalore, India**  
📧 **sachintanwar.ai@gmail.com**  
🔗 [LinkedIn](https://www.linkedin.com/in/stanwar94/) &nbsp; | &nbsp; [GitHub](https://github.com/sachin10894/)

---

### 🧩 About the Author
Sachin is a **Data Scientist at Lowe’s India**, specializing in **machine learning, data-driven optimization, and large-scale system design**.  
He holds a **Master’s degree in Artificial Intelligence**, where his research focused on **graph theory, community detection, and distributed data systems**.  

He is passionate about:
- Building **end-to-end ML and data products**  
- Exploring **distributed computing frameworks**  
- Contributing to **open-source analytical tools**  

📚 Always exploring the intersection of **AI, systems, and scalability**.
