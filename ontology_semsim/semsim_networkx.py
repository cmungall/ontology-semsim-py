import semsim

class NetworkxSemSimEngine(SemSimEngine):
    """
    Assumes that an ontology has already been loaded into a networkx object
    """

    def parents(c : Cls, rel=None : RelationPattern) -> Set[Cls]:
        """
        direct parents
        """
        None
