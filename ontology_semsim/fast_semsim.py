import semsim
"""
Implements a semsim emngine using fast(?) bitwise operations

See owlsim3 docs

Sets are represented as integers, where the integer is a bitmap,
such that if each element of the set E is assigned a unique non-negative integer I,
the set contains the element if the bit 2^I is set
"""

Bitmap = int
Pos = int

STEP = 16

def len_bm(bm : Bitmap) -> int:
    """
    calculates number of 'on' bits in a bitmap.
    When the bitmap represents a set, this is the length of the set
    """
    len_bm = 0
    while bm > 0:
        len_bm += len_bm_lo(bm)
        bm = bm >> STEP
    return len_bm

@lru_cache()
def len_bm_lo(bm : Bitmap) -> int:
    MASK = 2 ** STEP -1
    bm_lo = bm & MASK
    len_lo = 0
    while bm_lo > 0:
        len_lo += bm_lo & 1
        bm_lo = bm_lo >> 1
    return len_lo


class FastSemSimEngine(SemSimEngine):
    """
    this wraps an existing SemSimEngine and implements faster bitwise operations over it.

    It exposes the same operations
    """

    def __init__(self, engine : SemSimEngine):
        self.impl = engine
        self.cls_to_pos_map = {}
        self.pos_to_cls_ix = []
        self.max_pos = -1
    
    def cls_bm(c : Cls) -> Pos:
        """
        Given a class, return its bitmap index
        """
        if c in self.cls_to_pos_map:
            return self.cls_to_pos_map[c]
        else:
            # does not exist: add it
            self.max_pos += 1
            p = self.max_pos
            self.cls_to_pos_map[c] = p
            self.pos_to_cls_ix[p] = c
            return p


    def create_index() :
        # todo: operations are more efficient if we pre-index all classes
        # in order of IC
        return

    def bm_jaccard(xi: Bitmap, yi: Bitmap) -> float:
        """
        Jaccard similarity between two sets
        """
        return self.len_bm(set1 & set2)/self.len_bm(set1 | set2)
    
    def cls_wise_jaccard(x : Cls, y : Cls, rel=None : RelationPattern) -> float :
        """
        Jaccard similarity between two ontology classes
        """
        xa = self.ancestors_bm(x, rel, True)
        ya = self.ancestors_bm(y, rel, True)
        return self.bm_jaccard(xa, ya)

    def mrca(x : Cls, y : Cls, rel : RelationPattern = None) -> Set[Cls] :
        # delegate
        return impl.mrca(x, y, rel)
               
    def ancestors(c : Cls, rel=None : RelationPattern) -> Set[Cls]:
        # delegate
        return impl.ancestors(c, rel, reflexive)

    # private: ancestors as bitmap
    def ancestors_bm(c : Cls, rel=None : RelationPattern) -> Bitmap:
        ancs = impl.ancestors(c, rel, reflexive)
        bm = 0 # Bitmap
        for a in ancs:
            bm = bm | self.cls_bm(a)
        return bm

    def parents(c : Cls, rel=None : RelationPattern) -> Set[Cls]:
        # delegate
        return impl.parents(c, rel)
        
