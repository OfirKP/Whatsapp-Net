#!/usr/bin/env python
# coding: utf-8

from tqdm import tqdm
import json
import networkx as nx
import argparse
# import matplotlib.pyplot as plt

DEFAULT_OUTPUT_PATH = 'graph.gexf'  # Path to save
output_path = DEFAULT_OUTPUT_PATH

parser = argparse.ArgumentParser(description="Generate GEXF graph file from scraped data")
parser.add_argument("data", type=str, help="path to data (.json) file")
parser.add_argument("-c", "--contacts", type=str, help="path to contacts (.json) file")
parser.add_argument("-o", "--output", type=str, help="path to output GEXF file (default is {})"
                    .format(DEFAULT_OUTPUT_PATH))
args = parser.parse_args()

with open(args.data, mode='r', encoding='utf-8') as f:
    data = json.load(f)

if args.output:
    output_path = args.output

if args.contacts:
    with open(args.contacts, mode='r', encoding='utf-8') as f:
        contacts = json.load(f)

    for group in data.values():
        for contact in group["participants"][:]:
            if contact in contacts:
                group["participants"].remove(contact)
                group["participants"].append(contacts[contact])

print()

G = nx.Graph()
groups = list(data.values())

print("{} groups were found.".format(len(groups)))
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
nx.write_gexf(G, output_path)

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
