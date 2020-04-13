# test pour les classes
import pytest
import analyse_code

@pytest.fixture
def unit5():
    return analyse_code.unite('./test/unit5.pas')

@pytest.fixture
def unit6():
    return analyse_code.unite('./test/unit6.pas')

def test_func_dans_classe(unit5):
    assert unit5 is not None
    assert len(unit5.liste_type_interface[0].chercher('tclasse1')) == 1 
    classe = unit5.liste_type_interface[0].chercher('tclasse1')[0]
    assert len(classe.symbols.chercher('maproc1')) == 1
    assert len(classe.symbols.chercher('maproc2')) == 1
    assert len(classe.symbols.chercher('mafunc1')) == 1
    assert len(classe.symbols.chercher('mafunc2')) == 1
    assert len(classe.symbols.chercher('mafunc3')) == 1
    assert len(classe.symbols.chercher('mafunc4')) == 1
    assert len(classe.symbols.chercher('mafunc5')) == 1
    assert len(classe.symbols.chercher('mavar1')) == 1
    assert len(classe.symbols.chercher('mavar2')) == 1
    assert len(classe.symbols.chercher('mavar3')) == 1
    assert len(classe.symbols.chercher('maprop1')) == 1
    assert len(classe.symbols.chercher('maprop2')) == 1
    assert len(classe.symbols.chercher('maprop3')) == 1
    assert len(classe.symbols.chercher('maprop4')) == 1

def test_classe_dans_classe(unit6):
    assert unit6 is not None
    assert len(unit6.liste_type_interface[0].chercher('tclasse1')) == 1 
    classe = unit6.liste_type_interface[0].chercher('tclasse1')[0]
    assert len(classe.symbols.chercher('maproc1')) == 1
    assert len(classe.symbols.chercher('maproc2')) == 1
    assert len(classe.symbols.chercher('mavar1')) == 1
    assert len(classe.symbols.chercher('mavar2')) == 1
    assert len(classe.symbols.chercher('mavar3')) == 1
    assert len(classe.symbols.chercher('mafunc1')) == 1
    assert len(classe.symbols.chercher('mafunc3')) == 1
    assert len(classe.symbols.chercher('mafunc4')) == 0
    assert len(classe.type_local[0].chercher('tclasse2')) == 1 
    classe2 =  classe.type_local[0].chercher('tclasse2')[0] 
    assert len(classe2.symbols.chercher('mafunc4')) == 1 
