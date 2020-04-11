from .log import logger
from .regex import *

class cAnalyseur:
    def __init__(self, p_re, p_type, p_fils=[], p_obligatoire=True, p_repeter=False):
        if type(p_re) is not list:
            self.re = [p_re]
        else:
            self.re = p_re
        self.type = p_type
        self.fils = p_fils
        self.obligatoire = p_obligatoire
        self.repeter = p_repeter

    def __str__(self):
        return '[re <%s> type<%s> fils<%d> obl<%s> repet<%s>]' % (self.re, self.type, len(self.fils), str(self.obligatoire), str(self.repeter))


analyseur_unit = [ cAnalyseur(C_RE_UNIT, 'unit'),
                   cAnalyseur(C_RE_INTERFACE, 'interface'),
                   cAnalyseur(C_RE_USES, 'uses', p_obligatoire=False),
                   (cAnalyseur(C_RE_GROUPE_FUNCTION_PROCEDURE, 'function', p_obligatoire=False)),
                   cAnalyseur(C_RE_IMPLEMENTATION, 'implementation'),
                   cAnalyseur(C_RE_USES, 'uses', p_obligatoire=False),
                   cAnalyseur(C_RE_END_FINAL, 'end_final') ] 