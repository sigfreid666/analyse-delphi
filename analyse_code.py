import re
from pathlib import Path
import pickle
import codecs

import logging
  
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
        # current_pos = 0
        # type_inter = self._find_type(current_pos)
        # if type_inter is not None:
        #     logger.info('type trouve dans classe %s', str(type_inter))
        #     decl_type = re.search(C_RE_DECL_TYPE, self.data[type_inter[1]:])
        #     if decl_type is not None:
        #         pos_impl_type = (decl_type.start(0) + type_inter[1], decl_type.end(0) + type_inter[1], self.gestion_ml.num_ligne(decl_type.start(0) + type_inter[1]))
        #         current_pos = pos_impl_type[1]
        # funct_inter = (0, current_pos)
        # while funct_inter != None:
        #     funct_inter = self._find_function(funct_inter[1], -1)
        #     if funct_inter is not None:
        #         logger.info('fonction trouve : %s', str(funct_inter))
        #         self.liste_fonction[funct_inter[4][0]] = cFonction(funct_inter[4][0].strip(), funct_inter[4][1], self.genere_infosubutilitaire(funct_inter[0], funct_inter[1]))
        # logger.debug('fin des fonctions')
        # funct_inter = self._find_procedure(current_pos, -1)
        # if funct_inter is not None:
        #     logger.info('procedure trouve : info %s', str(funct_inter))
        #     self.liste_fonction[funct_inter[4][0]] = cFonction(funct_inter[4][0], funct_inter[4][1], self.genere_infosubutilitaire(funct_inter[0], funct_inter[1]))
        # while funct_inter != None:
        #     funct_inter = self._find_procedure(funct_inter[1], -1)
        #     if funct_inter is not None:
        #         logger.info('procedure trouve : info %s', str(funct_inter))
        #         self.liste_fonction[funct_inter[4][0]] = cFonction(funct_inter[4][0].strip(), funct_inter[4][1], self.genere_infosubutilitaire(funct_inter[0], funct_inter[1]))

    def __repr__(self):
        return '[CLA <%s> -> <%s> : %d fct]' % (self.nom, self.derivee, len(self.liste_fonction.keys()))
    def __str__(self):
        chaine = self.__repr__() + '\n'
        chaine += '\tLigne debut : %d\n' % self.data.num_ligne(self.data.start_point)
        chaine += '\tLigne fin : %d\n' % self.data.num_ligne(self.data.end_point)
        for fct in self.liste_fonction.values():
            chaine += str(fct) + '\n'
        return chaine


