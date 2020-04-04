from . import log

class cType:
    T_SIMPLE = 1
    T_CLASS = 2
    T_RECORD = 3
    T_DEFINIT = 4
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

    def chercher(self, nom_type, cat_type='simple'):
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

class cClasse(cType):
    def __init__(self, nom, derivee, p_oData):
        super().__init__(nom, '', p_oData, p_type=cType.T_CLASS)
        self.derivee = derivee
        self.liste_fonction = {}
        self.type_local = []
        logger.info('traitement de la classe %s', self.nom)

    def __repr__(self):
        return '[CLA <%s> -> <%s> : %d fct]' % (self.nom, self.derivee, len(self.liste_fonction.keys()))
    def __str__(self):
        chaine = self.__repr__() + '\n'
        chaine += '\tLigne debut : %d\n' % self.data.num_ligne(self.data.start_point)
        chaine += '\tLigne fin : %d\n' % self.data.num_ligne(self.data.end_point)
        for fct in self.liste_fonction.values():
            chaine += str(fct) + '\n'
        return chaine
