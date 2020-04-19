import pytest
import os
from pathlib import Path
from analyse_code.ensemble_unite import cEnsembleUnite

@pytest.fixture
def make_ensemble_unite():

    def _make(repertoire):
        p = Path(os.getcwd()) / Path('test') / Path(repertoire)
        ens = cEnsembleUnite(str(p), cache_unite=False, repertoire_remplacement=r"C:\Projets\Produits\DEV")
        return ens

    return _make


def test_main1(make_ensemble_unite):
    ens = make_ensemble_unite('ensembleunite')
    ens.lire_dpr('main1.dpr')
    assert ens is not None
    assert ens.nom_dpr == 'main1'
    assert len(ens.unites) == 2
    assert 'UNIT1' in ens.unites    
    assert 'UNIT2' in ens.unites

def test_main1_rep(make_ensemble_unite):
    ens = make_ensemble_unite('ensembleunite')
    ens.analyser_repertoire()
    assert len(ens.unites) == 3
    assert 'UNIT1' in ens.unites    
    assert 'UNIT2' in ens.unites
    assert 'UNIT3' in ens.unites

def test_main2(make_ensemble_unite):
    ens = make_ensemble_unite('ensembleunite')
    ens.lire_dpr('main2.dpr')
    assert ens is not None
    assert len(ens.unites) == 2
    assert 'UNIT1' in ens.unites    
    assert 'UNIT3' in ens.unites

def test_main2_nonutilise(make_ensemble_unite):
    ens = make_ensemble_unite('ensembleunite')
    ens.lire_dpr('main2.dpr')
    ens.check_uses_non_utilise()
    assert ens is not None
    assert len(ens.unites) == 2
    assert ens.unites_non_utilise == ['UNIT1']
    assert ens.unites_non_trouve == []
    assert 'unit4' in ens.unites_uses_non_trouve

def test_main3_nontrouve(make_ensemble_unite):
    ens = make_ensemble_unite('ensembleunite')
    ens.lire_dpr('main3.dpr')
    assert ens is not None
    assert len(ens.unites) == 1
    assert ens.unites_non_trouve == [('unit4',r'C:\Projets\Produits\DEV\unit4_.pas')]

