class gestion_multiligne:
    def __init__(self, lignes, mode_modification=False):
        self.index = []
        self.index_reel = []
        self.lignes = []
        self.data = ''
        index_courant = 0
        index_courant_reel = 0
        # en mode modificatio on garde les lignes pour pouvoir les modifier.
        if mode_modification:
            self.lignes = lignes
        for ligne in lignes:
            ligne_mod = re.sub(r'\(\*.*\*\)', ' ', ligne)
            ligne_mod = re.sub(r'\{.*?\}', ' ', ligne_mod)
            ligne_mod = ligne_mod.replace('{$REGION}', ' ')
            ligne_mod = ligne_mod.replace('{$ENDREGION}', ' ')
            pos_commentaire = ligne_mod.find('//')
            # if pos_commentaire != -1:
            #     print('commentaire trouve, ', ligne)
            ligne_mod = ligne_mod[0:pos_commentaire] + ' '
            self.data += ligne_mod
            # self.data += ligne[0:-1] + ' '
            self.index.append(index_courant)
            self.index_reel.append(index_courant_reel)
            index_courant += len(ligne_mod)
            index_courant_reel += len(ligne)
        # logger.debug('data <%s>', self.data)
    def num_ligne(self, indice):
        for pos in self.index:
            if pos > indice:
                return self.index.index(pos)
        if indice >= self.index[-1]:
            return len(self.index)
        raise Exception('numero de ligne non trouve')
    def pos_num_ligne(self, num_ligne):
        return self.index_reel[num_ligne - 1]
