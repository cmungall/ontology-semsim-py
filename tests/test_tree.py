from ontology_semsim.util import make_test_tree_nx
from pytest import approx

sse = make_test_tree_nx(5, ['a','b'])
G = sse.graph

def test_ancestors():
    ancs = sse.ancestors('aaa')
    print(f'ancs(aaa) = {ancs}')
    assert len(ancs) == 2
    assert 'aa' in ancs
    assert 'a' in ancs
    ancs = sse.ancestors('aab', reflexive=True)
    print(f'ancs(aaa) = {ancs}')
    assert len(ancs) == 3
    assert 'aab' in ancs
    assert 'aa' in ancs
    assert 'a' in ancs

def test_mrca():
    mrcas = sse.mrca('aaabb', 'aaaa')
    print(f'mrcas = {mrcas}')
    assert len(mrcas) == 1
    assert mrcas == {'aaa'}
    
def test_jaccard():
    j = sse.cls_wise_jaccard('aaabb', 'aaaa')
    print(f'J = {j}')
    assert j == 0.5
    assert sse.cls_wise_jaccard('bbbbb', 'bbbbb') == 1.0
    assert sse.cls_wise_jaccard('a', 'a') == 1.0
    assert sse.cls_wise_jaccard('a', 'b') == 0.0
    assert sse.cls_wise_jaccard('aa', 'bb') == 0.0
    assert sse.cls_wise_jaccard('aa', 'ab') == approx(0.3333, abs=1e-3)

    
