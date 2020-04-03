from typing import Optional, Set, List, Union, Dict, Any
from rdflib import URIRef, BNode, Literal, Graph, RDFS, OWL, Namespace
from ontology_semsim.semsim_rdflib import RdfSemSimEngine
from ontology_semsim.util import find_oddities
from pytest import approx

g = Graph()
g.parse("tests/data/chromosome.owl", format="xml")
sse = RdfSemSimEngine(g)
GO = Namespace("http://purl.obolibrary.org/obo/GO_")
BFO = Namespace("http://purl.obolibrary.org/obo/BFO_")
NC = GO['0000228'].toPython()
MC = GO['0000262'].toPython()
Ch = GO['0005694'].toPython()
Mt = GO['0005739'].toPython()
SUBCLASS_OF = RDFS['subClassOf'].toPython()
PART_OF = BFO['0000050'].toPython()

def test_oddities():
    l = find_oddities(sse)
    for j, x, y, mrca in l:
        xl = g.label(URIRef(x))
        yl = g.label(URIRef(y))
        if mrca is not None:
            ml = g.label(URIRef(mrca))
        else:
            ml = None
        print(f'{j} {x} "{xl}" <-> {y} "{yl}" :: {mrca} "{ml}"')
    assert False
