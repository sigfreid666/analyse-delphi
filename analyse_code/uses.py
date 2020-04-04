from .log import logger

class cUses:
    def __init__(self, data_uses):
        self.list_uses = [x.strip() for x in data_uses.split(',')]
        logger.info('%d uses trouves', len(self.list_uses))

    def __repr__(self):
        return 'USES nb <%d>' % (len(self.list_uses))

    def analyse_uses(self, ensemble_unite, tabulation):
        logger.info('analyse_uses : <%d>', len(self.list_uses))
        rangement = [
            { 'nom' : 'BibliothequeDelphi', 'chemins': 'LibDelphi', 'unites_trouves': [] },
            { 'nom' : 'Librairies', 'chemins': 'Librairies', 'unites_trouves': [] },
            { 'nom' : 'CommunProduits', 'chemins': 'CommunProduits', 'unites_trouves': [] },
            { 'nom' : 'Types', 'chemins': 'Types', 'unites_trouves': [] },
            { 'nom' : 'Tables', 'chemins': 'Tables', 'unites_trouves': [] },
            { 'nom' : 'Requetes', 'chemins': 'Requetes', 'unites_trouves': [] },
            { 'nom' : 'Services', 'chemins': 'Services', 'unites_trouves': [] },
            { 'nom' : 'EDT', 'chemins': 'EdT', 'unites_trouves': [] },
            { 'nom' : 'PRONOTE', 'chemins': 'Pronote', 'unites_trouves': [] },
            { 'nom' : 'Scolys', 'chemins': 'Scolys', 'unites_trouves': [] },
        ]

        uses_consomme = self.list_uses.copy()
        for uses in self.list_uses:
            nom_unite = uses # + '.pas'
            if nom_unite in ensemble_unite.unites:
                oPath = ensemble_unite.unites[nom_unite].nom_fichier
                for rang in rangement:
                    logger.debug('analyse_uses : chemin <%s> parts <%s>', rang['chemins'], str(oPath.parts))
                    if rang['chemins'] in oPath.parts:
                        rang['unites_trouves'].append(uses)
                        uses_consomme.remove(uses)
                        break
            

        logger.info('analyse_uses : uses consomme <%d>', len(uses_consomme))
        lignes = []
        for rang in rangement:
            if len(rang['unites_trouves']) > 0:
                lignes.append(tabulation + '// ' + rang['nom'])
                rang['unites_trouves'].sort()
                for unite in rang['unites_trouves']:
                    lignes.append(tabulation + unite + ',')
        if len(uses_consomme) > 0:
            print('uses non consommés', uses_consomme)
        chaine = ''
        if len(lignes) > 0:
            chaine = '\n'.join(lignes[0:-1])
            chaine += '\n%s;\n' % lignes[-1][:-1]
        return chaine
