import pickle
import re
import platform
from pathlib import Path

from .log import logger
from .unite import unite


class cEnsembleUnite:
    def __init__(self, repertoire, cache_unite=True, repertoire_remplacement=''):
        self.repertoire = repertoire
        self.nom_dpr = ''
        self.nom_fichier_dpr = ''
        self.repertoire_remplacement = repertoire_remplacement
        self.change_slash = platform.system() != 'Windows'
        self.unites = {}
        self.unites_non_utilise = []
        self.unites_non_trouve = []
        self.unites_uses_non_trouve = []

        self.nom_fichier = Path(repertoire) / Path('unite.pickle')
        if cache_unite:
            if self.nom_fichier.exists():
                with open(str(self.nom_fichier), 'rb') as f:
                    self.unites = pickle.load(f)

    def save(self):
        logger.info('sauvegarde : <%d> unite(s)', len(self.unites))
        with self.nom_fichier.open(mode='wb') as f:
            pickle.dump(self.unites, f)

    def analyser_repertoire(self):
        logger.info('ensemble unite : %s', self.repertoire)

        def parcour(p_repertoire):
            for x in Path(p_repertoire).iterdir():
                if (not x.is_dir()) and x.match('*.pas'):
                    self.unites[x.stem.upper()] = unite(str(x))
                    logger.debug('trouver : %s dans %s', x.name, p_repertoire)
                elif x.is_dir() and (not x.name.startswith('.')):
                    parcour(x)
        parcour(self.repertoire)

    def analyser(self, avec_type_interface=False):
        for un in self.unites:
            self.unites[un] = unite(un)
            if avec_type_interface:
                self.unites[un].analyse_type_interface()
            break

    def lire_dpr(self, nom_fichier_dpr, recharger=False):
        self.nom_fichier_dpr = nom_fichier_dpr
        with open(str(Path(self.repertoire) / Path(nom_fichier_dpr)), 'r') as f:
            logger.info('Ouverture du fichier dpr <%s>', nom_fichier_dpr)
            data = f.read()
            # on cherche le nom du programme
            program_pos = re.search(r'PROGRAM\s+(\w+?);', data, re.IGNORECASE)
            if program_pos is not None:
                self.nom_dpr = program_pos.groups()[0]
                logger.debug('Tag PROGRAM trouve nom <%s>', self.nom_dpr)
            else:
                raise Exception('nom du dpr non trouve')
            # on parcours les USES
            uses_pos = re.search(r'USES\s+', data, re.IGNORECASE)
            if uses_pos is not None:
                logger.debug('Tag USES trouve pos <%d>', uses_pos.start(0))
                unit_trouve = 0
                nom_fichier = ''
                for unit_pos in re.finditer(r'([\.\w]+)\s+IN\s+\'([\\\/\:\.\w]+)\'\s*(?:\{.*?\})?\s*(?:,|;)', data[uses_pos.end(0):], re.IGNORECASE):
                    try:
                        if recharger or (unit_pos.groups()[0].upper() not in self.unites):
                            nom_fichier = unit_pos.groups()[1]
                            if self.repertoire_remplacement != '':
                                pos = nom_fichier.find(self.repertoire_remplacement)
                                if pos > -1:
                                    nom_fichier = self.repertoire + nom_fichier[pos + len(self.repertoire_remplacement):]
                            if self.change_slash:
                                nom_fichier = nom_fichier.replace('\\', '/')
                            self.unites[unit_pos.groups()[0].upper()] = unite(nom_fichier)
                        logger.debug('unite trouve <%s> <%s>', unit_pos.groups()[0], unit_pos.groups()[1])
                        unit_trouve += 1
                    except FileNotFoundError:
                        self.unites_non_trouve.append((unit_pos.groups()[0], unit_pos.groups()[1]))
                        logger.error('le fichier <%s> n''existe pas (%s)', unit_pos.groups()[1], nom_fichier)
                    except Exception as e:
                        logger.error('impossibe d''analyser l''unite <%s>', unit_pos.groups()[0])
                        raise e
                logger.info('Nombre de unit trouve : <%d>', unit_trouve)

    def check_uses(self):
        for iunite in self.unites:
            if self.unites[iunite].uses_interface is not None:
                for uses in self.unites[iunite].uses_interface.list_uses:
                    if uses not in self.unites:
                        logger.error('impossible de trouve <%s> dans <%s>', uses, iunite)
            if self.unites[iunite].uses_implementation is not None:
                for uses in self.unites[iunite].uses_implementation.list_uses:
                    if uses not in self.unites:
                        logger.error('impossible de trouve <%s> dans <%s>', uses, iunite)

    def check_uses_non_utilise(self):
        self.unites_non_utilise = list(self.unites.keys())
        for iunite in self.unites:
            logger.debug('unite %s', iunite)
            if self.unites[iunite].uses_interface is not None:
                for uses in self.unites[iunite].uses_interface.list_uses:
                    logger.debug('verif uses interface %s', uses)
                    if uses.upper() in self.unites:
                        if uses.upper() in self.unites_non_utilise:
                            self.unites_non_utilise.remove(uses.upper())
                        if iunite not in self.unites[uses.upper()].liste_unite:
                            self.unites[uses.upper()].liste_unite.append(iunite)
                        logger.debug('remove %s', uses)
                    elif uses.upper() not in self.unites:
                        self.unites_uses_non_trouve.append(uses)
                        logger.error('uses <%s> non trouve dans les unites dans le fichier <%s>', uses, iunite)
            if self.unites[iunite].uses_implementation is not None:
                for uses in self.unites[iunite].uses_implementation.list_uses:
                    logger.debug('verif uses implementation %s', uses)
                    if uses.upper() in self.unites:
                        logger.debug('remove %s', uses)
                        if uses.upper() in self.unites_non_utilise:
                            self.unites_non_utilise.remove(uses.upper())
                        if iunite not in self.unites[uses.upper()].liste_unite:
                            self.unites[uses.upper()].liste_unite.append(iunite)
                    elif uses.upper() not in self.unites:
                        self.unites_uses_non_trouve.append(uses)
                        logger.error('uses <%s> non trouve dans les unites dans le fichier <%s>', uses, iunite)
        logger.info('check_uses_non_utilise : <%d> trouves, <%s>', len(self.unites_non_utilise), str(self.unites_non_utilise))

    def __str__(self):
        chaine = 'rep <%s> nombre unite <%d>' % (self.repertoire, len(self.unites))
        for un in self.unites:
            chaine = chaine + '\n' + str(self.unites[un])
        return chaine