class unite():
    def __init__(self, nom_fichier):
        self.data = ''
        self.gestion_ml = None
        self.nom_fichier = Path(nom_fichier)
        self.nom = ''
        with codecs.open(str(nom_fichier), 'r', encoding='utf-8-sig') as f:
            lignes = f.readlines()
            self.gestion_ml = gestion_multiligne(lignes)
            self.data = cData(self.gestion_ml)

        logger.info('Analyse du fichier <%s>', str(self.nom_fichier))
        self.pos_unite = self._find_unit()
        self.nom = self.pos_unite[3][0]
        self.liste_classe = []
        self.liste_section_interface = []
        self.liste_fonction = []
        self.type_interface_pos = []
        self.liste_type_interface = []
        self.symbols = cTableSymbol()
        self.uses_inter_pos = self.uses_interface = None
        self.uses_impl_pos = self.uses_implementation = None
        self.liste_unite = []
        self.interface_pos = self._find_interface()
        if self.interface_pos is None:
            logger.error('impossible de trouver la section interface')
        self.implementation_pos = self._find_implementation()
        if self.implementation_pos is None:
            logger.error('impossible de trouver la section implementation')
        self.end_final_pos = self._find_endfinal()
        if self.end_final_pos is None:
            logger.error('impossible de trouver le end final')
        if (self.interface_pos is not None) and (self.implementation_pos is not None):
            self.uses_inter_pos = self._find_uses(self.interface_pos[1], self.implementation_pos[0])
            self.uses_impl_pos = self._find_uses(self.implementation_pos[1], self.end_final_pos[0])
            if self.uses_inter_pos is not None:
                self.uses_interface = cUses(self.uses_inter_pos[3][0])
            if self.uses_impl_pos is not None:
                self.uses_implementation = cUses(self.uses_impl_pos[3][0])

    def analyse_type_interface(self):
        self.type_interface_pos, self.liste_type_interface = self._analyse_type(self.interface_pos[1], self.implementation_pos[0])
        # on cherche les functions / procedure entre les sections type
        debut = self.interface_pos[1]
        logger.debug('analyse_type_interface : liste pos %s', str(self.type_interface_pos))
        for pos in self.type_interface_pos:
            fin = pos[0]
            pos_function = self._find_function(debut, fin)
            while pos_function is not None:
                logger.debug('analyse_type_interface : fonction trouve %s', str(pos_function))
                pos_function = self._find_function(pos_function[1], fin)
            debut = pos[1]
        fin = self.implementation_pos[0]
        pos_function = self._find_function(debut, fin)
        while pos_function is not None:
            self.symbols.ajouter(pos_function[3][0], cType('function', '', None), self.data.genere_fils(pos_function[0], pos_function[1]))
            logger.debug('analyse_type_interface : fonction trouve %s', str(pos_function))
            pos_function = self._find_function(pos_function[1], fin)

    def _analyse_type(self, start_point, end_point):
        logger.info('debut analyse type')
        type_pos = []
        liste_type = []
        pos = self._find_type(start_point, end_point)
        while pos is not None:
            logger.info('section type trouve %s', str(pos))
            liste_type.append(self._analyse_section_type(pos[1], end_point))
            type_pos.append((pos[0], liste_type[-1].data.end_point))
            pos = self._find_type(liste_type[-1].data.end_point, end_point)
        return (type_pos, liste_type)

        # self.type_impl_pos = []
        # pos = self._find_type(self.implementation_pos[1])
        # logger.warning('section type trouve : %s', str(pos))
        # while pos != None:
        #     self.type_impl_pos.append(pos)
        #     pos = self._find_type(pos[1])
        #     logger.warning('section type trouve : %s', str(pos))
        # class_inter_pos = self._find_class(self.type_inter_pos[1], self.implementation_pos[0])
        # logger.info('section class trouve : %s', str(class_inter_pos))
        # while class_inter_pos != None:
        #     self.liste_classe.append(cClasse(class_inter_pos[4][0].strip(), class_inter_pos[4][1], self.genere_infosubutilitaire(class_inter_pos[0], class_inter_pos[1])))
        #     class_inter_pos = self._find_class(class_inter_pos[1], self.implementation_pos[0])
        #     logger.info('section class trouve : %s', str(class_inter_pos))
        # liste_pos_impl = []
        # # parcours des implementations
        # for cl in self.liste_classe:
        #     logger.debug('parcours des implementations pour la classe %s', cl.nom)
        #     for fct in cl.liste_fonction.values():
        #         logger.debug('recherche de %s', fct.nom)
        #         res = self._find_function(self.implementation_pos[0], self.end_final_pos[0], impl='%s.%s' % (cl.nom, fct.nom))
        #         if res is not None:
        #             logger.info('fonction %s trouvee %s', fct.nom, str(res))
        #             if res[0] in liste_pos_impl:
        #                 logger.error('fonction %s deja trouvee', fct.nom)
        #             liste_pos_impl.append(res[0])
        #         else:
        #             res = self._find_procedure(self.implementation_pos[0], self.end_final_pos[0], impl='%s.%s' % (cl.nom, fct.nom))
        #             if res is not None:
        #                 logger.info('procedure %s trouvee %s', fct.nom, str(res))
        #                 if res[0] in liste_pos_impl:
        #                     logger.error('procedure %s deja trouvee', fct.nom)
        #                 liste_pos_impl.append(res[0])
        # logger.debug('fin recherche implementation')
        # if len(liste_pos_impl) > 0:
        #     liste_pos_impl.sort()
        #     for x in self.type_impl_pos:
        #         if x[0] > liste_pos_impl[0]:
        #             logger.info('detection type apres premiere implementation ligne %d', self.num_ligne(x[0]))
        #         else:
        #             liste_pos_impl.append(x[0])
        #     liste_pos_impl.sort()
        # liste_pos_impl.append(self.end_final_pos[0])
        # logger.info('%d implementation detecte', len(liste_pos_impl))
        # for cl in self.liste_classe:
        #     for fct in cl.liste_fonction.values():
        #         res = self._find_function(self.implementation_pos[0], self.end_final_pos[0], impl='%s.%s' % (cl.nom, fct.nom))
        #         if res is not None:
        #             next_pos = liste_pos_impl[ liste_pos_impl.index(res[0]) + 1] - 1
        #             logger.debug('creation implementation : %s.%s %s -> %d', cl.nom, fct.nom, str(res), next_pos)
        #             fct.implementation = cFonctionImpl('%s.%s' % (cl.nom, fct.nom), self.genere_infosubutilitaire(res[1], next_pos))
                    

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

    def _find_unit(self):
        return self.data._find_regex(C_RE_UNIT, 0, -1)
    def _find_interface(self):
        return self.data._find_regex(C_RE_INTERFACE, 0, -1)
    def _find_implementation(self):
        return self.data._find_regex(C_RE_IMPLEMENTATION, 0, -1)
    def _find_endfinal(self):
        return self.data._find_regex(C_RE_END_FINAL, 0, -1)

    def _find_function(self, start_point, end_point, impl=''):
        match_obj = None
        verb = 'function'
        liste_group = [ ]
        if impl == '':
            match_obj = self.data._find_regex(C_RE_FUNCTION_DECL_S, start_point, end_point)
            if match_obj is None:
                match_obj = self.data._find_regex(C_RE_FUNCTION_DECL, start_point, end_point)
            match_obj_proc = self.data._find_regex(C_RE_PROCEDURE_DECL_S, start_point, end_point)
            if match_obj_proc is None:
                match_obj_proc = self.data._find_regex(C_RE_PROCEDURE_DECL, start_point, end_point)
            # la procedure est avant la function on garde la procedure
            if ((match_obj is not None) and (match_obj_proc is not None) and (match_obj_proc[0] < match_obj[0])) or\
               ((match_obj is None) and (match_obj_proc is not None)):
                verb = 'procedure'
                match_obj = match_obj_proc
        else:
            match_obj = self.data._find_regex(C_RE_FUNCTION_IMPL_S % impl, start_point, end_point)
            if match_obj is None:            
                match_obj = self.data._find_regex(C_RE_FUNCTION_IMPL % impl, start_point, end_point)
            match_obj_proc = self.data._find_regex(C_RE_PROCEDURE_IMPL_S % impl, start_point, end_point)
            if match_obj_proc is None:
                match_obj_proc = self.data._find_regex(C_RE_PROCEDURE_IMPL % impl, start_point, end_point)
            # la procedure est avant la function on garde la procedure
            if match_obj_proc[0] < match_obj[0]:
                match_obj = match_obj_proc
        if match_obj is not None:
            logger.debug('resultat detection function/procedure : %s', str(match_obj[3]))
            group_match = match_obj[3]
            if len(match_obj[3]) == 4:
                match_obj_param = re.finditer(C_RE_PARAM, group_match[1])
                for match_iter in match_obj_param:
                    liste_param = match_iter.groups()[1]
                    if (liste_param == '') or (liste_param is None):
                        logger.error('nom de parametre non trouve dans fonction %s', group_match[0])
                    for param in liste_param.split(','):
                        liste_group.append((match_iter.groups()[0], param.strip(), match_iter.groups()[2]))
                group_match = (group_match[0], liste_group, group_match[2])
            else:
                group_match = (group_match[0], [], group_match[1], group_match[2])
            return (match_obj[0], match_obj[1], match_obj[2], group_match, verb)
        return None
    def _find_procedure(self, start_point, end_point, impl=''):
        match_obj = None
        if impl == '':
            match_obj = self.data._find_regex(C_RE_PROCEDURE_DECL_S, start_point, end_point)
            if match_obj is None:
                match_obj = self.data._find_regex(C_RE_PROCEDURE_DECL, start_point, end_point)
        else:
            match_obj = self.data._find_regex(C_RE_PROCEDURE_IMPL_S % impl, start_point, end_point)
            if match_obj is None:
                match_obj = self.data._find_regex(C_RE_PROCEDURE_IMPL % impl, start_point, end_point)
        if match_obj is not None:
            group_match = match_obj[3]
            if len(match_obj[3]) == 3:
                match_obj_param = re.finditer(C_RE_PARAM, group_match[1])
                liste_group = [ ]
                for match_iter in match_obj_param:
                    liste_param = match_iter.groups()[1]
                    if (liste_param == '') or (liste_param is None):
                        logger.error('nom de parametre non trouve dans procedure %s', group_match[0])
                    for param in liste_param.split(','):
                        liste_group.append((match_iter.groups()[0], param.strip(), match_iter.groups()[2]))
                group_match = (group_match[0], liste_group)
            else:
                group_match = (group_match[0], [])
            return (match_obj[0], match_obj[1], match_obj[2], group_match)
        return None

    def _find_uses(self, start_point, end_point):
        return self.data._find_regex(C_RE_USES, start_point, end_point)

    def _find_type(self, start_point, end_point):
        return self.data._find_regex(C_RE_TYPES, start_point, end_point)

    def _find_class(self, start_point, end_point):
        match_pos = self.data._find_regex(C_RE_CLASS_DEB, start_point, end_point)
        end_pos = None
        if match_pos is not None:
            logger.debug('find_class : debut de class trouve type %s', match_pos[3][2])
            current_pos = match_pos[1]
            # on cherche le premier end
            end_pos = self.data._find_regex(C_RE_END, current_pos, end_point)
            # on cherche une section type
            pos_type = self._find_type(current_pos, end_point)
            # si type detecte et avant premier end
            if (pos_type is not None) and (end_pos is not None) and (pos_type[1] < end_pos[1]):
                current_pos = pos_type[1]
                logger.debug('find_class : section type trouve : %d %d', current_pos,end_pos[1])
                while True:
                    match_pos_class = self.data._find_regex(C_RE_CLASS_DEB, current_pos, end_pos[1])
                    # on a trouve une classe avant le end
                    if (match_pos_class is not None):
                        logger.debug('classe fille trouve ligne : %d', self.num_ligne(start_point + current_pos + match_pos_class[0]))
                        # on cherche le prochain end
                        end_pos = self.data._find_regex(C_RE_END, end_pos[1], end_point)
                        current_pos = end_pos[1]
                        logger.debug('end trouve ligne : %s', str(end_pos))
                    else:
                        break
            if end_pos is not None:
                return (match_pos[0], end_pos[1], self.gestion_ml.num_ligne(match_pos[0]), self.gestion_ml.num_ligne(end_pos[1]), match_pos[3])
        return None
    def _find_record(self, start_point, end_point):
        return self.data._find_regex(C_RE_RECORD, start_point, end_point)

    def _find_type_proc_func(self, start_point, end_point):
        return self.data._find_regex(C_RE_TYPE_PROC_FUNC, start_point, end_point)

    def _find_type_decl(self, start_point, end_point):
        return self.data._find_regex(C_RE_DECL_TYPE, start_point, end_point)

    def _analyse_section_type(self, start_point, end_point):
        resultat = { 'class': [], 'record': [], 'type': [], 'setof': [], 'type_procedure': [], 'finsection': end_point}
        resultat = cEnsembleType(self.data.genere_fils(start_point, end_point))
        current_pos = start_point
        logger.debug('analyse type : %s', self.data.data[current_pos:current_pos+30])
        # d'abord on saute les premiers espace
        espace_pos = self.data._find_regex(r'\s*', current_pos, -1)
        if espace_pos is not None:
            logger.debug('espace trouve : %s %d', str(espace_pos), espace_pos[1] + 1)
            current_pos = espace_pos[1]
        while current_pos < end_point:
            logger.debug('analyse type : %s', self.data.data[current_pos:current_pos+30])
            # on recherche une classe
            class_pos = self._find_class(current_pos, end_point)
            if (class_pos is not None) and (class_pos[0] == current_pos):
                logger.info('classe trouve : %s', str(class_pos))
                current_pos = class_pos[1] + 1
                if class_pos[4][1] == 'CLASS':
                    resultat.ajouter(cClasse(class_pos[4][0], class_pos[4][2], self.data.genere_fils(class_pos[0], class_pos[1])))
                else:
                    resultat.ajouter(cType(class_pos[4][0], '', self.data.genere_fils(class_pos[0], class_pos[1]), p_type=class_pos[4][1]))
                # resultat['class'].append(class_pos) 
            else:
                typefunc_pos = self._find_type_proc_func(current_pos, end_point)
                if (typefunc_pos is not None) and (typefunc_pos[0] == current_pos):
                    logger.info('type procedure trouve')
                    current_pos = typefunc_pos[1] + 1
                    resultat.ajouter(cType(typefunc_pos[3][0], '', self.data.genere_fils(typefunc_pos[0], typefunc_pos[1])))
                    # resultat['type_procedure'].append(typefunc_pos) 
                else:
                    typedecl_pos = self._find_type_decl(current_pos, end_point)
                    if (typedecl_pos is not None) and (typedecl_pos[0] == current_pos):
                        logger.info('type declaration trouve')
                        current_pos = typedecl_pos[1] + 1
                        resultat.ajouter(cType(typedecl_pos[3][0], '', self.data.genere_fils(typedecl_pos[0], typedecl_pos[1])))
                        # resultat['type'].append(typedecl_pos) 
                    else:
                        logger.error('type non trouve')
                        # resultat['finsection'] = current_pos
                        resultat.data.end_point = current_pos
                        logger.info('fin analyse type ; %s', str(resultat))
                        return resultat
            espace_pos = self.data._find_regex(r'\s*', current_pos, -1)
            if espace_pos is not None:
                # logger.debug('avant saut espace : %s', self.data[current_pos:current_pos+30])
                current_pos = espace_pos[1]
        # resultat['finsection'] = current_pos
        resultat.data.end_point = current_pos
        logger.info('fin analyse type ; %s', str(resultat))
        return resultat
    def num_ligne(self, position):
        return self.gestion_ml.num_ligne(position)


