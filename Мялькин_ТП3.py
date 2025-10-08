import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

nodes = list("ABCDEFGH")
edges = [
    ("A", "B", 2),
    ("A", "C", 5),
    ("B", "D", 3),
    ("C", "D", 4),
    ("C", "E", 6),
    ("D", "F", 5),
    ("E", "F", 3),
    ("F", "G", 4),
    ("G", "H", 5),
]

G = nx.Graph()
G.add_nodes_from(nodes)
for u, v, w in edges:
    G.add_edge(u, v, weight=w)

degrees = dict(G.degree())

sum_weights = {}
for n in G.nodes():
    wsum = 0
    for nb in G.neighbors(n):
        wsum += G[n][nb]["weight"]
    sum_weights[n] = wsum

print("Степени узлов:")
for n in sorted(G.nodes()):
    print(f"  {n}: degree={degrees[n]}")

print("\nСумма весов инцидентных рёбер:")
for n in sorted(G.nodes()):
    print(f"  {n}: sum_w={sum_weights[n]}")

max_deg = max(degrees.values())
candidates = [n for n, d in degrees.items() if d == max_deg]

best_node = min(candidates, key=lambda n: (sum_weights[n], n))

print(f"\nЦентральный узел по правилу: {best_node} "
      f"(degree={degrees[best_node]}, sum_w={sum_weights[best_node]})")

plt.figure(figsize=(7, 5))
pos = nx.spring_layout(G, seed=42)

node_colors = []
for n in G.nodes():
    node_colors.append("#f94144" if n == best_node else "#90be6d")

weights = [G[u][v]["weight"] for u, v in G.edges()]
max_w = max(weights) if weights else 1
edge_widths = [1.5 + 2.5 * (w / max_w) for w in weights]

nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=900, edgecolors="black")
nx.draw_networkx_edges(G, pos, width=edge_widths, edge_color="#577590")
nx.draw_networkx_labels(G, pos, font_size=11, font_weight="bold")

edge_labels = {(u, v): G[u][v]["weight"] for u, v in G.edges()}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

plt.title("Взвешенный граф (центральный узел выделен)")
plt.axis("off")
plt.tight_layout()
plt.show()

points = np.array([
    [1, 1],
    [2, 2],
    [3, 1],
    [4, 2],
    [5, 2],
    [6, 3],
    [7, 2],
    [8, 3],
], dtype=float)
labels_points = ["P1","P2","P3","P4","P5","P6","P7","P8"]

def kmeans(X, k=3, iters=20, seed=42):
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(X), size=k, replace=False)
    C = X[idx].copy()
    for _ in range(iters):
        dists = np.linalg.norm(X[:, None, :] - C[None, :, :], axis=2)  # [n,k]
        clusters = np.argmin(dists, axis=1)
        newC = C.copy()
        for j in range(k):
            pts = X[clusters == j]
            if len(pts) > 0:
                newC[j] = pts.mean(axis=0)
        if np.allclose(newC, C):
            break
        C = newC
    return clusters, C

k = 3
clusters, centers = kmeans(points, k=k, iters=40, seed=42)

plt.figure(figsize=(7, 5))
for j in range(k):
    idx = (clusters == j)
    plt.scatter(points[idx, 0], points[idx, 1], s=70, label=f"Зона {j+1}")
    for (x, y), lbl in zip(points[idx], np.array(labels_points)[idx]):
        plt.text(x + 0.05, y + 0.05, lbl, fontsize=9)

plt.scatter(centers[:, 0], centers[:, 1], marker="X", s=160, edgecolor="black", linewidths=1.5, label="Центры")

plt.title("Мини-районирование (k-means, k=3)")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()

print("\nРаспределение точек по зонам (k=3):")
for j in range(k):
    pts = [lbl for lbl, c in zip(labels_points, clusters) if c == j]
    print(f"  Зона {j+1}: {', '.join(pts) if pts else '(пусто)'}")
