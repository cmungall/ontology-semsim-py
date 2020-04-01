from typing import Optional, Set, List, Union, Dict, Any
from ontology_semsim.semsim_networkx import NetworkxSemSimEngine
import networkx as nx

def make_test_tree_nx(depth : int = 8, atoms : Set[str] = ['a', 'b']):
    G = nx.MultiDiGraph()
    for c in atoms:
        G.add_node(c)
    leaf_nodes = atoms
    while depth > 0:
        nu_leaf_nodes = []
        for p in leaf_nodes:
            for a in atoms:
                c = p+a
                nu_leaf_nodes.append(c)
                G.add_node(c)
                G.add_edge(p, c)
        leaf_nodes = nu_leaf_nodes
        depth -= 1
    return NetworkxSemSimEngine(G)
