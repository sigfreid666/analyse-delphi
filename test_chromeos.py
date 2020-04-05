import analyse_code

retour = analyse_code.unite('./FrameSco_CoursNonAssures.pas')
print('ca marche')
print(retour)

ensemble = None
ensemble = analyse_code.cEnsembleUnite('/home/sigfreids/code_delphi/dev', repertoire_remplacement='C:\\Projets\\Produits\\DEV', change_slash=True)
ensemble.lire_dpr('MonoposteEdT.dpr')

# ensemble.check_uses_non_utilise()
ensemble.save()
