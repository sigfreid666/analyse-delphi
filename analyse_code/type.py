from .log import *
from .regex import *

class cType:
    T_SIMPLE = 1
    T_CLASS = 2
    T_RECORD = 3
    T_INTERFACE = 4
    def __init__(self, p_nom, p_definition, p_oData, p_type=T_SIMPLE):
        self.nom = p_nom
        self.definition = p_definition
        self.data = p_oData
        self.type = p_type
    def __str__(self):
        return 'TYPE <%s> <%d>' % (self.nom, self.type)

class cEnsembleType:
    def __init__(self, p_oData):
        self.types = {}
        self.data = p_oData

    def ajouter(self, o_ctype):
        if o_ctype.nom in self.types:
            self.types[o_ctype.nom].append(o_ctype)
        else:
            self.types[o_ctype.nom] = [o_ctype]

    def chercher(self, nom_type, cat_type='*'):
        if nom_type in self.types:
            if cat_type == '*':
                return self.types[nom_type]
            else:
                return [x for x in self.types[nom_type] if x.type == cat_type]
        else:
            return []

    def __str__(self):
        resultat = 'Ensemble type <%d> <%d>\n' % (self.data.start_point, self.data.end_point)
        for i_type in self.types:
            resultat += '\t%s <%d> ' % (i_type, len(self.types[i_type]))
            for elem in self.types[i_type]:
                resultat += '%s ' % str(elem)
            resultat += '\n'
        return resultat

class cTableSymbol:
    def __init__(self):
        self.symbol = {}

    def ajouter(self, p_symbol, p_type, p_oData):
        if p_symbol in self.symbol:
            self.symbol[p_symbol].append((p_type, p_oData))
        else:
            self.symbol[p_symbol] = [(p_type, p_oData)]

    def chercher(self, nom_symbol, cat_type='*'):
        if nom_symbol in self.symbol:
            if cat_type == '*':
                return self.symbol[nom_symbol]
            else:
                return [x for x in self.symbol[nom_symbol] if x[0].nom == cat_type]
        else:
            return []

    def __str__(self):
        resultat = 'Ensemble symbol <%d>\n' % len(self.symbol)
        for i_symbol in self.symbol:
            resultat += '\t%s <%d> ' % (i_symbol, len(self.symbol[i_symbol]))
            for elem in self.symbol[i_symbol]:
                resultat += '<%s> ' % elem[0].nom
            resultat += '\n'
        return resultat

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


class cClasse(cType):
    def __init__(self, nom, derivee, p_oResultatAnalyse, p_oData):
        super().__init__(nom, '', p_oData, p_type=cType.T_CLASS)
        self.analyse = p_oResultatAnalyse
        self.derivee = derivee
        self.liste_fonction = {}
        self.type_local = []
        self.symbols = cTableSymbol()
        self.liste_section = []
        logger.info('traitement de la classe %s', self.nom)
        for element in self.analyse.chercher(p_type='function'):
            self.symbols.ajouter(element.reconnu[0], cType('function', '', None), self.data.genere_fils(element.debut, element.fin))
        for element in self.analyse.chercher(p_type='menber'):
            for nom in element.reconnu[0].split(','):
                self.symbols.ajouter(nom.strip(' '), cType(element.reconnu[1], '', None), self.data.genere_fils(element.debut, element.fin))
        for element in self.analyse.chercher(p_type='property'):
            self.symbols.ajouter(element.reconnu[0], cType(element.reconnu[1], '', None), self.data.genere_fils(element.debut, element.fin))

        self.type_local = []
        res = self.analyse.chercher(p_type='section_type') # on recherche que le premier niveau
        if len(res) > 0:
            for section_type in res:
                self.type_local.append(cEnsembleType(self.data.genere_fils(section_type.debut, section_type.fin)))
                for element in section_type.fils.chercher(p_type='class'):
                    if element.reconnu[1].upper() == 'CLASS':
                        self.type_local[-1].ajouter(cClasse(element.reconnu[0], element.reconnu[2], element.fils, self.data.genere_fils(element.debut, element.fin)))
                    elif element.reconnu[1].upper() == 'RECORD':
                        self.type_local[-1].ajouter(cType(element.reconnu[0], '', self.data.genere_fils(element.debut, element.fin), p_type=cType.T_RECORD))
                    elif element.reconnu[1].upper() == 'INTERFACE':
                        self.type_local[-1].ajouter(cType(element.reconnu[0], '', self.data.genere_fils(element.debut, element.fin), p_type=cType.T_INTERFACE))
                    else:
                        self.type_local[-1].ajouter(cType(element.reconnu[0], '', self.data.genere_fils(element.debut, element.fin)))

                for element in section_type.fils.chercher(p_type='type_function'):
                    self.type_local[-1].ajouter(cType(element.reconnu[0], '', self.data.genere_fils(element.debut, element.fin)))
                for element in section_type.fils.chercher(p_type='type_autre'):
                    self.type_local[-1].ajouter(cType(element.reconnu[0], '', self.data.genere_fils(element.debut, element.fin)))
                    
    def __repr__(self):
        return '[CLA <%s> -> <%s> : %d fct]' % (self.nom, self.derivee, len(self.liste_fonction.keys()))
    def __str__(self):
        chaine = self.__repr__() + '\n'
        chaine += '\tLigne debut : %d\n' % self.data.num_ligne(self.data.start_point)
        chaine += '\tLigne fin : %d\n' % self.data.num_ligne(self.data.end_point)
        chaine += '\t'  + str(self.symbols)
        for fct in self.liste_fonction.values():
            chaine += str(fct) + '\n'
        return chaine
