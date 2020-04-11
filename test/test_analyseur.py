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
        return data.analyse(analyse_code.analyseur_unit)
    return _make_data

def test_func(data):
    data = data('./test/unit_analyseur_1.pas')
    assert data is not None
    assert len([x for x in filter(lambda x: x[0] == 'unit', data)]) == 1
    assert len([x for x in filter(lambda x: x[0] == 'interface', data)]) == 1
    assert len([x for x in filter(lambda x: x[0] == 'implementation', data)]) == 1

def test_func(data):
    data = data('./test/unit_analyseur_2.pas')
    assert data is not None
    assert len([x for x in filter(lambda x: x[0] == 'unit', data)]) == 1
    assert len([x for x in filter(lambda x: x[0] == 'interface', data)]) == 1
    assert len([x for x in filter(lambda x: x[0] == 'implementation', data)]) == 1
    assert len([x for x in filter(lambda x: x[0] == 'uses', data)]) == 2

def test_func(data):
    data = data('./test/unit_analyseur_3.pas')
    assert data is not None
    assert len([x for x in filter(lambda x: x[0] == 'function', data)]) == 1
