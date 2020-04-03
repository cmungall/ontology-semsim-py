from typing import Optional, Set, List, Union, Dict, Any
from rdflib import URIRef, BNode, Literal, Graph, RDFS, OWL, Namespace
from ontology_semsim.semsim_networkx import NetworkxSemSimEngine
import networkx as nx
SUBCLASS_OF = RDFS['subClassOf'].toPython()
import time

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

def time_all_ancestors(sse):
    t0 = time.time()
    for c in sse.cls_set():
        n_ancs = len(sse.ancestors(c))
    t1 = time.time()
    return t1-t0

def time_all_jaccard(sse):
    t0 = time.time()
    for x in sse.cls_set():
        for y in sse.cls_set():
            j = sse.cls_wise_jaccard(x,y)
    t1 = time.time()
    return t1-t0

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



def find_oddities(sse):
    cs = sse.cls_set()
    pairs = []
    for x in cs:
        for y in cs:
            #j = sse.cls_wise_jaccard(x, y)
            ovl = sse.ancestors(x, None, reflexive=True) & sse.ancestors(y, None, reflexive=True)
            #mrcas = sse.mrca(x,y,SUBCLASS_OF)
            mrcas = sse.mrca(x,y)

            best_j = 0
            best_mrca = None
            for mrca in mrcas:
                ancs = sse.ancestors(mrca, None, reflexive=True)
                j = len(ancs & ovl) / len(ancs | ovl)
                if j > best_j:
                    best_j = j
                    best_mrca = mrca
            pairs.append( (best_j, x, y, best_mrca) )
    pairs.sort(key=lambda tup: tup[0])
    return pairs[:100]
                
        
def find_odditiesXX(sse):
    cs = sse.cls_set()
    pairs = []
    for x in cs:
        for y in cs:
            j = sse.subsumed_by_jaccard(x, y)
            if j < 1.0:
                rj = sse.subsumed_by_jaccard(y, x)
                if rj < 1.0:
                    mrcas = sse.mrca(x,y,SUBCLASS_OF)
                    pairs.append( (j, x, y) )
    pairs.sort(key=lambda tup: tup[0], reverse=True)
    return pairs[:100]
                
        
