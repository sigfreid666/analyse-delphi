# test pour les classes
import pytest
import analyse_code

@pytest.fixture
def unit():
    def _make_unit(nom_fichier):
        return analyse_code.unite(nom_fichier)
    return _make_unit

def test_func_dans_classe(unit):
    unit5 = unit('./test/unit5.pas')
    assert unit5 is not None
    assert len(unit5.liste_type_interface.chercher('tclasse1')) == 1 
    classe = unit5.liste_type_interface.chercher('tclasse1')[0]
    assert type(classe) == analyse_code.cClasse
    assert classe.derivee == 'maderivee'
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

def test_classe_dans_classe(unit):
    unit6 = unit('./test/unit6.pas')
    assert unit6 is not None
    assert len(unit6.liste_type_interface.chercher('tclasse1')) == 1 
    classe = unit6.liste_type_interface.chercher('tclasse1')[0]
    assert len(classe.symbols.chercher('maproc1')) == 1
    assert len(classe.symbols.chercher('maproc2')) == 1
    assert len(classe.symbols.chercher('mavar1')) == 1
    assert len(classe.symbols.chercher('mavar2')) == 1
    assert len(classe.symbols.chercher('mavar3')) == 1
    assert len(classe.symbols.chercher('mafunc1')) == 1
    assert len(classe.symbols.chercher('mafunc3')) == 1
    assert len(classe.symbols.chercher('mafunc4')) == 0
    assert len(classe.type_local.chercher('tclasse2')) == 1 
    classe2 =  classe.type_local.chercher('tclasse2')[0] 
    assert len(classe2.symbols.chercher('mafunc4')) == 1 
    assert len(classe.symbols.chercher('const1')) == 1
    assert len(classe.symbols.chercher('const2')) == 1
    assert len(classe.symbols.chercher('const3')) == 1

def test_record1(unit):
    unit = unit('./test/unit7.pas')
    assert unit is not None
    assert len(unit.liste_type_interface.chercher('trecord1')) == 1 
    record = unit.liste_type_interface.chercher('trecord1')[0]
    assert type(record) == analyse_code.cRecord
    assert len(record.symbols.chercher('maproc1')) == 1
    assert len(record.symbols.chercher('maproc2')) == 1
    assert len(record.symbols.chercher('mafunc1')) == 1
    assert len(record.symbols.chercher('mafunc2')) == 1
    assert len(record.symbols.chercher('mafunc3')) == 1
    assert len(record.symbols.chercher('mafunc4')) == 1
    assert len(record.symbols.chercher('mafunc5')) == 1
    assert len(record.symbols.chercher('mavar1')) == 1
    assert len(record.symbols.chercher('mavar2')) == 1
    assert len(record.symbols.chercher('mavar3')) == 1
    assert len(record.symbols.chercher('maprop1')) == 1
    assert len(record.symbols.chercher('maprop2')) == 1
    assert len(record.symbols.chercher('maprop3')) == 1
    assert len(record.symbols.chercher('maprop4')) == 1

