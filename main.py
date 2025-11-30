import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict, deque

# граф
graph = defaultdict(dict)

# список ребер і пропускна здатність
edges = [
    ("Термінал 1", "Склад 1", 25),
    ("Термінал 1", "Склад 2", 20),
    ("Термінал 1", "Склад 3", 15),
    ("Термінал 2", "Склад 2", 10),
    ("Термінал 2", "Склад 3", 15),
    ("Термінал 2", "Склад 4", 30),
    ("Склад 1", "Магазин 1", 15),
    ("Склад 1", "Магазин 2", 10),
    ("Склад 1", "Магазин 3", 20),
    ("Склад 2", "Магазин 4", 15),
    ("Склад 2", "Магазин 5", 10),
    ("Склад 2", "Магазин 6", 25),
    ("Склад 3", "Магазин 7", 20),
    ("Склад 3", "Магазин 8", 15),
    ("Склад 3", "Магазин 9", 10),
    ("Склад 4", "Магазин 10", 20),
    ("Склад 4", "Магазин 11", 10),
    ("Склад 4", "Магазин 12", 15),
    ("Склад 4", "Магазин 13", 5),
    ("Склад 4", "Магазин 14", 10)
]

# додати ребра в граф
for u, v, c in edges:
    graph[u][v] = c
    # зворотні ребра
    graph[v][u] = 0

# джерело і стік
INF = 1_000_000
terminals = ["Термінал 1", "Термінал 2"]
warehouses = ["Склад 1", "Склад 2", "Склад 3", "Склад 4"]
stores = [f"Магазин {i}" for i in range(1, 15)]

graph["S"] = {t: INF for t in terminals}
for store in stores:
    graph[store]["T"] = INF

# BFS для Едмондса-Карпа
def bfs(residual, parent):
    visited = set()
    queue = deque(["S"])
    visited.add("S")
    while queue:
        u = queue.popleft()
        for v in residual[u]:
            if v not in visited and residual[u][v] > 0:
                parent[v] = u
                if v == "T":
                    return True
                visited.add(v)
                queue.append(v)
    return False

# алгоритм Едмондса-Карпа
def edmonds_karp_with_flows(graph):
    residual = {u: graph[u].copy() for u in graph}
    flow_passed = defaultdict(lambda: defaultdict(int))
    max_flow = 0
    parent = {}
    
    while bfs(residual, parent):
        path_flow = float('inf')
        s = "T"
        while s != "S":
            path_flow = min(path_flow, residual[parent[s]][s])
            s = parent[s]
        
        v = "T"
        while v != "S":
            u = parent[v]
            residual[u][v] -= path_flow
            if v not in residual:
                residual[v] = {}
            if u not in residual[v]:
                residual[v][u] = 0
            residual[v][u] += path_flow
            flow_passed[u][v] += path_flow
            v = parent[v]
        
        max_flow += path_flow
        parent = {}
    
    return max_flow, flow_passed

max_flow, flow_passed = edmonds_karp_with_flows(graph)
print("Максимальний потік:", max_flow)

# граф для візуалізації
G = nx.DiGraph()

# ребра Термінал - Склад
for t in terminals:
    for w in warehouses:
        flow = flow_passed[t].get(w, 0)
        G.add_edge(t, w, weight=flow)

# ребра Склад - Магазин
for w in warehouses:
    for m in stores:
        flow = flow_passed[w].get(m, 0)
        G.add_edge(w, m, weight=flow)

# додати всі вузли
for node in terminals + warehouses + stores:
    if node not in G:
        G.add_node(node)

# позиції вузлів для меншої плутанини
pos = {}
x_counter = defaultdict(int)

# термінали
for i, t in enumerate(terminals):
    pos[t] = (i * 4, 3)

# склади
for i, w in enumerate(warehouses):
    pos[w] = (i * 4 + 2, 2)

# магазини
for i, m in enumerate(stores):
    pos[m] = (i * 1.5, 1)

# граф
plt.figure(figsize=(18, 8))
edge_colors = ["green" if G[u][v]['weight']>0 else "lightgray" for u,v in G.edges()]
edge_widths = [max(G[u][v]['weight']/5, 1) for u,v in G.edges()]
nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=12,
        font_weight="bold", arrows=True, edge_color=edge_colors, width=edge_widths)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.title("Логістична мережа: Термінали - Склади - Магазини", fontsize=14)
plt.show()

# коментарі в Readme