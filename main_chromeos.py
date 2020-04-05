import analyse_code

def test_unite():
    retour = analyse_code.unite('./FrameSco_CoursNonAssures.pas')
    assert retour is not None

# ensemble = None
# ensemble = analyse_code.cEnsembleUnite('/home/sigfreids/code_delphi/dev', repertoire_remplacement='C:\\Projets\\Produits\\DEV', change_slash=True)
# ensemble.lire_dpr('MonoposteEdT.dpr')

# # ensemble.check_uses_non_utilise()
# ensemble.save()