class cEnsembleUnite:
    def __init__(self, repertoire, cache_unite=True):
        self.repertoire = repertoire
        self.nom_dpr = ''
        self.nom_fichier_dpr = ''
        self.unites = {}

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
                    self.unites[str(x)] = unite(str(x))
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
                for unit_pos in re.finditer(r'([\.\w]+)\s+IN\s+\'([\\\/\:\.\w]+)\'\s*(?:\{.*?\})?\s*(?:,|;)', data[uses_pos.end(0):], re.IGNORECASE):
                    try:
                        if recharger or (unit_pos.groups()[0].upper() not in self.unites):
                            self.unites[unit_pos.groups()[0].upper()] = unite(unit_pos.groups()[1])
                        logger.debug('unite trouve <%s> <%s>', unit_pos.groups()[0], unit_pos.groups()[1])
                        unit_trouve += 1
                    except FileNotFoundError:
                        logger.error('le fichier <%s> n''existe pas', unit_pos.groups()[0])
                    except Exception as e:
                        logger.error('impossibe d''analyser l''unite <%s>', unit_pos.groups()[0])
                        raise e
                logger.info('Nombre de unit trouve : <%d>', unit_trouve)

    def check_uses(self):
        for unite in self.unites:
            if self.unites[unite].uses_interface is not None:
                for uses in self.unites[unite].uses_interface.list_uses:
                    if uses not in self.unites:
                        logger.error('impossible de trouve <%s> dans <%s>', uses, unite)
            if self.unites[unite].uses_implementation is not None:
                for uses in self.unites[unite].uses_implementation.list_uses:
                    if uses not in self.unites:
                        logger.error('impossible de trouve <%s> dans <%s>', uses, unite)

    def check_uses_non_utilise(self):
        stat = list(self.unites.keys())
        for unite in self.unites:
            logger.debug('unite %s', unite)
            # if unite not in stat:
            #     continue
            logger.debug('on continue')
            if self.unites[unite].uses_interface is not None:
                for uses in self.unites[unite].uses_interface.list_uses:
                    logger.debug('verif uses interface %s', uses)
                    if (uses.upper() in self.unites) and (uses.upper() in stat):
                        stat.remove(uses.upper())
                        if unite not in self.unites[uses.upper()].liste_unite:
                            self.unites[uses.upper()].liste_unite.append(unite)
                        logger.debug('remove %s', uses)
                    elif uses.upper() not in self.unites:
                        logger.error('uses <%s> non trouve dans les unites dans le fichier <%s>', uses, unite)
            if self.unites[unite].uses_implementation is not None:
                for uses in self.unites[unite].uses_implementation.list_uses:
                    logger.debug('verif uses implementation %s', uses)
                    if (uses.upper() in self.unites) and (uses.upper() in stat):
                        logger.debug('remove %s', uses)
                        stat.remove(uses.upper())
                        if unite not in self.unites[uses.upper()].liste_unite:
                            self.unites[uses.upper()].liste_unite.append(unite)
                    elif uses.upper() not in self.unites:
                        logger.error('uses <%s> non trouve dans les unites dans le fichier <%s>', uses, unite)
        logger.info('check_uses_non_utilise : <%d> trouves, <%s>', len(stat), str(stat))

    def __str__(self):
        chaine = 'rep <%s> nombre unite <%d>' % (self.repertoire, len(self.unites))
        for un in self.unites:
            chaine = chaine + '\n' + str(self.unites[un])
        return chaine


