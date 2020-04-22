import codecs
import json
from pathlib import Path
from hashlib import sha256

from .log import logger
from .data import cData
from .uses import cUses
from .type import cTableSymbol, cEnsembleType, cClasse
from .type import cType, cFonction, cRecord
from .type import genere_ensemble_type_par_groupe_resultat
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

        self.hash = sha256(self.data.data.encode('utf-8')).hexdigest()
        logger.info('Analyse du fichier <%s>', str(self.nom_fichier))
        self.analyse = analyseur_unit.analyse(self.data)[0]
        self.nom = self.analyse.chercher(p_type='unit')  # self.pos_unite[3][0]
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

        self.liste_section_interface = []
        self.type_interface_pos = []
        self.liste_type_interface = []
        self.symbols = cTableSymbol()
        self.liste_unite = []

        self.liste_type_interface = genere_ensemble_type_par_groupe_resultat(self.analyse, self.data)

        res = self.analyse.chercher(p_type='function')
        if len(res) > 0:
            for element in res:
                self.symbols.ajouter(element.reconnu[0],
                                     cFonction(element.reconnu[0],
                                               element,
                                               self.data.genere_fils(element.debut, element.fin)),
                                     self.data.genere_fils(element.debut, element.fin))
        for section_const in self.analyse.chercher(p_type='section_const'):
            for element in section_const.fils.chercher(p_type='const'):
                self.symbols.ajouter(element.reconnu[0],
                                     cType('const', element.reconnu[1],
                                           self.data.genere_fils(element.debut, element.fin),
                                           p_type=cType.T_CONST),
                                     self.data.genere_fils(element.debut, element.fin))
        logger.info('fin creation unite : %s', str(self))

    def json(self):
        return {
            'id': self.hash,
            'nom': self.nom,
            'nom_fichier': str(self.nom_fichier),
            'types': self.liste_type_interface.json(),            
            'symbol': self.symbols.json(),
        }
    
    def export_json_tofile(self, nomfichier):
        with open(nomfichier, 'w') as f:
            json.dump(self.json(), f, indent=4)

    def __str__(self):
        chaine = 'UNITE <%s> <%s> utilise par <%d>\n' % (self.nom, str(self.nom_fichier), len(self.liste_unite))
        chaine += '\tINTERFACE Ligne : %d\n' % self.analyse.chercher('interface')[0].num_ligne
        if self.uses_interface is not None:
            chaine += '\t\t' + str(self.uses_interface) + '\n'
        chaine += '\t\t' + str(self.liste_type_interface) + '\n'
        chaine += '\tIMPLEMENTATION cLigne : %d\n' % self.analyse.chercher('implementation')[0].num_ligne
        if self.uses_implementation is not None:
            chaine += '\t\t' + str(self.uses_implementation) + '\n'
        chaine += '\t%s\n' % str(self.symbols)
        return chaine

    def num_ligne(self, position):
        return self.gestion_ml.num_ligne(position)
