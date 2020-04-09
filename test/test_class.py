# test pour les classes
import pytest
import analyse_code

@pytest.fixture
def unit5():
    unit = analyse_code.unite('./test/unit5.pas')
    unit.analyse_type_interface()
    return unit

def test_func_dans_classe(unit5):
    assert unit5 is not None
    assert len(unit5.liste_type_interface[0].chercher('tclasse1')) == 1 
    classe = unit5.liste_type_interface[0].chercher('tclasse1')[0]
    classe.analyse_section()
    assert len(classe.symbols.chercher('maproc1')) == 1
    assert len(classe.symbols.chercher('maproc2')) == 1
    assert len(classe.symbols.chercher('mafunc1')) == 1
    assert len(classe.symbols.chercher('mafunc2')) == 1
    assert len(classe.symbols.chercher('mafunc3')) == 1
    assert len(classe.symbols.chercher('mafunc4')) == 1
