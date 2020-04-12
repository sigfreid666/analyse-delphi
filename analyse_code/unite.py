import re
from pathlib import Path
import codecs

from .log import *
from .gestion_multiligne import *
from .data import *
from .uses import *
from .regex import *
from .type import *

from .analyseur import analyseur_unit

class unite():
    def __init__(self, nom_fichier):
        self.data = ''
        self.gestion_ml = None
        self.nom_fichier = Path(nom_fichier)
        self.nom = ''
        with codecs.open(str(nom_fichier), 'r', encoding='utf-8-sig') as f:
            lignes = f.readlines()
            self.data = cData(lignes)
            self.gestion_ml = self.data.ogestionmultiligne

        logger.info('Analyse du fichier <%s>', str(self.nom_fichier))
        self.analyse = analyseur_unit.analyse(self.data)[0]
        # self.pos_unite = self._find_unit()
        self.nom = self.analyse.chercher(p_type='unit') # self.pos_unite[3][0]
        if len(self.nom) > 0:
            self.nom = self.nom[0].reconnu[0]
            logger.info('nom unite trouve <%s>', self.nom)

        self.uses_interface = self.uses_implementation = None

        res = self.analyse.chercher(p_type='uses_interface')
        if len(res) == 1:
            self.uses_interface = cUses(res[0].reconnu[0])
        res = self.analyse.chercher(p_type='uses_implementation')
        if len(res) == 1:
            self.uses_implementation = cUses(res[0].reconnu[0])

        self.liste_classe = []
        self.liste_section_interface = []
        self.liste_fonction = []
        self.type_interface_pos = []
        self.liste_type_interface = []
        self.symbols = cTableSymbol()
        self.liste_unite = []

        resultat = []
        res = self.analyse.chercher(p_type='section_type', recurse=False) # on recherche que le premier niveau
        if len(res) > 0:
            for section_type in res:
                resultat.append(cEnsembleType(self.data.genere_fils(section_type.debut, section_type.fin)))
                for element in section_type.fils.chercher(p_type='class'):
                    if element.reconnu[1].upper() == 'CLASS':
                        resultat[-1].ajouter(cClasse(element.reconnu[0], element.reconnu[2], element.fils, self.data.genere_fils(element.debut, element.fin)))
                    elif element.reconnu[1].upper() == 'RECORD':
                        resultat[-1].ajouter(cType(element.reconnu[0], '', self.data.genere_fils(element.debut, element.fin), p_type=cType.T_RECORD))
                    elif element.reconnu[1].upper() == 'INTERFACE':
                        resultat[-1].ajouter(cType(element.reconnu[0], '', self.data.genere_fils(element.debut, element.fin), p_type=cType.T_INTERFACE))
                    else:
                        resultat[-1].ajouter(cType(element.reconnu[0], '', self.data.genere_fils(element.debut, element.fin)))

                for element in section_type.fils.chercher(p_type='type_function'):
                    resultat[-1].ajouter(cType(element.reconnu[0], '', self.data.genere_fils(element.debut, element.fin)))
                for element in section_type.fils.chercher(p_type='type_autre'):
                    resultat[-1].ajouter(cType(element.reconnu[0], '', self.data.genere_fils(element.debut, element.fin)))

            self.liste_type_interface = resultat

        res = self.analyse.chercher(p_type='function')
        if len(res) > 0:
            for element in res:
                self.symbols.ajouter(element.reconnu[0], cType('function', '', None), self.data.genere_fils(element.debut, element.fin))

    def __str__(self):
        chaine = 'UNITE <%s> <%s> utilise par <%d>\n' % (self.nom, str(self.nom_fichier), len(self.liste_unite))
        chaine += '\tINTERFACE Ligne : %d\n' % self.gestion_ml.num_ligne(self.interface_pos[0])
        if self.uses_interface is not None:
            chaine += '\t\t' + str(self.uses_interface) + '\n'
        for t in self.liste_type_interface:
            chaine += '\t\t' + str(t) + '\n'
        chaine += '\tIMPLEMENTATION cLigne : %d\n' % self.gestion_ml.num_ligne(self.implementation_pos[0])
        if self.uses_implementation is not None:
            chaine += '\t\t' + str(self.uses_implementation) + '\n'
        chaine += '\t%s\n' % str(self.symbols)

        for iclass in self.liste_classe:
            chaine += str(iclass)
        for ifct in self.liste_fonction:
            chaine += str(ifct)
        return chaine

    def num_ligne(self, position):
        return self.gestion_ml.num_ligne(position)
