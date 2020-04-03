from typing import Optional, Set, List, Union, Dict, Any
from functools import lru_cache

Cls = str
RelationPattern = Union[str, Set[str]]   # note frozenset should be used
Relation = str

def set_wise_jaccard(set1: Set, set2: Set) -> float:
    """
    Jaccard similarity between two sets
    """
    return len(set1 & set2)/len(set1 | set2)

class SemSimEngine:
    """
    Base class for semantic similarity

    This is neutral w.r.t how the graph is stored; e.g.
     - networkx
     - rdflib object
     - external triplestore or database...

    It assumes a very minimal datamodel : a graph labeled with edges

    """

    def cls_wise_jaccard(self, x : Cls, y : Cls, rel : RelationPattern = None) -> float :
        """
        Jaccard similarity between two ontology classes
        """
        xa = self.ancestors(x, rel, True)
        ya = self.ancestors(y, rel, True)
        return set_wise_jaccard(xa, ya)

    def subsumed_by_jaccard(self, x : Cls, y : Cls, rel : RelationPattern = None) -> float :
        """
        Extent to which x is subsumed by y
        """
        xa = self.ancestors(x, rel, True)
        ya = self.ancestors(y, rel, True)
        return len(xa & ya) / len(xa)
        
    def mrca(self, x : Cls, y : Cls, rel : RelationPattern = None) -> Set[Cls] :
        """
        Most Recent Common Ancestor between two ontology classes
        """
        xa = self.ancestors(x, rel, True)
        ya = self.ancestors(y, rel, True)
        cas = xa.intersection(ya)
        mrcas = set(cas)
        for a in cas:
            mrcas -= self.ancestors(a, rel, False)
        return mrcas

    @lru_cache(maxsize=None)
    def ancestors(self, c : Cls, rel : RelationPattern = None, reflexive : bool =False) -> Set[Cls] :
        """
        All ancestors for a class, overspecified relations

        This is the transitive closure of parents
        """
        ancs = set() # Set[Cls]
        visited = set()
        stk = [c]
        while len(stk) > 0:
            x = stk.pop()
            if x not in visited:
                parents = self.parents(x, rel)
                stk += parents
                visited.add(x)
                ancs.update(parents)
        if reflexive:
            ancs.add(c)
        return ancs

    def parents(self, c : Cls, rel : RelationPattern = None) -> Set[Cls]:
        """
        direct parents
        """
        # this should be implemented in a subclass
        return set()

    def relmatch(self, r : Relation, rq : RelationPattern) -> bool:
        if rq is None:
            return True
        if isinstance(rq, frozenset):
            return r in rq
        if isinstance(rq, set):
            return r in rq
        if isinstance(rq, list):
            return r in rq
        return r == rq

    
