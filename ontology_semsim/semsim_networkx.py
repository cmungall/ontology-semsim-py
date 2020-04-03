from typing import Optional, Set, List, Union, Dict, Any
from ontology_semsim.semsim import SemSimEngine, Cls, RelationPattern

class NetworkxSemSimEngine(SemSimEngine):
    """
    Assumes that an ontology has already been loaded into a networkx object
    """

    def __init__(self, graph):
        self.graph = graph

    def parents(self, c : Cls, rel : RelationPattern = None) -> Set[Cls]:
        """
        direct parents
        """
        # TODO rel
        return set(self.graph.predecessors(c))

