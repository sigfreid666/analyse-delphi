import pytest
import analyse_code

@pytest.fixture
def unit3():
    unit = analyse_code.unite('./test/unit3.pas')
    return unit

@pytest.fixture
def unit4():
    unit = analyse_code.unite('./test/unit4.pas')
    return unit

def test_func(unit3):
    assert unit3 is not None
    assert 'Proc1' in unit3.symbols.symbol
    assert 'Proc2' in unit3.symbols.symbol
    assert 'Proc3' in unit3.symbols.symbol
    assert 'Proc4' in unit3.symbols.symbol
    assert 'Proc5' in unit3.symbols.symbol
    assert 'Proc6' in unit3.symbols.symbol
    assert 'Proc7' in unit3.symbols.symbol
    assert 'Proc8' in unit3.symbols.symbol
    assert 'Func1' in unit3.symbols.symbol
    assert 'Func2' in unit3.symbols.symbol
    assert 'Func3' in unit3.symbols.symbol
    assert 'Func4' in unit3.symbols.symbol
    assert 'Func5' in unit3.symbols.symbol
    assert 'Func6' in unit3.symbols.symbol
    assert 'Func7' in unit3.symbols.symbol
    assert 'Func8' in unit3.symbols.symbol
    assert len(unit3.symbols.symbol['Proc8']) == 2

def test_func_avec_type(unit4):
    assert unit4 is not None
    assert 'Proc1' in unit4.symbols.symbol
    assert 'Proc2' in unit4.symbols.symbol
    assert 'Proc3' in unit4.symbols.symbol
    assert 'Proc4' in unit4.symbols.symbol
    assert 'Proc5' in unit4.symbols.symbol
    assert 'Proc6' in unit4.symbols.symbol
    assert 'Proc7' in unit4.symbols.symbol
    assert 'Proc8' in unit4.symbols.symbol
    assert 'Func1' in unit4.symbols.symbol
    assert 'Func2' in unit4.symbols.symbol
    assert 'Func3' in unit4.symbols.symbol
    assert 'Func4' in unit4.symbols.symbol
    assert 'Func5' in unit4.symbols.symbol
    assert 'Func6' in unit4.symbols.symbol
    assert 'Func7' in unit4.symbols.symbol
    assert 'Func8' in unit4.symbols.symbol
    assert len(unit4.symbols.symbol['Proc8']) == 2
    assert len(unit4.liste_type_interface[0].chercher('TClass1')) == 1 
    assert len(unit4.liste_type_interface[1].chercher('TRecord')) == 1 

