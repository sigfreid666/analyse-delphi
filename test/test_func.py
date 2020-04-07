import pytest
import analyse_code

@pytest.fixture
def unit3():
    unit = analyse_code.unite('./test/unit3.pas')
    unit.analyse_type_interface()
    return unit

def test_func(unit3):
    assert unit3 is not None
    assert [x for x in unit3.symbols.symbol.keys()] == ['Proc1', 'Proc2', 'Proc3', 'Proc4', 'Proc5', 'Proc6', 'Proc7', 'Proc8' ]
    assert len(unit3.symbols.symbol['Proc8']) == 2
