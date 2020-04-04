import re
from pathlib import Path
import pickle
import codecs

import logging
  
class cFonctionImpl:
    def __init__(self, nom, info_utilitaire):
        super().__init__(*info_utilitaire)
        self.nom = nom
        self.pos_var = 0
        self.pos_first_begin = 0
        self.pos_last_end = 0
        self.fct_local = []
        logger.debug('Implementation fonction analyse : %s', self.data[:50])
        liste_begin_end = [(res_end_inter.groups()[0], res_end_inter.start(0)) for res_end_inter in re.finditer('(FUNCTION|TRY|CASE|PROCEDURE|VAR|BEGIN|END|TYPE)+', self.data)]
        self._analyse_begin_end(liste_begin_end)
                   
    def __repr__(self):
        return '<%s,%d,%d,%d,%d>' % (self.nom, self.pos_var, self.pos_first_begin, self.pos_last_end, len(self.fct_local))

    def __str__(self):
        return 'FCT IMPL <%s> repr <%s> ligne debut <%d> ligne fin <%d>' % (self.nom, self.__repr__(), self.num_ligne(0), self.num_ligne(len(self.data)))

    def _analyse_begin_end(self, liste_terme):
        logger.debug('analyse begin end : %d terme(s)', len(liste_terme))
        nb_begin_end = 0
        self.pos_first_begin = liste_terme[-1][1]
        self.pos_last_end = liste_terme[-1][1]
        self.pos_var = 0
        position = 0
        while position < len(liste_terme):
            element = liste_terme[position]
            if (element[0] == 'BEGIN') or (element[0] == 'TRY') or (element[0] == 'CASE'):
                self.pos_first_begin = min(self.pos_first_begin, element[1])
                nb_begin_end += 1
            if element[0] == 'END':
                nb_begin_end -= 1
                if nb_begin_end == 0:
                    self.pos_last_end = element[1]
                    logger.debug('fin analyse : premier begin %d dernier end %d pos var %d', self.pos_first_begin, self.pos_last_end, self.pos_var)
                    return (position, self.pos_first_begin, self.pos_last_end, self.pos_var)
            if (element[0] == 'PROCEDURE') or (element[0] == 'FUNCTION'):
                self.fct_local.append(self._analyse_begin_end(liste_terme[position + 1:]))
                position = self.fct_local[-1][0] + position
            if element[0] == 'VAR':
                self.pos_var = element[1]
            position += 1
        logger.debug('fin analyse : premier begin %d dernier end %d pos var %d', self.pos_first_begin, self.pos_last_end, self.pos_var)
        return (position, self.pos_first_begin, self.pos_last_end, self.pos_var)

class cFonction:
    def __init__(self, nom, params, info_utilitaire):
        super().__init__(*info_utilitaire)
        self.nom = nom
        self.params = params
        self.offset_decl_deb = info_utilitaire[2]
        self.offset_decl_fin = info_utilitaire[3]
        self.parametres = []
        self.offset_impl_deb = 0
        self.offset_impl_fin = 0
        self.implementation = None

        # analyse des parametres
        # logger.debug('analyse des parametres')
        # for param1 in self.params.split(';'):
        #     logger.debug('param')

    def __repr__(self):
        return '<%s,%d,%d>' % (self.nom, self.offset_decl_deb, self.offset_decl_fin)

    def __str__(self):
        chaine = 'FCT <%s> params <%d> offset <%d> <%d> ligne <%d>' % (self.nom, len(self.params), self.offset_decl_deb, self.offset_decl_fin, self.num_ligne(0))
        if self.implementation is not None:
            chaine += '\n\t' + str(self.implementation)
        return chaine










