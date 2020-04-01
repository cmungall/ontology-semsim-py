from ontology_semsim.util import make_test_tree_nx, make_cross_product
from pytest import approx

g1 = make_test_tree_nx(3, ['a','b'])
g2 = make_test_tree_nx(3, ['X','Y'])
sse = make_cross_product(g1.graph, g2.graph)

def test_ancestors():
    for n in sse.graph.nodes():
        print(n)
    ancs = sse.ancestors('aaa-XXX')
    print(f'ancs(aaa) = {ancs}')
    assert len(ancs) == 8
    D =  ancs - {'aaa-X', 'a-X', 'aaa-XX', 'a-XX', 'a-XXX', 'aa-XX', 'aa-XXX', 'aa-X'}
    assert len(D) == 0

def test_mrca():
    mrcas = sse.mrca('aaa-XXX', 'aba-XY')
    print(f'mrcas = {mrcas}')
    assert len(mrcas) == 1
    assert mrcas == {'a-X'}
    
