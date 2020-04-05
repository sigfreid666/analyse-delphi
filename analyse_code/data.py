import re

from . import gestion_multiligne
from .log import logger

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
            res = (match_obj.start(0) + start, match_obj.end(0) + start, self.ogestionmultiligne.num_ligne(match_obj.start(0) + start), match_obj.groups())
            logger.debug('trouve : %s', str(res))
            return res
        logger.debug('pas trouve !!')
        return None

    def genere_fils(self, new_start_point, new_end_point):
        return cData(self.ogestionmultiligne, new_start_point, new_end_point)

    def num_ligne(self, indice):
        return self.ogestionmultiligne.num_ligne(indice)

