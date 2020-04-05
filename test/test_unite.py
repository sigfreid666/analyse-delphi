import pytest
import analyse_code

@pytest.fixture
def unit1():
    return analyse_code.unite('./test/unit1.pas')
    
def test_unite_analyse(unit1):
    assert unit1 is not None

def test_unite_nom(unit1):
    assert unit1.nom == 'unit1'

def test_unite_uses(unit1):
    assert unit1.uses_interface is not None
    assert unit1.uses_implementation is not None
    assert len(unit1.uses_interface.list_uses) == 2
    assert len(unit1.uses_implementation.list_uses) == 3
    assert unit1.uses_interface.list_uses == ['uses1', 'uses2']
    assert unit1.uses_implementation.list_uses == ['uses3', 'uses4', 'uses5']
