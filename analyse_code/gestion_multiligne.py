import re

from .log import logger


class gestion_multiligne:
    def __init__(self, lignes, mode_modification=False):
        logger.debug('debut gestion ligne %d ligne', len(lignes))
        self.index = []
        self.index_reel = []
        self.lignes = []
        self.data = ''
        index_courant = 0
        index_courant_reel = 0
        # en mode modificatio on garde les lignes pour pouvoir les modifier.
        if mode_modification:
            self.lignes = lignes
        mode_commentaire = False # pas de commentaire en cours
        for ligne in lignes:
            ligne_mod = ligne.replace('{$REGION}', ' ')
            ligne_mod = ligne_mod.replace('{$ENDREGION}', ' ')
            pos_commentaire = ligne_mod.find('//')
            ligne_mod = ligne_mod[0:pos_commentaire] + ' '
            position = 0
            ligne_finale = ''
            m_re = ()
            while (position < len(ligne_mod)) and (m_re is not None):
                # recherche le debut d'un commentaire            
                if not mode_commentaire:
                    m_re = re.search(r'(?<!\')\(\*', ligne_mod[position:])
                    if m_re is None:
                        m_re = re.search(r'(?<!\')\{', ligne_mod[position:])
                    # on en a trouve un
                    if m_re is not None:
                        logger.debug('debut commentaire detecte ligne '
                                     '<%d> <%d> <%d> -> <%d>', 
                                     len(self.index) + 1, position,
                                     m_re.start(0), m_re.end(0))
                        mode_commentaire = True
                        ligne_finale += ligne_mod[position:m_re.start(0)]
                        position += m_re.end(0)
                    # else:
                    #     ligne_finale += ligne_mod[position:]
                # recherche de la fin d'un commentaire
                else:
                    m_re = re.search(r'\*\)(?!\')', ligne_mod[position:])
                    if m_re is None:
                        m_re = re.search(r'\}(?!\')', ligne_mod[position:])
                    # on en a trouve un
                    if m_re is not None:
                        logger.debug('fin commentaire detecte ligne '
                                     '<%d> <%d> <%d> -> <%d>', 
                                     len(self.index) + 1, position,
                                     m_re.start(0), m_re.end(0))
                        mode_commentaire = False
                        position += m_re.end(0)
            # ce qu'il reste
            if not mode_commentaire:
                ligne_finale += ligne_mod[position:]

            self.data += ligne_finale
            self.index.append(index_courant)
            self.index_reel.append(index_courant_reel)
            index_courant += len(ligne_mod)
            index_courant_reel += len(ligne)

    def num_ligne(self, indice):
        for pos in self.index:
            if pos > indice:
                return self.index.index(pos)
        if indice >= self.index[-1]:
            return len(self.index)
        raise Exception('numero de ligne non trouve')

    def pos_num_ligne(self, num_ligne):
        return self.index_reel[num_ligne - 1]