class cEnsembleUnite:
    def __init__(self, repertoire, cache_unite=True):
        self.repertoire = repertoire
        self.nom_dpr = ''
        self.nom_fichier_dpr = ''
        self.unites = {}

        self.nom_fichier = Path(repertoire) / Path('unite.pickle')
        if cache_unite:
            if self.nom_fichier.exists():
                with open(str(self.nom_fichier), 'rb') as f:
                    self.unites = pickle.load(f)

    def save(self):
        logger.info('sauvegarde : <%d> unite(s)', len(self.unites))
        with self.nom_fichier.open(mode='wb') as f:
            pickle.dump(self.unites, f)


    def analyser_repertoire(self):
        logger.info('ensemble unite : %s', self.repertoire)
        def parcour(p_repertoire):
            for x in Path(p_repertoire).iterdir():
                if (not x.is_dir()) and x.match('*.pas'):
                    self.unites[str(x)] = unite(str(x))
                    logger.debug('trouver : %s dans %s', x.name, p_repertoire)
                elif x.is_dir() and (not x.name.startswith('.')):
                    parcour(x)
        parcour(self.repertoire)

    def analyser(self, avec_type_interface=False):
        for un in self.unites:
            self.unites[un] = unite(un)   
            if avec_type_interface:
                self.unites[un].analyse_type_interface()
            break

    def lire_dpr(self, nom_fichier_dpr, recharger=False):
        self.nom_fichier_dpr = nom_fichier_dpr
        with open(str(Path(self.repertoire) / Path(nom_fichier_dpr)), 'r') as f:
            logger.info('Ouverture du fichier dpr <%s>', nom_fichier_dpr)
            data = f.read()
            # on cherche le nom du programme
            program_pos = re.search(r'PROGRAM\s+(\w+?);', data, re.IGNORECASE)
            if program_pos is not None:
                self.nom_dpr = program_pos.groups()[0]
                logger.debug('Tag PROGRAM trouve nom <%s>', self.nom_dpr)
            else:
                raise Exception('nom du dpr non trouve')
            # on parcours les USES
            uses_pos = re.search(r'USES\s+', data, re.IGNORECASE)
            if uses_pos is not None:
                logger.debug('Tag USES trouve pos <%d>', uses_pos.start(0))
                unit_trouve = 0
                for unit_pos in re.finditer(r'([\.\w]+)\s+IN\s+\'([\\\/\:\.\w]+)\'\s*(?:\{.*?\})?\s*(?:,|;)', data[uses_pos.end(0):], re.IGNORECASE):
                    try:
                        if recharger or (unit_pos.groups()[0].upper() not in self.unites):
                            self.unites[unit_pos.groups()[0].upper()] = unite(unit_pos.groups()[1])
                        logger.debug('unite trouve <%s> <%s>', unit_pos.groups()[0], unit_pos.groups()[1])
                        unit_trouve += 1
                    except FileNotFoundError:
                        logger.error('le fichier <%s> n''existe pas', unit_pos.groups()[0])
                    except Exception as e:
                        logger.error('impossibe d''analyser l''unite <%s>', unit_pos.groups()[0])
                        raise e
                logger.info('Nombre de unit trouve : <%d>', unit_trouve)

    def check_uses(self):
        for unite in self.unites:
            if self.unites[unite].uses_interface is not None:
                for uses in self.unites[unite].uses_interface.list_uses:
                    if uses not in self.unites:
                        logger.error('impossible de trouve <%s> dans <%s>', uses, unite)
            if self.unites[unite].uses_implementation is not None:
                for uses in self.unites[unite].uses_implementation.list_uses:
                    if uses not in self.unites:
                        logger.error('impossible de trouve <%s> dans <%s>', uses, unite)

    def check_uses_non_utilise(self):
        stat = list(self.unites.keys())
        for unite in self.unites:
            logger.debug('unite %s', unite)
            # if unite not in stat:
            #     continue
            logger.debug('on continue')
            if self.unites[unite].uses_interface is not None:
                for uses in self.unites[unite].uses_interface.list_uses:
                    logger.debug('verif uses interface %s', uses)
                    if (uses.upper() in self.unites) and (uses.upper() in stat):
                        stat.remove(uses.upper())
                        if unite not in self.unites[uses.upper()].liste_unite:
                            self.unites[uses.upper()].liste_unite.append(unite)
                        logger.debug('remove %s', uses)
                    elif uses.upper() not in self.unites:
                        logger.error('uses <%s> non trouve dans les unites dans le fichier <%s>', uses, unite)
            if self.unites[unite].uses_implementation is not None:
                for uses in self.unites[unite].uses_implementation.list_uses:
                    logger.debug('verif uses implementation %s', uses)
                    if (uses.upper() in self.unites) and (uses.upper() in stat):
                        logger.debug('remove %s', uses)
                        stat.remove(uses.upper())
                        if unite not in self.unites[uses.upper()].liste_unite:
                            self.unites[uses.upper()].liste_unite.append(unite)
                    elif uses.upper() not in self.unites:
                        logger.error('uses <%s> non trouve dans les unites dans le fichier <%s>', uses, unite)
        logger.info('check_uses_non_utilise : <%d> trouves, <%s>', len(stat), str(stat))

    def __str__(self):
        chaine = 'rep <%s> nombre unite <%d>' % (self.repertoire, len(self.unites))
        for un in self.unites:
            chaine = chaine + '\n' + str(self.unites[un])
        return chaine


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
