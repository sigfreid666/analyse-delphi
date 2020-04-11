import re

from . import gestion_multiligne
from .log import logger

class cData:
    def __init__(self, lignes, start_point=0, end_point=-1):
        self.ogestionmultiligne = gestion_multiligne.gestion_multiligne(lignes)
        self.data = self.ogestionmultiligne.data
        self.start_point = start_point
        self.end_point = end_point

    def analyse(self, liste_analyseur):
        resultat = []
        position = 0
        for ianalyseur in liste_analyseur:
            # on saute tout espace trouve
            pos_espace = self._match_regex(r'\s+', position, -1)
            if pos_espace is not None:
                logger.debug('saut d espace')
                position = pos_espace[1]
            # si l'element a analyse est une liste 
            if type(ianalyseur) != tuple:
                ianalyseur = [ianalyseur]
                logger.debug('liste d analyseur detecte nb %d', len(ianalyseur))
            # c'est le premier qui dit si l'ensemble est obligatoire
            trouve = not ianalyseur[0].obligatoire
            # on parcours l'un des element doit etre valide pour passer au suivant
            for isous_analyseur in ianalyseur:
                logger.debug('recherche de %s', isous_analyseur.type)
                # le re est une liste d expression reguliere
                for regex in isous_analyseur.re:
                    pos = self._match_regex(regex, position, -1)
                    if pos is not None:
                        break
                # on a trouve quelque chose
                if pos is not None:
                    trouve = True
                    logger.debug('trouve')
                    resultat.append((isous_analyseur.type, pos))
                    position = pos[1]
                    # maintenant on parcours les fils
                    if len(isous_analyseur.fils) > 0:
                        resultat.append(self.analyse(isous_analyseur.fils))
                    break
            if not trouve:
                raise Exception('impossible de trouver %s' % str(ianalyseur[0]))
        return resultat


    def _find_regex(self, str_regex, start_point, end_point):
        logger.info('_find_regex : <%s> <%d> <%d> <%d> <%d>', str_regex, start_point, end_point, self.ogestionmultiligne.num_ligne(start_point), self.ogestionmultiligne.num_ligne(end_point))
        start = self.start_point + start_point
        end = self.end_point if end_point == -1 else self.start_point + end_point
        logger.debug('_find_regex : <%d> <%d> <%s>', start, end, self.data[start:start+50])
        match_obj = re.search(str_regex, self.data[start:end], flags=re.IGNORECASE)
        if match_obj is not None:
            res = (match_obj.start(0) + start, match_obj.end(0) + start, self.ogestionmultiligne.num_ligne(match_obj.start(0) + start), match_obj.groups())
            logger.debug('trouve : %s', str(res))
            return res
        logger.debug('pas trouve !!')
        return None

    def _match_regex(self, str_regex, start_point, end_point):
        logger.info('_match_regex : <%s> <%d> <%d> <%d> <%d>', str_regex, start_point, end_point, self.ogestionmultiligne.num_ligne(start_point), self.ogestionmultiligne.num_ligne(end_point))
        start = self.start_point + start_point
        end = self.end_point if end_point == -1 else self.start_point + end_point
        logger.debug('_match_regex : <%d> <%d> <%s>', start, end, self.data[start:start+50])
        match_obj = re.match(str_regex, self.data[start:end], flags=re.IGNORECASE)
        if match_obj is not None:
            res = (match_obj.start(0) + start, match_obj.end(0) + start, self.ogestionmultiligne.num_ligne(match_obj.start(0) + start), match_obj.groups())
            logger.debug('trouve : %s', str(res))
            return res
        logger.debug('pas trouve !!')
        return None

    def genere_fils(self, new_start_point, new_end_point):
        return cData(self.ogestionmultiligne, new_start_point, new_end_point)

    def num_ligne(self, indice):
        return self.ogestionmultiligne.num_ligne(indice)