if __name__ == "__main__":
    logger.info('#### DEBUT #####')
    # try:
    #     # un = unite('C:\\Projets\\Produits\\DEV\\Scolys\\_Delphi\\_ClientsServeurs\\Database\\Requetes\\Requetes_CoursDEleve.pas')
    #     un = unite('C:\\Projets\\Produits\\DEV\\Scolys\\_Delphi\\_ClientsServeurs\\EdT\\_Clients\\_ClientGraphique\\TableAffEDT_VolumesHoraires.pas')
    # except re.error as e:
    #     print(e.pattern)
    # print(un)

    ensemble = None
    ensemble = cEnsembleUnite('C:\\Projets\\Produits\\DEV')
    ensemble.lire_dpr('Scolys\\_Delphi\\_ClientsServeurs\\EdT\\_Clients\\_ClientGraphique\\_Monoposte\\MonoposteEdT.dpr')

    ensemble.check_uses_non_utilise()
    print(codecs.encode(str(ensemble.unites['NetBaseSco'.upper()]), encoding='iso8859', errors='ignore'))

    # ensemble = cEnsembleUnite('/home/sigfreids/code_delphi')
    # ensemble.analyser(avec_type_interface=True)
    # print(ensemble)
    # print(ensemble.unites['FicheSco_AssisstantHoraireAffiche'].uses_interface.analyse_uses(ensemble, ''))

    # for nom_unite in ensemble.unites:
    #     match = re.finditer(r'\.Masquer\s*\(?\s*\)?\s*;', ensemble.unites[nom_unite].data.data, re.IGNORECASE)
    #     taille = [ensemble.unites[nom_unite].data.num_ligne(x.start(0)) for x in match]
    #     if len(taille) > 0:
    #         taille_detaille = []
    #         for x in re.finditer(r'FINALLY.*?(Masquer\s*\(?\s*\)?\s*;).*?END', ensemble.unites[nom_unite].data.data, re.IGNORECASE):
    #             taille_detaille.append(ensemble.unites[nom_unite].data.num_ligne(x.start(1)))
    #         if len(taille) > len(taille_detaille):
    #             print('\tTrouve dans %s <%s>' % (nom_unite, str([x for x in taille if x not in taille_detaille])))

    ensemble.save()
    # un = unite('C:\\Projets\\Produits\\DEV\\Scolys\\_Delphi\\_ClientsServeurs\\FicheSco_AssisstantHoraireAffiche.pas')
    # un = unite('/home/sigfreids/code_delphi/EditSco_Cours.pas')
    # un.analyse_type_interface()
    # print(un)
# with open('Q:\\test.pas', 'w') as f:
#     entire_file = ''
#     with open('C:\\Projets\\Produits\\DEV\\Scolys\\_Delphi\\_ClientsServeurs\\Database\\Requetes\\Requetes_CoursDEleve.pas', 'r') as unite_file:
#         ligne_pre_uses = un.gestion_ml.num_ligne(un.uses_inter_pos[0])
#         pos_pre_uses = un.gestion_ml.pos_num_ligne(ligne_pre_uses + 1)
#         ligne_post_uses = un.gestion_ml.num_ligne(un.uses_inter_pos[1])
#         pos_post_uses = un.gestion_ml.pos_num_ligne(ligne_post_uses + 1)
#         entire_file = unite_file.read()
#     f.write(entire_file[0:pos_pre_uses])
#     f.write(un.uses_interface.analyse_uses(ensemble, '\t\t'))
#     f.write(entire_file[pos_post_uses:])
