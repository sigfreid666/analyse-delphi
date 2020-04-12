import pytest
import analyse_code
import codecs

@pytest.fixture
def data():
    def _make_data(file):
        data = None
        with codecs.open(file, 'r', encoding='utf-8-sig') as f:
            lignes = f.readlines()
            data = analyse_code.cData(lignes)
        return data
    return _make_data

def test_func1(data):
    data = data('./test/unit_analyseur_1.pas')
    data = analyse_code.analyseur_unit.analyse(data)[0]
    assert data is not None
    assert len(data.chercher(p_type='unit')) == 1
    assert len(data.chercher(p_type='interface')) == 1
    assert len(data.chercher(p_type='implementation')) == 1

def test_func2(data):
    data = data('./test/unit_analyseur_2.pas')
    data = analyse_code.analyseur_unit.analyse(data)[0]
    assert data is not None
    assert len(data.chercher(p_type='uses')) == 2

def test_func3(data):
    data = data('./test/unit_analyseur_3.pas')
    data = analyse_code.analyseur_unit.analyse(data)[0]
    assert data is not None
    assert len(data.chercher(p_type='function')) == 2
    assert len(data.chercher(p_type='section_type')) == 1
    assert len(data.chercher(p_type='class')) == 1

def test_func4(data):
    data = data('./test/unit_analyseur_4.pas')
    data = analyse_code.analyseur_unit.analyse(data)[0]
    assert data is not None
    assert len(data.chercher(p_type='function')) == 3
    assert len(data.chercher(p_type='section_type')) == 1
    assert len(data.chercher(p_type='class')) == 1
