import pytest
import os
from pathlib import Path
from analyse_code.ensemble_unite import cEnsembleUnite

def test_main1():
    p = Path(os.getcwd()) / Path('test') / Path('ensembleunite')
    ens = cEnsembleUnite(str(p), cache_unite=False, repertoire_remplacement=r"C:\Projets\Produits\DEV")
    ens.lire_dpr('main1.dpr')
    assert ens is not None
    assert ens.nom_dpr == 'main1'
    assert len(ens.unites) == 2
    assert 'UNIT1' in ens.unites    
    assert 'UNIT2' in ens.unites