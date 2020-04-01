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
                G.add_edge(p, c, relation='subClassOf')
        leaf_nodes = nu_leaf_nodes
        depth -= 1
    return NetworkxSemSimEngine(G)

def mk_node(n1 : str, n2 : str):
    return f'{n1}-{n2}'

def make_cross_product(g1, g2):
    G = nx.MultiDiGraph()
    for n1 in g1.nodes():
        for n2 in g2.nodes():
            n = mk_node(n1,n2)
            G.add_node(n)
            for n1p in g1.predecessors(n1):
                G.add_edge(mk_node(n1p, n2), n)
            for n2p in g2.predecessors(n2):
                G.add_edge(mk_node(n1, n2p), n)
    return NetworkxSemSimEngine(G)

