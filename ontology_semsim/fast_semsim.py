from typing import Optional, Set, List, Union, Dict, Any
from ontology_semsim.semsim import SemSimEngine, Cls, RelationPattern
from functools import lru_cache

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

@lru_cache(maxsize=None)
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
    
    def cls_bm(self, c : Cls) -> Pos:
        """
        Given a class, return its bitmap index
        """
        if c in self.cls_to_pos_map:
            return self.cls_to_pos_map[c]
        else:
            # does not exist: add it
            p = len(self.cls_to_pos_map) + 1
            self.cls_to_pos_map[c] = p
            self.pos_to_cls_ix.append(c)
            return p

    def cls_set(self) -> Set[Cls]:
        # delegate
        return self.impl.cls_set()

    def label(self, c : Cls) -> str:
        # delegate
        return self.impl.label(c)

    def create_index() :
        # todo: operations are more efficient if we pre-index all classes
        # in order of IC
        return

    def bm_jaccard(self, xi: Bitmap, yi: Bitmap) -> float:
        """
        Jaccard similarity between two sets
        """
        return len_bm(xi & yi)/len_bm(xi | yi)
    
    def cls_wise_jaccard(self, x : Cls, y : Cls, rel : RelationPattern = None) -> float :
        """
        Jaccard similarity between two ontology classes
        """
        xa = self.ancestors_bm(x, rel, reflexive=True)
        ya = self.ancestors_bm(y, rel, reflexive=True)
        return self.bm_jaccard(xa, ya)

    def mrca(self, x : Cls, y : Cls, rel : RelationPattern = None) -> Set[Cls] :
        # delegate
        return self.impl.mrca(x, y, rel)
               
    def ancestors(self, c : Cls, rel : RelationPattern = None, reflexive : bool = False) -> Set[Cls]:
        # delegate
        return self.impl.ancestors(c, rel, reflexive)

    # private: ancestors as bitmap
    @lru_cache(maxsize=None)
    def ancestors_bm(self, c : Cls, rel : RelationPattern = None, reflexive : bool = False) -> Bitmap:
        ancs = self.impl.ancestors(c, rel, reflexive)
        bm = 0 # Bitmap
        for a in ancs:
            bm = bm | 2**self.cls_bm(a)
        return bm

    def parents(self, c : Cls, rel : RelationPattern = None) -> Set[Cls]:
        # delegate
        return self.impl.parents(c, rel)
        
    def cls_overlap_vs_mrca(self, x : Cls, y : Cls, rel : RelationPattern = None):
        ovl = self.ancestors_bm(x, rel, reflexive=True) & self.ancestors_bm(y, rel, reflexive=True)
        mrcas = self.mrca(x,y, rel)

        best_j = 0
        best_mrca = None
        
        for mrca in mrcas:
            ancs = self.ancestors_bm(mrca, rel, reflexive=True)
            mj = len_bm(ancs & ovl) / len_bm(ancs | ovl)
            if mj > best_j:
                best_j = mj
                best_mrca = mrca
        return (best_j, best_mrca)
        
