#!/usr/bin/env python
# coding: utf-8
import os

from tqdm import tqdm
import json
import networkx as nx
import argparse
# import matplotlib.pyplot as plt

DEFAULT_OUTPUT_PATH = 'graph.gexf'  # Path to save
output_path = DEFAULT_OUTPUT_PATH
contacts = None


def merge_json_files(*filenames):
    merged = {}
    for filename in filenames[::-1]:
        assert os.path.isfile(filename), "File {} doesn't exist!".format(filename)
        with open(filename, 'r', encoding='utf-8') as file:
            merged.update(json.load(file))
    return merged


def insert_data_into_graph(data, graph, contacts=None, only_contacts=False):
    groups = list(data.values())

    if contacts:
        for group in groups:
            for phone in group["participants"][:]:
                if phone in contacts:
                    graph.add_node(phone, label=contacts[phone])

                elif only_contacts:
                    group["participants"].remove(phone)

    print("{} groups were found.".format(len(groups)))
    for group_id, group in tqdm(data.items()):
        if group_id not in visited_groups:
            visited_groups.add(group_id)

            participants_cpy = group["participants"][:]
            for participant in group["participants"]:
                participants_cpy.remove(participant)
                for neighbor in participants_cpy:
                    if graph.has_edge(participant, neighbor):
                        graph[participant][neighbor]["weight"] += 1
                    else:
                        graph.add_edge(participant, neighbor, weight=1)


parser = argparse.ArgumentParser(description="Generate GEXF graph file from scraped data")
parser.add_argument("data", nargs="+", type=str, help="paths to data (.json) files")
parser.add_argument("-c", "--contacts", nargs="*", type=str, help="paths to contacts (.json) files, so that the first "
                                                                  "file overrides names of identical contacts in other "
                                                                  "files")
parser.add_argument("-oc", "--only-contacts", action="store_true", help="use only given contacts when creating graph")
parser.add_argument("-o", "--output", type=str, help="path to output GEXF file (default is {})"
                    .format(DEFAULT_OUTPUT_PATH))
args = parser.parse_args()

if args.output:
    output_path = args.output

if args.contacts:
    contacts = merge_json_files(*args.contacts)

assert args.contacts or not args.only_contacts, "When using --only-contacts, provide a contacts file using the " \
                                                "--contacts argument"
only_contacts = args.only_contacts

visited_groups = set()

print("Creating graph...")
print()

G = nx.Graph()
for path in args.data:
    with open(path, mode='r', encoding='utf-8') as f:
        groups_data = json.load(f)
    insert_data_into_graph(groups_data, G, contacts=contacts, only_contacts=only_contacts)
    print()

print("Saving Graph to {}...".format(output_path))
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
