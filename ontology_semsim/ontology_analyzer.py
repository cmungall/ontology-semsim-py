import click
import logging
from typing import Optional, Set, List, Union, Dict, Any
from rdflib import URIRef, BNode, Literal, Graph, RDFS, OWL, Namespace
from ontology_semsim.semsim_rdflib import RdfSemSimEngine
from ontology_semsim.fast_semsim import FastSemSimEngine
BFO = Namespace("http://purl.obolibrary.org/obo/BFO_")
SUBCLASS_OF = RDFS['subClassOf'].toPython()
PART_OF = BFO['0000050'].toPython()
rels = frozenset({SUBCLASS_OF, PART_OF})

logger = logging.getLogger(__name__)

def result_to_str( sse, tup ):
    j, x, y, mrca = tup
    xl = sse.label(x)
    yl = sse.label(y)
    if mrca is not None:
        ml = sse.label(mrca)
    else:
        ml = None
    mrcas = sse.mrca(x,y,rels) - {mrca}
    lmrcas = [f'{c} "{sse.label(c)}"' for c in mrcas]
    return f'{j} {x} "{xl}" <-> {y} "{yl}" :: {mrca} "{ml}" ADD: {lmrcas}'
    

def find_missing_groupings(sse):
    """
    Finds pairs of classes that share properties in common, where there is no MRCA that
    shares the same properties.

    This indicates a potential new MRCA to be added to the ontology
    """
    cs = sse.cls_set()
    pairs = []
    for x in cs:
        logging.info(f'Base: {x}')
        for y in cs:
            best_j, best_mrca = sse.cls_overlap_vs_mrca(x,y,rels)
            if best_j <= 0.85 and best_j > 0.0:
                simj = sse.cls_wise_jaccard(x,y,rels)
                if simj > 0.60:
                    pairs.append( (best_j, x, y, best_mrca) )
                    logger.info(result_to_str( sse, (best_j, x, y, best_mrca) ))
    pairs.sort(key=lambda tup: tup[0])
    return pairs[:100]

def show_missing_groupings(sse):
    l = find_missing_groupings(sse)
    for j, x, y, mrca in l:
        xl = sse.label(x)
        yl = sse.label(y)
        if mrca is not None:
            ml = sse.label(mrca)
        else:
            ml = None
        print(result_to_str(sse, (j, x, y, mrca)))


@click.command()
@click.option('--input', '-i')
def findall(input):
    logging.basicConfig(level=logging.INFO)
    g = Graph()
    logging.info(f'Parsing {input}')
    g.parse(input, format="xml")
    sse = FastSemSimEngine(RdfSemSimEngine(g))
    show_missing_groupings(sse)


if __name__ == '__main__':
    findall()
                
        
