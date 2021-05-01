#!/usr/bin/env python
# coding: utf-8

import argparse
from collections import defaultdict
from typing import Dict, Optional, List

from py2neo import Graph
from py2neo.bulk import create_nodes, create_relationships

from tqdm import tqdm

from generate_graph import merge_json_files

"""
    This script processes downloaded JSONs from scrape.js and creates a graph containing
    participant nodes, group nodes, and MEMBER_OF relationships between them into a neo4j backend.
"""

DEFAULT_BATCH_SIZE = 5000


def divide_into_batches(l: List, batch_size: int):
    assert batch_size > 0, "Batch size must be larger than 0"

    for i in range(0, len(l), batch_size):
        batch = l[i:i + batch_size]
        yield batch


def insert_relationships_into_graph(graph: Graph, serialized_groups: dict, batch_size: int = DEFAULT_BATCH_SIZE):
    """
    Create and insert relationships (MEMBER_OF) into the neo4j database using py2neo bulk functions
    :param batch_size: batch size to upload items in bulk to DB
    :param graph: represents connection to neo4j backend
    :param serialized_groups: scraper's output
    """
    relationships_data = []
    for group_id, group_properties in serialized_groups.items():
        if 'participants' in group_properties:
            group_participants_numbers = group_properties['participants']

            for participant_number in group_participants_numbers:
                # Prepare relationships info for bulk insertion
                relationships_data.append((participant_number, {}, group_id))

    # Bulk insert all relationships into DB
    print(f"Inserting {len(relationships_data)} relationships into DB...")
    for batch_relationships in tqdm(list(divide_into_batches(relationships_data, batch_size=batch_size))):
        create_relationships(
            graph.auto(),
            data=batch_relationships,
            rel_type="MEMBER_OF",
            start_node_key=("Participant", "phone_number"),
            end_node_key=("Group", "group_id")
        )


def insert_nodes_into_graph(graph: Graph, serialized_groups: dict,
                            contacts: Optional[Dict[str, str]],
                            batch_size: int = DEFAULT_BATCH_SIZE):
    """
    Create and insert nodes (Participant/Group) into the neo4j database using py2neo bulk functions
    :param graph: represents connection to neo4j backend
    :param serialized_groups: scraper's output
    :param contacts: a dictionary converting from phone number to name
    :param batch_size: batch size to upload items in bulk to DB
    """
    participants = defaultdict(lambda: defaultdict(dict))
    groups = []

    for group_id, group_properties in serialized_groups.items():
        if 'participants' in group_properties:
            group_name = group_properties.get('group_name', None)
            group_participants_numbers = group_properties['participants']

            for participant_number in group_participants_numbers:
                if participant_number not in participants:
                    # Prepare participant data for bulk insertion
                    participants[participant_number]['phone_number'] = participant_number
                    if contacts is not None:
                        participants[participant_number]['name'] = contacts.get(participant_number, None)
            # Prepare group data for bulk insertion
            groups.append(dict(name=group_name, group_id=group_id))

    # Create participants nodes
    participants_list = participants.values()
    print(f"Inserting {len(participants_list)} participants into DB...")
    for batch_participants in tqdm(list(divide_into_batches(list(participants_list), batch_size=batch_size))):
        create_nodes(graph.auto(), batch_participants, labels={"Participant"})

    # Create groups nodes
    print(f"Inserting {len(groups)} groups into DB...")
    for batch_groups in tqdm(list(divide_into_batches(groups, batch_size=batch_size))):
        create_nodes(graph.auto(), batch_groups, labels={"Group"})


def main():
    parser = argparse.ArgumentParser(description="Insert group data into Neo4J DB")
    parser.add_argument("data", nargs="+", type=str, help="paths to data (.json) files")
    parser.add_argument("-c", "--contacts", nargs="*", type=str,
                        help="paths to contacts (.json) files, so that the first "
                             "file overrides names of identical contacts in other "
                             "files")
    parser.add_argument("-H", "--host", default="localhost", type=str, help="address of host with neo4j backend")
    parser.add_argument("-u", "--username", default="neo4j", type=str, help="username for the neo4j database")
    parser.add_argument("-p", "--password", default="neo4j", type=str, help="password for the neo4j database")
    args = parser.parse_args()

    contacts = None
    if args.contacts:
        contacts = merge_json_files(*args.contacts)

    serialized_groups = merge_json_files(*args.data)
    graph = Graph(host=args.host, user=args.username, password=args.password)

    insert_nodes_into_graph(graph=graph, serialized_groups=serialized_groups, contacts=contacts)
    insert_relationships_into_graph(graph=graph, serialized_groups=serialized_groups)

    print("Finished insertion!")


if __name__ == '__main__':
    main()
