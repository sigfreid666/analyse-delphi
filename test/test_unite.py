import pytest
import analyse_code

@pytest.fixture
def unit1():
    return analyse_code.unite('./test/unit1.pas')
    
@pytest.fixture
def unit2():
    unit = analyse_code.unite('./test/unit2.pas')
    # unit.analyse_type_interface()
    return unit
    
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

def test_unite_classe1(unit2):
    assert unit2.liste_type_interface is not None
    assert len(unit2.liste_type_interface.chercher('Classe1')) == 1 
    assert len(unit2.liste_type_interface.chercher('Classe1',cat_type=analyse_code.cType.T_CLASS)) == 1 

def test_unite_classe2(unit2):
    assert unit2.liste_type_interface is not None
    assert len(unit2.liste_type_interface.chercher('Classe2')) == 1 
    oClasse2 = unit2.liste_type_interface.chercher('Classe2')[0]
    assert oClasse2.derivee == 'Classe1' 

def test_unite_type_simple(unit2):
    assert unit2.liste_type_interface is not None
    assert len(unit2.liste_type_interface.chercher('TArrayBlabla',cat_type=analyse_code.cType.T_SIMPLE)) == 1 

def test_unite_type_proc_func(unit2):
    assert unit2.liste_type_interface is not None
    assert len(unit2.liste_type_interface.chercher('TProcPB',cat_type=analyse_code.cType.T_SIMPLE)) == 1 
    assert len(unit2.liste_type_interface.chercher('TProcFB',cat_type=analyse_code.cType.T_SIMPLE)) == 1 
    assert len(unit2.liste_type_interface.chercher('TProcP',cat_type=analyse_code.cType.T_SIMPLE)) == 1 
    assert len(unit2.liste_type_interface.chercher('TProcF',cat_type=analyse_code.cType.T_SIMPLE)) == 1 
    assert len(unit2.liste_type_interface.chercher('TProcPBSP',cat_type=analyse_code.cType.T_SIMPLE)) == 1 
    assert len(unit2.liste_type_interface.chercher('TProcFBSP',cat_type=analyse_code.cType.T_SIMPLE)) == 1 
    assert len(unit2.liste_type_interface.chercher('TProcPSP',cat_type=analyse_code.cType.T_SIMPLE)) == 1 
    assert len(unit2.liste_type_interface.chercher('TProcFSP',cat_type=analyse_code.cType.T_SIMPLE)) == 1 

def test_unite_record(unit2):
    assert unit2.liste_type_interface is not None
    assert len(unit2.liste_type_interface.chercher('Record1',cat_type=analyse_code.cType.T_RECORD)) == 1 

def test_unite_interface(unit2):
    assert unit2.liste_type_interface is not None
    assert len(unit2.liste_type_interface.chercher('Interface1',cat_type=analyse_code.cType.T_INTERFACE)) == 1 

def test_setof(unit2):
    assert unit2.liste_type_interface is not None
    lsetof = unit2.liste_type_interface.chercher('TSetof1')
    assert len(lsetof) == 1
    lsetof = lsetof[0]  
    assert lsetof.membre == ['premier', 'deuxieme']
