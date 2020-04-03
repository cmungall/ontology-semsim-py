from ontology_semsim.util import time_all_ancestors, time_all_jaccard
from ontology_semsim.fast_semsim import FastSemSimEngine
from pytest import approx
from typing import Optional, Set, List, Union, Dict, Any
from rdflib import URIRef, BNode, Literal, Graph, RDFS, OWL, Namespace
from ontology_semsim.semsim_rdflib import RdfSemSimEngine
from pytest import approx
import logging

g = Graph()
g.parse("tests/data/chromosome.owl", format="xml")
GO = Namespace("http://purl.obolibrary.org/obo/GO_")
BFO = Namespace("http://purl.obolibrary.org/obo/BFO_")
NC = GO['0000228'].toPython()
MC = GO['0000262'].toPython()
Ch = GO['0005694'].toPython()
Mt = GO['0005739'].toPython()
SUBCLASS_OF = RDFS['subClassOf'].toPython()
PART_OF = BFO['0000050'].toPython()
logging.basicConfig(level=logging.INFO)


def test_timings():
    print('')
    rdf_sse = RdfSemSimEngine(g)
    rpt('rdf0', rdf_sse)
    rpt('rdf1', rdf_sse)
    rpt('rdf2', rdf_sse)
    rpt('rdf3', rdf_sse)
    rdf_sse = RdfSemSimEngine(g)
    fast_sse = FastSemSimEngine(rdf_sse)
    rpt('fast0', fast_sse)
    rpt('fast1', fast_sse)
    rpt('fast2', fast_sse)
    rpt('fast3', fast_sse)

    
# to see output: pytest -s  tests/test_speed.py 
def rpt(n, sse):
    t = time_all_ancestors(sse)
    print(f'A {n} :: {t}')
    t = time_all_jaccard(sse)
    print(f'J {n} :: {t}')
    
