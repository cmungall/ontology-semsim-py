from typing import Optional, Set, List, Union, Dict, Any
from functools import lru_cache

Cls = str
RelationPattern = str

class SemSimEngine:
    """
    Base class for semantic similarity

    This is neutral w.r.t how the graph is stored; e.g.
     - networkx
     - rdflib object
     - external triplestore or database...

    It assumes a very minimal datamodel : a graph labeled with edges

    """

    def set_wise_jaccard(set1: Set, set2: Set) -> float:
        """
        Jaccard similarity between two sets
        """
        return len(set1 & set2)/len(set1 | set2)
    
    def cls_wise_jaccard(x : Cls, y : Cls, rel : RelationPattern = None) -> float :
        """
        Jaccard similarity between two ontology classes
        """
        xa = self.ancestors(x, rel, True)
        ya = self.ancestors(y, rel, True)
        return self.set_jaccard(xa, ya)

    def mrca(x : Cls, y : Cls, rel : RelationPattern = None) -> Set[Cls] :
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

    @lru_cache()
    def ancestors(c : Cls, rel : RelationPattern = None, reflexive : bool =False) -> Set[Cls] :
        """
        All ancestors for a class, overspecified relations

        This is the transitive closure of parents
        """
        ancs = set() # Set[Cls]
        stk = [c]
        while len(stk) > 0:
            x = stk.pop()
            if x not in ancs:
                parents = self.parents(x, rel)
                stk += parents
                ancs.update(parents)
        if reflexive:
            ancs += {c}
        return ancs

    def parents(c : Cls, rel : RelationPattern = None) -> Set[Cls]:
        """
        direct parents
        """
        # this should be implemented in a subclass
        return set()
    
