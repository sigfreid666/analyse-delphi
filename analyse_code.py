import re
from pathlib import Path
import pickle
import codecs

import logging
  












if __name__ == "__main__":
    logger.info('#### DEBUT #####')
    # try:
    #     # un = unite('C:\\Projets\\Produits\\DEV\\Scolys\\_Delphi\\_ClientsServeurs\\Database\\Requetes\\Requetes_CoursDEleve.pas')
    #     un = unite('C:\\Projets\\Produits\\DEV\\Scolys\\_Delphi\\_ClientsServeurs\\EdT\\_Clients\\_ClientGraphique\\TableAffEDT_VolumesHoraires.pas')
    # except re.error as e:
    #     print(e.pattern)
    # print(un)

    ensemble = None
    ensemble = cEnsembleUnite('C:\\Projets\\Produits\\DEV')
    ensemble.lire_dpr('Scolys\\_Delphi\\_ClientsServeurs\\EdT\\_Clients\\_ClientGraphique\\_Monoposte\\MonoposteEdT.dpr')

    ensemble.check_uses_non_utilise()
    print(codecs.encode(str(ensemble.unites['NetBaseSco'.upper()]), encoding='iso8859', errors='ignore'))

    # ensemble = cEnsembleUnite('/home/sigfreids/code_delphi')
    # ensemble.analyser(avec_type_interface=True)
    # print(ensemble)
    # print(ensemble.unites['FicheSco_AssisstantHoraireAffiche'].uses_interface.analyse_uses(ensemble, ''))

    # for nom_unite in ensemble.unites:
    #     match = re.finditer(r'\.Masquer\s*\(?\s*\)?\s*;', ensemble.unites[nom_unite].data.data, re.IGNORECASE)
    #     taille = [ensemble.unites[nom_unite].data.num_ligne(x.start(0)) for x in match]
    #     if len(taille) > 0:
    #         taille_detaille = []
    #         for x in re.finditer(r'FINALLY.*?(Masquer\s*\(?\s*\)?\s*;).*?END', ensemble.unites[nom_unite].data.data, re.IGNORECASE):
    #             taille_detaille.append(ensemble.unites[nom_unite].data.num_ligne(x.start(1)))
    #         if len(taille) > len(taille_detaille):
    #             print('\tTrouve dans %s <%s>' % (nom_unite, str([x for x in taille if x not in taille_detaille])))

    ensemble.save()
    # un = unite('C:\\Projets\\Produits\\DEV\\Scolys\\_Delphi\\_ClientsServeurs\\FicheSco_AssisstantHoraireAffiche.pas')
    # un = unite('/home/sigfreids/code_delphi/EditSco_Cours.pas')
    # un.analyse_type_interface()
    # print(un)
# with open('Q:\\test.pas', 'w') as f:
#     entire_file = ''
#     with open('C:\\Projets\\Produits\\DEV\\Scolys\\_Delphi\\_ClientsServeurs\\Database\\Requetes\\Requetes_CoursDEleve.pas', 'r') as unite_file:
#         ligne_pre_uses = un.gestion_ml.num_ligne(un.uses_inter_pos[0])
#         pos_pre_uses = un.gestion_ml.pos_num_ligne(ligne_pre_uses + 1)
#         ligne_post_uses = un.gestion_ml.num_ligne(un.uses_inter_pos[1])
#         pos_post_uses = un.gestion_ml.pos_num_ligne(ligne_post_uses + 1)
#         entire_file = unite_file.read()
#     f.write(entire_file[0:pos_pre_uses])
#     f.write(un.uses_interface.analyse_uses(ensemble, '\t\t'))
#     f.write(entire_file[pos_post_uses:])
