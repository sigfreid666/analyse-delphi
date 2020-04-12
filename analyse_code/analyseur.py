from .log import logger
from .regex import C_RE_CLASS_DEB
from .regex import C_RE_TYPE_PROC_FUNC
from .regex import C_RE_DECL_TYPE_SETOF
from .regex import C_RE_DECL_TYPE
from .regex import C_RE_UNIT
from .regex import C_RE_INTERFACE
from .regex import C_RE_USES
from .regex import C_RE_FUNCTION_DECL
from .regex import C_RE_FUNCTION_DECL_S
from .regex import C_RE_PROCEDURE_DECL
from .regex import C_RE_PROCEDURE_DECL_S
from .regex import C_RE_TYPES
from .regex import C_RE_IMPLEMENTATION
from .regex import C_RE_END_FINAL
from .regex import C_RE_END


class cGroupeResultat():
    """Ensemble des resultats d'une analyse"""
    class cResultat():
        """un resultat d'analyse"""
        def __init__(self, p_type, p_position, p_fils):
            self.type = p_type
            self.debut = p_position[0]
            self.fin = p_position[1]
            self.num_ligne = p_position[2]
            self.reconnu = p_position[3]
            if p_fils is not None:
                self.fils = cGroupeResultat().ajouter(p_fils)
            else:
                self.fils = None

    def __init__(self):
        self.resultats = []

    def ajouter(self, p_resultats):
        if type(p_resultats) == cGroupeResultat:
            for resultat in p_resultats.resultats:
                self.ajouter(resultat)
        else:
            self.resultats.append(p_resultats)
        return self

    def chercher(self, p_type='', p_nom=''):
        res = []
        for resultat in self.resultats:
            if (p_type != '') and (resultat.type == p_type):
                res.append(resultat)
            if (p_nom != '') and (resultat.type == p_nom):
                res.append(resultat)
            if resultat.fils is not None:
                if type(resultat.fils) == cGroupeResultat:
                    for elem in resultat.fils.chercher(p_type=p_type, p_nom=p_nom):
                        res.append(elem)
                else:
                    if (p_type != '') and (resultat.fils.type == p_type):
                        res.append(resultat.fils)
                    if (p_nom != '') and (resultat.fils.type == p_nom):
                        res.append(resultat.fils)
        return res


class cAnalyseur:
    """Analyseur simple"""
    def __init__(self, p_re, p_type, p_fils=None, p_obligatoire=True):
        self.re = p_re
        self.type = p_type
        self.fils = p_fils
        self.obligatoire = p_obligatoire

    def analyse(self, data, position=0):
        logger.debug('debut analyse type<%s> type_fils<%s> obl<%s>', self.type, str(type(self.fils)), str(self.obligatoire))
        resultat = None
        pos_espace = data._match_regex(r'\s+', position, -1)
        if pos_espace is not None:
            position = pos_espace[1]
        pos = data._match_regex(self.re, position, -1)
        if pos is not None:
            if self.fils is not None:
                fils_resultat, position = self.fils.analyse(data, pos[1])
                resultat = cGroupeResultat.cResultat(self.type, pos, fils_resultat)
            else:
                resultat = cGroupeResultat.cResultat(self.type, pos, None)
                position = pos[1]
        elif self.obligatoire:
            raise Exception('impossible de trouver %s' % str(self))
        return resultat, position

    def __repr__(self):
        return 'cAnalyseur<%s>' % self.type

    def __str__(self):
        return '[re <%s> type<%s> fils<%s> obl<%s>]' % (self.re, self.type, str(self.fils), str(self.obligatoire))


class cRepeteurAnalyseur:
    """Repete n fois un analyseur"""
    def __init__(self, p_analyseur):
        self.analyseur = p_analyseur

    def analyse(self, data, position=0):
        logger.debug('cRepeteurAnalyseur : debut analyse')
        resultat = cGroupeResultat()
        elem_resultat, elem_position = self.analyseur.analyse(data, position)
        while elem_resultat is not None:
            position = elem_position
            resultat.ajouter(elem_resultat)
            elem_resultat, elem_position = self.analyseur.analyse(data, position)
        if elem_resultat is not None:
            position = elem_position
            resultat.ajouter(elem_resultat)
        logger.debug('cRepeteurAnalyseur : fin analyse')
        return resultat, position


class cListeAnalyseur:
    """Liste sequentiel d'analyseur"""
    def __init__(self, p_analyseurs):
        self.analyseurs = p_analyseurs

    def analyse(self, data, position=0):
        logger.debug('cListeAnalyseur : debut analyse')
        resultat = cGroupeResultat()
        for analyseur in self.analyseurs:
            elem_resultat, elem_position = analyseur.analyse(data, position)
            if elem_resultat is not None:
                resultat.ajouter(elem_resultat)
                position = elem_position
        logger.debug('cListeAnalyseur : fin analyse')
        return resultat, position


class cGroupeAnalyseur():
    """Groupement d'analyseur, des qu'un correspond arrete l'analyse"""
    def __init__(self, p_analyseurs, p_obligatoire=True):
        self.analyseurs = p_analyseurs
        for analyseur in self.analyseurs:
            analyseur.obligatoire = False
        self.obligatoire = p_obligatoire

    def analyse(self, data, position=0):
        logger.debug('cGroupeAnalyseur : debut analyse')
        for analyseur in self.analyseurs:
            elem_resultat, elem_position = analyseur.analyse(data, position)
            if elem_resultat is not None:
                logger.debug('cGroupeAnalyseur : fin analyse')
                return elem_resultat, elem_position
        if self.obligatoire:
            raise Exception('impossible de trouver %s' % str(analyseur))
        else:
            logger.debug('cGroupeAnalyseur : fin analyse')
            return None, position


analyseur_class = cListeAnalyseur((
    cAnalyseur(C_RE_END, 'end'),
))

analyseur_types = cGroupeAnalyseur((
    cAnalyseur(C_RE_CLASS_DEB, 'class', p_fils=analyseur_class),
    cAnalyseur(C_RE_TYPE_PROC_FUNC, 'type_function'),
    cAnalyseur(C_RE_DECL_TYPE_SETOF, 'type_setof'),
    cAnalyseur(C_RE_DECL_TYPE, 'type_autre')))

analyseur_unit = cListeAnalyseur((
    cAnalyseur(C_RE_UNIT, 'unit'),
    cAnalyseur(C_RE_INTERFACE, 'interface'),
    cAnalyseur(C_RE_USES, 'uses', p_obligatoire=False),
    cRepeteurAnalyseur(
        cGroupeAnalyseur((
            cAnalyseur(C_RE_FUNCTION_DECL, 'function'),
            cAnalyseur(C_RE_FUNCTION_DECL_S, 'function'),
            cAnalyseur(C_RE_PROCEDURE_DECL, 'function'),
            cAnalyseur(C_RE_PROCEDURE_DECL_S, 'function'),
            cAnalyseur(C_RE_TYPES, 'section_type', p_fils=analyseur_types)),
            p_obligatoire=False)),
    cAnalyseur(C_RE_IMPLEMENTATION, 'implementation'),
    cAnalyseur(C_RE_USES, 'uses', p_obligatoire=False),
    cAnalyseur(C_RE_END_FINAL, 'end_final')))
