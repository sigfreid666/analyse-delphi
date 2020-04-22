import pytest
from test_ensembleunite import make_ensemble_unite_dpr 

# @pytest.fixture
# def make_ensemble_unite_dpr():

#     def _make(nom_dpr):
#         p = Path(os.getcwd()) / Path('test') / Path('ensembleunite') / Path(nom_dpr)
#         ens = cEnsembleUniteDpr(p, cache_unite=False, repertoire_remplacement=r"C:\Projets\Produits\DEV")
#         return ens

#     return _make

def test_json1(make_ensemble_unite_dpr):
    dpr = make_ensemble_unite_dpr('main1.dpr')
    assert dpr is not None
    dpr.export_json_tofile('dump.json')