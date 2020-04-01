import semsim

class RdfSemSimEngine(SemSimEngine):
    """
    Assumes that an ontology has already been loaded into an rdflib object
    """

    def parents(c : Cls, rel=None : RelationPattern) -> Set[Cls]:
        """
        direct parents
        """
        None

    def materialize_relational_graph():
        """
        turns C subClassOf R Some D ==> C R D
        """
        None

