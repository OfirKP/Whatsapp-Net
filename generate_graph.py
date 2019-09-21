#!/usr/bin/env python
# coding: utf-8

from tqdm import tqdm
import json
import networkx as nx
# import matplotlib.pyplot as plt

GROUPS_DATA_PATH = 'data.json'  # Replace with your json file path
OUTPUT_GEXF_PATH = 'graph.gexf'  # Path to save graph

with open(GROUPS_DATA_PATH, mode='r', encoding='utf-8') as f:
    data = json.load(f)

G = nx.Graph()
groups = list(data.values())

print("Creating graph...")
for group in tqdm(groups):
    participants_cpy = group["participants"][:]
    for participant in group["participants"]:
        participants_cpy.remove(participant)
        for neighbor in participants_cpy:
            if G.has_edge(participant, neighbor):
                G[participant][neighbor]["weight"] += 1
            else:
                G.add_edge(participant, neighbor, weight=1)
print()

print("Saving Graph...")
nx.write_gexf(G, OUTPUT_GEXF_PATH)

# Uncomment lines below to plot the graph using networkx and matplotlib

# pos = nx.spring_layout(G)
# # nodes
# nx.draw_networkx_nodes(G, pos, node_size=90)
#
# # edges
# nx.draw_networkx_edges(G, pos, edgelist=G.edges,
#                        width=0.1)
#
# # labels
# nx.draw_networkx_labels(G, pos, font_size=9, font_family='sans-serif')
#
# plt.axis('off')
# plt.show()
#
