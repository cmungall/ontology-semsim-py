from typing import Optional, Set, List, Union, Dict, Any
from rdflib import URIRef, BNode, Literal, Graph, RDFS, RDF, OWL
from ontology_semsim.semsim import SemSimEngine, Cls, RelationPattern

class RdfSemSimEngine(SemSimEngine):
    """
    Assumes that an ontology has already been loaded into an rdflib object
    """

    def __init__(self, graph : Graph):
        self.graph = graph

    def cls_set(self) -> Set[Cls]:
        cs = set()
        for c, _, _ in self.graph.triples( (None, RDF['type'], OWL['Class']) ):
            if not isinstance(c, Literal) and not isinstance(c, BNode):
                cs.add(c.toPython())
        return cs

    def label(self, c : Cls) -> str:
        # delegate
        return self.graph.label(URIRef(c))
    
    def parents(self, c : Cls, rel : RelationPattern = None) -> Set[Cls]:
        """
        direct parents
        """
        g = self.graph
        cu = URIRef(c)
        parents = set()
        SUBCLASS_OF = RDFS['subClassOf']
        for _, _, pc in g.triples( (cu, SUBCLASS_OF, None) ):
            if not isinstance(pc, Literal) and not isinstance(pc, BNode):
                if self.relmatch(SUBCLASS_OF.toPython(), rel):
                    parents.add(pc.toPython())
            if isinstance(pc, BNode):
                v = g.value(pc, OWL['someValuesFrom'])
                if v is not None:
                    p = g.value(pc, OWL['onProperty'])
                    if p is not None:
                        if self.relmatch(p.toPython(), rel):
                            parents.add(v.toPython())
                            
        return parents
                

