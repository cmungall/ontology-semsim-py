from typing import Optional, Set, List, Union, Dict, Any
from rdflib import URIRef, BNode, Literal, Graph, RDFS, OWL, Namespace
from ontology_semsim.semsim_rdflib import RdfSemSimEngine
from ontology_semsim.fast_semsim import FastSemSimEngine
from pytest import approx

g = Graph()
g.parse("tests/data/chromosome.owl", format="xml")
sse = FastSemSimEngine(RdfSemSimEngine(g))
GO = Namespace("http://purl.obolibrary.org/obo/GO_")
BFO = Namespace("http://purl.obolibrary.org/obo/BFO_")
NC = GO['0000228'].toPython()
MC = GO['0000262'].toPython()
Ch = GO['0005694'].toPython()
Mt = GO['0005739'].toPython()
IMBO = GO['0043231'].toPython()
SUBCLASS_OF = RDFS['subClassOf'].toPython()
PART_OF = BFO['0000050'].toPython()

def test_ancestors():
    ancs = sse.ancestors(MC)
    print(f'ANCS {MC} = {ancs}')
    assert Ch in ancs
    assert Mt in ancs
    ancs = sse.ancestors(NC)
    print(f'ANCS {NC} = {ancs}')
    assert Ch in ancs
    assert Mt not in ancs
    assert len(sse.ancestors(Ch) -  sse.ancestors(NC)) == 0
    assert len(sse.ancestors(Ch) -  sse.ancestors(MC)) == 0
    assert NC in sse.ancestors(NC, None, reflexive=True)
    assert NC not in sse.ancestors(NC, None, reflexive=False)
    assert NC not in sse.ancestors(NC, None)

def test_ancestors_sc():
    ancs = sse.ancestors(MC, SUBCLASS_OF)
    print(f'ANCS {MC} = {ancs}')
    assert Ch in ancs
    assert Mt not in ancs
    ancs = sse.ancestors(NC, SUBCLASS_OF)
    print(f'ANCS {NC} = {ancs}')
    assert Ch in ancs
    assert Mt not in ancs
    assert len(sse.ancestors(Ch, SUBCLASS_OF) -  sse.ancestors(NC, SUBCLASS_OF)) == 0
    assert len(sse.ancestors(Ch, SUBCLASS_OF) -  sse.ancestors(MC, SUBCLASS_OF)) == 0
    assert NC in sse.ancestors(NC, SUBCLASS_OF, reflexive=True)
    assert NC not in sse.ancestors(NC, SUBCLASS_OF, reflexive=False)
    assert NC not in sse.ancestors(NC, SUBCLASS_OF)

def test_ancestors_subclass_partof():
    rels = frozenset({SUBCLASS_OF, PART_OF})
    ancs = sse.ancestors(MC, rels)
    print(f'ANCS {MC} = {ancs}')
    assert Ch in ancs
    assert Mt in ancs
    ancs = sse.ancestors(NC, rels)
    print(f'ANCS {NC} = {ancs}')
    assert Ch in ancs
    assert Mt not in ancs
    assert len(sse.ancestors(Ch, rels) -  sse.ancestors(NC, rels)) == 0
    assert len(sse.ancestors(Ch, rels) -  sse.ancestors(MC, rels)) == 0
    assert NC in sse.ancestors(NC, rels, reflexive=True)
    assert NC not in sse.ancestors(NC, rels, reflexive=False)
    assert NC not in sse.ancestors(NC, rels)
    
def test_mrca():
    mrcas = sse.mrca(NC, MC)
    print(f'mrcas = {mrcas}')
    assert len(mrcas) == 3
    assert Ch in mrcas
    assert sse.mrca(NC, NC) == {NC}
    assert sse.mrca(NC, Ch) == {Ch}
    assert sse.mrca(NC, Mt) == {IMBO}
    
def test_jaccard():
    j = sse.cls_wise_jaccard(NC, MC)
    print(f'J = {j}')
    assert j == sse.cls_wise_jaccard(MC, NC)
    assert j == approx(0.56, abs=1e-1)
    assert sse.cls_wise_jaccard(NC, NC) == 1.0
    assert sse.cls_wise_jaccard(NC, Ch) == approx(0.5, abs=1e-1)
    assert sse.subsumed_by_jaccard(Ch, Ch) == 1.0
    assert sse.subsumed_by_jaccard(Ch, MC) == 1.0
    assert sse.subsumed_by_jaccard(Ch, NC) == 1.0
    assert sse.subsumed_by_jaccard(Mt, MC) == 1.0
    assert sse.subsumed_by_jaccard(Mt, MC) == 1.0
    assert sse.subsumed_by_jaccard(MC, NC) < 1.0
    assert sse.subsumed_by_jaccard(NC, MC) < 1.0

