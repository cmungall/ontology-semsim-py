import semsim

class FastSemSimEngine(SemSimEngine):
    """
    this wraps an existing SemSimEngine and implements faster bitwise operations over it
    """

    def cls_wise_jaccard(x : Cls, y : Cls, rel=None : RelationPattern) -> float :
        """
        Jaccard similarity between two ontology classes
        """
        xa = self.ancestors(x, rel, True)
        ya = self.ancestors(y, rel, True)
        return self.set_jaccard(xa, ya)
    

    def ancestors(c : Cls, rel=None : RelationPattern) -> Set[Cls]:
        return impl.ancestors(c, rel, reflexive)

    def parents(c : Cls, rel=None : RelationPattern) -> Set[Cls]:
        return impl.parents(c, rel)
        
