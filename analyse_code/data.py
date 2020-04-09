import re

from . import gestion_multiligne
from .log import logger
from .regex import *

class cData:
    def __init__(self, ogestionmultiligne, start_point=0, end_point=-1):
        self.ogestionmultiligne = ogestionmultiligne
        self.data = ogestionmultiligne.data
        self.start_point = start_point
        self.end_point = end_point

    def _find_regex(self, str_regex, start_point, end_point):
        logger.info('_find_regex : <%s> <%d> <%d> <%d> <%d>', str_regex, start_point, end_point, self.ogestionmultiligne.num_ligne(start_point), self.ogestionmultiligne.num_ligne(end_point))
        start = self.start_point + start_point
        end = self.end_point if end_point == -1 else self.start_point + end_point
        logger.debug('_find_regex : <%d> <%d> <%s>', start, end, self.data[start:start+50])
        match_obj = re.search(str_regex, self.data[start:end], flags=re.IGNORECASE)
        if match_obj is not None:
            res = (match_obj.start(0) + start_point, match_obj.end(0) + start_point, self.ogestionmultiligne.num_ligne(match_obj.start(0) + start), match_obj.groups())
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
            res = (match_obj.start(0) + start_point, 
                match_obj.end(0) + start_point, 
                self.ogestionmultiligne.num_ligne(match_obj.start(0) + start), match_obj.groups())
            logger.debug('trouve : %s', str(res))
            return res
        logger.debug('pas trouve !!')
        return None

    def _find_function(self, start_point, end_point, impl=''):
        match_obj = None
        verb = 'function'
        liste_group = [ ]
        match_obj_deb = self._find_regex(C_RE_PROCEDURE_FUNCTION_DEB, start_point, end_point)
        if match_obj_deb is not None:
            verb = match_obj_deb[3][0].lower()
            if impl == '':
                if verb == 'function':
                    match_obj = self._match_regex(C_RE_FUNCTION_DECL_S, match_obj_deb[0], end_point)
                    if match_obj is None:
                        match_obj = self._match_regex(C_RE_FUNCTION_DECL, match_obj_deb[0], end_point)
                else:
                    match_obj = self._match_regex(C_RE_PROCEDURE_DECL_S, match_obj_deb[0], end_point)
                    if match_obj is None:
                        match_obj = self._match_regex(C_RE_PROCEDURE_DECL, match_obj_deb[0], end_point)
            else:
                if verb == 'function':
                    match_obj = self._match_regex(C_RE_FUNCTION_IMPL_S % impl, match_obj_deb[0], end_point)
                    if match_obj is None:            
                        match_obj = self._match_regex(C_RE_FUNCTION_IMPL % impl, match_obj_deb[0], end_point)
                else:
                    match_obj = self._match_regex(C_RE_PROCEDURE_IMPL_S % impl, match_obj_deb[0], end_point)
                    if match_obj is None:
                        match_obj = self._match_regex(C_RE_PROCEDURE_IMPL % impl, match_obj_deb[0], end_point)

        if match_obj is not None:
            logger.debug('resultat detection function/procedure %s : %s', verb, str(match_obj[3]))
            group_match = match_obj[3]
            if len(match_obj[3]) == 4:
                match_obj_param = re.finditer(C_RE_PARAM, group_match[1])
                for match_iter in match_obj_param:
                    liste_param = match_iter.groups()[1]
                    if (liste_param == '') or (liste_param is None):
                        logger.error('nom de parametre non trouve dans fonction %s', group_match[0])
                    for param in liste_param.split(','):
                        liste_group.append((match_iter.groups()[0], param.strip(), match_iter.groups()[2]))
                group_match = (group_match[0], liste_group, group_match[2])
            elif len(match_obj[3]) == 2:
                group_match = (group_match[0], [], group_match[1], None)
            else:
                group_match = (group_match[0], [], group_match[1], group_match[2])
            return (match_obj[0], match_obj[1], match_obj[2], group_match, verb)
        return None


    def genere_fils(self, new_start_point, new_end_point):
        return cData(self.ogestionmultiligne, new_start_point, new_end_point)

    def num_ligne(self, indice):
        return self.ogestionmultiligne.num_ligne(indice)

