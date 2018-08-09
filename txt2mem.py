# -*- coding: utf-8 -*-
import os.path
import collections
import csv
import time
import pickle
def prettyType(type_):
        return(type(type_).__name__)
def check_structure(lobject):
    types_u = list(map(lambda y: prettyType(y), lobject))
    if not 'list' in types_u:
        return('s')
    else:
        if lobject[0] == 'PRub.':
            return('p')
        else:
            return('c')
def key_val2dict(lobject):
    ldict = {}
    ldict[lobject[0]] = lobject[1]
    return(ldict)
def hkey_key_val2dict(lobject):
    ldict = {lobject[0] : {}}
    elems = lobject[1:]
    for elem in elems:
        ldict[lobject[0]][elem[0]] = elem[1]        
    return(ldict)
def prubkom2dict(lobject):
        ldict = {}
        
def prub2dict(lobject):
    ldict = {lobject[0] : {}}
    elems = lobject[1:]
    dict_list = []
    for elem in elems:
        dict_list.append(hkey_key_val2dict(elem))
    for it in range(0, len(dict_list)):
        ldict[lobject[0]][dict_list[it].keys()[0]] = {}
        for itt in range(0, len(dict_list[it].values()[0].keys())):
            ldict[lobject[0]][dict_list[it].keys()[0]][dict_list[it].values()[0].keys()[itt]] = dict_list[it].values()[0].values()[itt]
    return(ldict)
def gen_dict(lobject):
    code_txt = check_structure(lobject)
    if code_txt == 's':
        return(key_val2dict(lobject))
    elif code_txt == 'p':
        return(prub2dict(lobject))
    else:
        return(hkey_key_val2dict(lobject))
def section2dict(lobject):
    section_num = lobject[0]
    ldict = { section_num : {}}
    section_body = {}
    blank_body_list = {}
    sub_list = []
    for blank in lobject[1:]:
        unique_set = set()
        unique_cnt = 0
        if len(blank[0]) == 1:
            blank_number = blank[0][0]
        else:
            blank_number, blank_title = blank[0]
            blank_body_list[blank_number] = {}
        for key_val in blank[1:]:
            key_val_dict = gen_dict(key_val)
            if (blank_number, key_val_dict.keys()[0]) in unique_set:
                    unique_cnt = unique_cnt + 1
                    blank_body_list[blank_number][key_val_dict.keys()[0] + '_' + str(unique_cnt)] = key_val_dict.values()[0]
            else:
                    unique_set.add((blank_number, key_val_dict.keys()[0]))
                    blank_body_list[blank_number][key_val_dict.keys()[0]] = key_val_dict.values()[0]    
        sub_list.append(blank_body_list)
    ldict[section_num] = blank_body_list
    return(section_num,ldict)
def body2dict(lobject):
    ldict = {}
    for section in lobject:
        section_num, section_dict = section2dict(section)
        ldict[section_num] = section_dict
    return(ldict)
def header2dict(lobject):
    header_list = lobject[0]
    ldict = dict.fromkeys(['poz', 'nazwa', 'krs', 'data_wpisu'])
    for i in range(0,len(header_list)):
         ldict[ldict.keys()[i]] = header_list[i]
    return(ldict)
def lframe2dframe(lobject):
    return({'header' : header2dict(lobject), 'body' : body2dict(lobject[1:])})
class Framef:
        def __init__(self, lframe):
                self.frame = lframe2dframe(lframe)
        def print_frame(self):
                print(self.frame)
def extract_header(frame):
        header_dict = frame['header']
        return(header_dict)
class EcoEntity:
        csv_headers = ['POZ', 'NAZWA_PODM', 'KRS', 'DATA_WPISU']
        def __init__(self, frame):
                self.header = extract_header(frame)
                self.body = dict.fromkeys([str(i) for i in range(1,7)])       
        def fill_body(self, frame):
                frame_keys = frame['body'].keys()
                for sec_num in frame_keys:
                                self.body[str(sec_num)] = frame['body'][str(sec_num)]
        def write_csv(self):
                pass
        def update(self):
                pass
        def get_type(self):
                return(self.body['1']['1']['1']['1'])
def merge_info(ltobject1, ltobject2):
        for item in ltobject1:
                for item2 in ltobject2:
                        if not len(set(item) & set(item2)):
                                item.append(('9', 'NIE'))
                        else:
                                item.append(('9', 'TAK'))
        return(ltobject1)
def fill_blank(eeobject, blank_number, spec = None):
        blank_num = 0
        all_keys = []
        if blank_number == '1':
                blank_num = 6
                all_keys = [str(i) for i in range(1, blank_num+1)]
        elif blank_number == '2':
                if spec == '1':
                        all_keys = ['kraj', 'wojewodztwo', 'powiat', 'gmina', 'miejscowosc']
                elif spec == '2':
                        all_keys = ['ulica', 'nr domu', 'nr lokalu', 'miejscowosc', 'kod pocztowy', 'poczta', 'kraj']
                elif spec == '3':
                        all_keys = ['kraj', 'jednostka podzialu terytorialnego', 'miejscowosc', 'nr domu', 'nr lokalu', 'kod pocztowy', 'poczta', 'ulica']
        available_keys = set(eeobject.keys()) & set(all_keys)
        for item in all_keys:
                if item in set(all_keys) - set(available_keys):
                        eeobject[item] = 'None'
                else:
                        pass
        if blank_number == '2':
                return(collections.OrderedDict(sorted(eeobject.items(), key = lambda x: all_keys.index(x[0]))).values())
        else:
                return(collections.OrderedDict(sorted(eeobject.items())).values())

        

        
        
        
def get_body_info(eeobject):
        object_type = eeobject.get_type()
        if object_type == 'SPOLKA JAWNA':
                entity_info = []
                source_info = []
                aso_entity_info = []
                repr_entity_info = []
                prok_entity_info = []
                entity_blanks = ['1', '2', '3', '5']
                eeobject = eeobject.body
                filled_keys = list(set(entity_blanks) & set(eeobject['1']['1'].keys()))
                for blank in entity_blanks:
                        if blank == '2' and blank in filled_keys:
                                entity_info.extend(fill_blank(eeobject['1']['1'][blank]['1'], blank, '1'))
                                entity_info.extend(fill_blank(eeobject['1']['1'][blank]['2'], blank, '2'))
                                continue
                        elif blank == '3' and blank in filled_keys:
                                entity_info.extend([len(eeobject['1']['1'][blank].keys())])
                                continue
                        elif blank == '3' and blank not in filled_keys:
                                entity_info.extend([0])
                                continue
                        elif blank == '5' and blank in filled_keys:
                                ee_time = eeobject['1']['1'][blank]['1']
                                ee_code = '.'.join(map(str, eeobject['3']['3']['1']['1']['1']))
                                entity_info.extend([ee_time, ee_code])
                                break
                        else:
                                pass
                        entity_info.extend(fill_blank(eeobject['1']['1'][blank], blank))
                source_blanks = ['1', 'PRub.']
                filled_keys = list(set(source_blanks) & set(eeobject['1']['1']['6'].keys()))
                for blank in filled_keys:
                        if blank == '1':
                                source_info.extend([eeobject['1']['1']['6'][blank]])
                        if blank == 'PRub.':
                                hkey_num = len(eeobject['1']['1']['6'][blank].keys())
                                for hkey in range(hkey_num, hkey_num+1):
                                        source_info.extend([eeobject['1']['1']['6'][blank][str(hkey)].values()])
                aso_blanks = ['7']
                aso_blanks2 = ['1', '2'] 
                filled_keys = list(set(aso_blanks) & set(eeobject['1']['1'].keys()))
                filled_keys2 = list(set(aso_blanks2) & set(eeobject['2']['2'].keys()))
                for blank in filled_keys:
                        aso_num = len(eeobject['1']['1'][blank].keys())
                        entity_info.extend([aso_num])
                        aso_keys = ['1', '2', '3', '4', '5', '6', '7', '8']
                        for aso in range(1, aso_num+1):
                                aso_list = []
                                filled_aso_keys = list(set(aso_keys) & set(eeobject['1']['1'][blank][str(aso)].keys()))
                                for aso_key in filled_aso_keys:
                                        aso_list.append((str(aso_key),eeobject['1']['1'][blank][str(aso)][aso_key]))
                                aso_entity_info.extend([aso_list])
                for blank in filled_keys2:
                        if blank == '1':                                
                                if 'PRub.' in eeobject['2']['2'][blank].keys():
                                        repr_num = len(eeobject['2']['2'][blank]['PRub.'].keys())
                                        for repr_ in range(1, repr_num+1):
                                                hkey = len(eeobject['2']['2'][blank]['PRub.'][str(repr_)])
                                                repr_list = []
                                                for hkey_ in range(1, hkey+1):
                                                        repr_list.append((str(hkey_), eeobject['2']['2'][blank]['PRub.']\
                                                                  [str(repr_)][str(hkey_)]))
                                        repr_entity_info.extend([repr_list])
                                else:
                                        pass
                        elif blank == '3':
                                prok_num = len(eeobject['2']['2'][blank].keys())
                                for prok in range(1, prok_num+1):
                                        prok_entity_info.expand([eeobject['2']['2'][blank][str(prok)].values()])
                return(entity_info, source_info, merge_info(aso_entity_info, repr_entity_info))
######################################################################################################################################
        if object_type == 'SPOLKA Z OGRANICZONA ODPOWIEDZIALNOSCIA':
                entity_info = []
                source_info = []
                aso_entity_info = []
                repr_entity_info = []
                prok_entity_info = []
                entity_blanks = ['1', '2', '3', '5']
                eeobject = eeobject.body
                filled_keys = list(set(entity_blanks) & set(eeobject['1']['1'].keys()))
                for blank in entity_blanks:
                        if blank == '2' and blank in filled_keys:
                               entity_info.extend(fill_blank(eeobject['1']['1'][blank]['1'], blank, '1'))
                               entity_info.extend(fill_blank(eeobject['1']['1'][blank]['2'], blank, '2'))
                               continue
                        elif blank == '3' and blank in filled_keys:
                                entity_info.extend([len(eeobject['1']['1'][blank].keys())])
                                continue
                        elif blank == '3' and blank not in filled_keys:
                                entity_info.extend([0])
                                continue
                        elif blank == '5' and blank in filled_keys:
                                ee_time = eeobject['1']['1'][blank]['1']
                                ee_code = '.'.join(map(str, eeobject['3']['3']['1']['1']['1']))
                                entity_info.extend([ee_time, ee_code])
                                break
                        else:
                                pass
                        entity_info.extend(fill_blank(eeobject['1']['1'][blank], blank))
                source_blanks = ['1', 'PRub.']
                if '6' in eeobject['1']['1'].keys():
                        filled_keys = list(set(source_blanks) & set(eeobject['1']['1']['6'].keys()))
                        for blank in filled_keys:
                                if blank == '1':
                                        source_info.extend([eeobject['1']['1']['6'][blank]])
                                        if blank == 'PRub.':
                                                hkey_num = len(eeobject['1']['1']['6'][blank].keys())
                                                for hkey in range(hkey_num, hkey_num+1):
                                                        source_info.extend([eeobject['1']['1']['6'][blank][str(hkey)].values()])
                aso_blanks = ['7', '8']
                aso_blanks2 = ['1', '2', '3'] 
                filled_keys = list(set(aso_blanks) & set(eeobject['1']['1'].keys()))
                filled_keys2 = list(set(aso_blanks2) & set(eeobject['2']['2'].keys()))
                for blank in filled_keys:
                        if blank == '7':
                                aso_num = len(eeobject['1']['1'][blank].keys())
                                entity_info.extend([aso_num])
                                aso_keys = ['1', '2', '3', '4', '5', '6']
                                for aso in range(1, aso_num+1):
                                        aso_list = []
                                        filled_aso_keys = list(set(aso_keys) & set(eeobject['1']['1'][blank][str(aso)].keys()))
                                        for aso_key in filled_aso_keys:
                                                aso_list.append((str(aso_key),eeobject['1']['1'][blank][str(aso)][aso_key]))
                                        aso_entity_info.extend([aso_list])
                        elif blank == '8':
                                entity_info.extend(eeobject['1']['1'][blank].values())
                for blank in filled_keys2:
                        if blank == '1':                                
                                if 'PRub.' in eeobject['2']['2'][blank].keys():
                                        repr_num = len(eeobject['2']['2'][blank]['PRub.'].keys())
                                        for repr_ in range(1, repr_num+1):
                                                hkey = len(eeobject['2']['2'][blank]['PRub.'][str(repr_)])
                                                repr_list = []
                                                for hkey_ in eeobject['2']['2'][blank]['PRub.'][str(repr_)].keys():
                                                        repr_list.append((str(hkey_), eeobject['2']['2'][blank]['PRub.']\
                                                                  [str(repr_)][hkey_]))
                                                repr_entity_info.extend([repr_list])
                                else:
                                        pass
                        elif blank == '3':
                                prok_num = len(eeobject['2']['2'][blank].keys())
                                for prok in range(1, prok_num+1):
                                        prok_entity_info.expand([eeobject['2']['2'][blank][str(prok)].values()])
                entity_info[-1] = aso_update(repr_entity_info, aso_entity_info)
                return(entity_info, source_info, aso_entity_info, repr_entity_info)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        if object_type == 'SPOLKA KOMANDYTOWA':
                entity_info = []
                source_info = []
                aso_entity_info = []
                repr_entity_info = []
                prok_entity_info = []
                entity_blanks = ['1', '2', '3', '5']
                eeobject = eeobject.body
                filled_keys = list(set(entity_blanks) & set(eeobject['1']['1'].keys()))
                for blank in entity_blanks:
                        if blank == '2' and blank in filled_keys:
                               entity_info.extend(fill_blank(eeobject['1']['1'][blank]['1'], blank, '1'))
                               entity_info.extend(fill_blank(eeobject['1']['1'][blank]['2'], blank, '2'))
                               continue
                        elif blank == '3' and blank in filled_keys:
                                entity_info.extend([len(eeobject['1']['1'][blank].keys())])
                                continue
                        elif blank == '3' and blank not in filled_keys:
                                entity_info.extend([0])
                                continue
                        elif blank == '5' and blank in filled_keys:
                                ee_time = eeobject['1']['1'][blank]['1']
                                ee_code = '.'.join(map(str, eeobject['3']['3']['1']['1']['1']))
                                entity_info.extend([ee_time, ee_code])
                                break
                        else:
                                pass
                        entity_info.extend(fill_blank(eeobject['1']['1'][blank], blank))
                source_blanks = ['1', 'PRub.']
                if '6' in eeobject['1']['1'].keys():
                        filled_keys = list(set(source_blanks) & set(eeobject['1']['1']['6'].keys()))
                        for blank in filled_keys:
                                if blank == '1':
                                        source_info.extend([eeobject['1']['1']['6'][blank]])
                                elif blank == 'PRub.':
                                        hkey_num = len(eeobject['1']['1']['6'][blank].keys())
                                        for hkey in range(hkey_num, hkey_num+1):
                                                source_info.extend([eeobject['1']['1']['6'][blank][str(hkey)].values()])
                aso_blanks = ['7', '8']
                aso_blanks2 = ['1', '2', '3'] 
                filled_keys = list(set(aso_blanks) & set(eeobject['1']['1'].keys()))
                filled_keys2 = list(set(aso_blanks2) & set(eeobject['2']['2'].keys()))
                for blank in filled_keys:
                        if blank == '7':
                                aso_num = eeobject['1']['1'][blank].keys()
                                entity_info.extend([aso_num])
                                aso_keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
                                for aso in aso_num:
                                        aso_list = []
                                        if aso in eeobject['1']['1'][blank].keys()[1:]:
                                                filled_aso_keys = list(set(aso_keys) & set(eeobject['1']['1'][blank][aso][eeobject['1']['1'][blank][aso].keys()[1]]))
                                        else:
                                                filled_aso_keys = list(set(aso_keys) & set(eeobject['1']['1'][blank][aso].keys()))
                                        for aso_key in filled_aso_keys:
                                                if aso in eeobject['1']['1'][blank].keys()[1:]:
                                                        aso_list.append((str(aso_key), eeobject['1']['1'][blank][aso][eeobject['1']['1'][blank][aso].keys()[1]][aso_key]))
                                                else:
                                                        aso_list.append((str(aso_key),eeobject['1']['1'][blank][aso][aso_key]))
                                        aso_entity_info.extend([aso_list])
                        elif blank == '8':
                                entity_info.extend(eeobject['1']['1'][blank].values())
                for blank in filled_keys2:
                        if blank == '1':                                
                                if 'PRub.' in eeobject['2']['2'][blank].keys():
                                        repr_num = len(eeobject['2']['2'][blank]['PRub.'].keys())
                                        for repr_ in range(1, repr_num+1):
                                                hkey = len(eeobject['2']['2'][blank]['PRub.'][str(repr_)])
                                                repr_list = []
                                                for hkey_ in eeobject['2']['2'][blank]['PRub.'][str(repr_)].keys():
                                                        repr_list.append((str(hkey_), eeobject['2']['2'][blank]['PRub.']\
                                                                  [str(repr_)][hkey_]))
                                                        
                                        repr_entity_info.extend([repr_list])
                                else:
                                        pass
                        elif blank == '3':
                                prok_num = len(eeobject['2']['2'][blank].keys())
                                for prok in range(1, prok_num+1):
                                        prok_entity_info.expand([eeobject['2']['2'][blank][str(prok)].values()])
                entity_info[-1] = aso_update(repr_entity_info, aso_entity_info)
                return(entity_info, source_info, aso_entity_info, repr_entity_info)
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^        
        if object_type == 'SPOLKA AKCYJNA':                
                entity_info = []
                source_info = []
                action_info = []
                aso_entity_info = []
                repr_entity_info = []
                prok_entity_info = []
                entity_blanks = ['1', '2', '3', '5', '8', '9']
                eeobject = eeobject.body
                filled_keys = list(set(entity_blanks) & set(eeobject['1']['1'].keys()))
                for blank in entity_blanks:
                        if blank == '2' and blank in filled_keys:
                               entity_info.extend(fill_blank(eeobject['1']['1'][blank]['1'], blank, '1'))
                               entity_info.extend(fill_blank(eeobject['1']['1'][blank]['2'], blank, '2'))
                               continue
                        elif blank == '3' and blank in filled_keys:
                                entity_info.extend([len(eeobject['1']['1'][blank].keys())])
                                continue
                        elif blank == '3' and blank not in filled_keys:
                                entity_info.extend([0])
                                continue
                        elif blank == '5' and blank in filled_keys:
                                ee_time = eeobject['1']['1'][blank]['1']
                                ee_code = '.'.join(map(str, eeobject['3']['3']['1']['1']['1']))
                                entity_info.extend([ee_time, ee_code])
                                continue
                        elif blank == '8' and blank in filled_keys:
                                blank_keys = [str(i) for i in range(1, 7)]
                                eeobject['1']['1'][blank] = collections.OrderedDict(sorted(eeobject['1']['1'][blank].items()))
                                for filled in blank_keys:
                                        if filled in eeobject['1']['1'][blank].keys():
                                                entity_info.extend([eeobject['1']['1'][blank][filled]])
                                        else:
                                                entity_info.extend(['None'])
                                continue
                        elif blank == '9' and blank in filled_keys:
                                blank_keys = [str(i) for i in range(1, 4)]
                                hkeys = collections.OrderedDict(sorted(eeobject['1']['1'][blank].items())).keys()
                                for hkey in hkeys:
                                        sub_action = []
                                        eeobject['1']['1'][blank][hkey] = collections.OrderedDict(sorted(eeobject['1']['1'][blank][hkey].items()))
                                        
                                        for filled in blank_keys:
                                                if filled in eeobject['1']['1'][blank][hkey].keys():
                                                        sub_action.extend([eeobject['1']['1'][blank][hkey][filled]])
                                                else:
                                                        sub_action.extend(['None'])
                                        action_info.extend([sub_action])
                                break
                        else:
                                pass
                        
                        entity_info.extend(fill_blank(eeobject['1']['1'][blank], blank))
                source_blanks = ['1', 'PRub.']
                if '6' in eeobject['1']['1'].keys():
                        filled_keys = list(set(source_blanks) & set(eeobject['1']['1']['6'].keys()))
                        for blank in filled_keys:
                                if blank == '1':
                                        source_info.extend([eeobject['1']['1']['6'][blank]])
                                elif blank == 'PRub.':
                                        hkey_num = len(eeobject['1']['1']['6'][blank].keys())
                                        for hkey in range(hkey_num, hkey_num+1):
                                                source_info.extend([eeobject['1']['1']['6'][blank][str(hkey)].values()])
                aso_blanks = ['2', '8']
                aso_blanks2 = ['1', '2', '3'] 
                filled_keys = list(set(aso_blanks) & set(eeobject['1']['1'].keys()))
                filled_keys2 = list(set(aso_blanks2) & set(eeobject['2']['2'].keys()))
                for blank in filled_keys:
                        if blank == '2':
                                eeobject['2']['2'][blank]['PRub.'] = collections.OrderedDict(sorted(eeobject['2']['2'][blank]['PRub.'].items()))
                                aso_num = eeobject['2']['2'][blank]['PRub.'].keys()
                                #entity_info.extend([aso_num])
                                aso_keys = ['1', '2', '3']
                                for aso in aso_num:
                                        sub_aso = []
                                        for filled in aso_keys:
                                                if filled in eeobject['2']['2'][blank]['PRub.'][aso].keys():
                                                        sub_aso.extend([eeobject['2']['2'][blank]['PRub.'][aso][filled]])
                                                else:
                                                        sub_aso.extend(['None'])
                                        aso_entity_info.extend([sub_aso])
                        elif blank == '8':
                                entity_info.extend(eeobject['1']['1'][blank].values())
                for blank in filled_keys2:
                        if blank == '1':                                
                                if 'PRub.' in eeobject['2']['2'][blank].keys():
                                        repr_num = len(eeobject['2']['2'][blank]['PRub.'].keys())
                                        for repr_ in range(1, repr_num+1):
                                                hkey = len(eeobject['2']['2'][blank]['PRub.'][str(repr_)])
                                                repr_list = []
                                                for hkey_ in eeobject['2']['2'][blank]['PRub.'][str(repr_)].keys():
                                                        repr_list.append((str(hkey_), eeobject['2']['2'][blank]['PRub.']\
                                                                  [str(repr_)][hkey_]))
                                                        
                                        repr_entity_info.extend([repr_list])
                                else:
                                        pass
                        elif blank == '3':
                                prok_num = len(eeobject['2']['2'][blank].keys())
                                for prok in range(1, prok_num+1):
                                        prok_entity_info.expand([eeobject['2']['2'][blank][str(prok)].values()])
                entity_info[-1] = aso_update(repr_entity_info, aso_entity_info, typ='1')
                return(entity_info, source_info, aso_entity_info, repr_entity_info, action_info)
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        if object_type == 'SPOLKA KOMANDYTOWO-AKCYJNA':
                entity_info = []
		action_info = []
                source_info = []
                aso_entity_info = []
                repr_entity_info = []
                prok_entity_info = []
                entity_blanks = ['1', '2', '3', '5', '8', '9']
                eeobject = eeobject.body
                filled_keys = list(set(entity_blanks) & set(eeobject['1']['1'].keys()))
                for blank in entity_blanks:
                        if blank == '2' and blank in filled_keys:
                               entity_info.extend(fill_blank(eeobject['1']['1'][blank]['1'], blank, '1'))
                               entity_info.extend(fill_blank(eeobject['1']['1'][blank]['2'], blank, '2'))
                               continue
                        elif blank == '3' and blank in filled_keys:
                                entity_info.extend([len(eeobject['1']['1'][blank].keys())])
                                continue
                        elif blank == '3' and blank not in filled_keys:
                                entity_info.extend([0])
                                continue
                        elif blank == '5' and blank in filled_keys:
                                ee_time = eeobject['1']['1'][blank]['1']
                                ee_code = '.'.join(map(str, eeobject['3']['3']['1']['1']['1']))
                                entity_info.extend([ee_time, ee_code])
                                continue
			elif blank == '8' and blank in filled_keys:
                                blank_keys = [str(i) for i in range(1, 7)]
                                eeobject['1']['1'][blank] = collections.OrderedDict(sorted(eeobject['1']['1'][blank].items()))
                                for filled in blank_keys:
                                        if filled in eeobject['1']['1'][blank].keys():
                                                entity_info.extend([eeobject['1']['1'][blank][filled]])
                                        else:
                                                entity_info.extend(['None'])
                                continue
			elif blank == '9' and blank in filled_keys:
                                blank_keys = [str(i) for i in range(1, 4)]
                                hkeys = collections.OrderedDict(sorted(eeobject['1']['1'][blank].items())).keys()
                                for hkey in hkeys:
                                        sub_action = []
                                        eeobject['1']['1'][blank][hkey] = collections.OrderedDict(sorted(eeobject['1']['1'][blank][hkey].items()))
                                        
                                        for filled in blank_keys:
                                                if filled in eeobject['1']['1'][blank][hkey].keys():
                                                        sub_action.extend([eeobject['1']['1'][blank][hkey][filled]])
                                                else:
                                                        sub_action.extend(['None'])
                                        action_info.extend([sub_action])
                                break

                        else:
                                pass
                        entity_info.extend(fill_blank(eeobject['1']['1'][blank], blank))
                source_blanks = ['1', 'PRub.']
                if '6' in eeobject['1']['1'].keys():
                        filled_keys = list(set(source_blanks) & set(eeobject['1']['1']['6'].keys()))
                        for blank in filled_keys:
                                if blank == '1':
                                        source_info.extend([eeobject['1']['1']['6'][blank]])
                                elif blank == 'PRub.':
                                        hkey_num = len(eeobject['1']['1']['6'][blank].keys())
                                        for hkey in range(hkey_num, hkey_num+1):
                                                source_info.extend([eeobject['1']['1']['6'][blank][str(hkey)].values()])
                aso_blanks = ['7']
                aso_blanks2 = ['1', '2', '3'] 
                filled_keys = list(set(aso_blanks) & set(eeobject['1']['1'].keys()))
                filled_keys2 = list(set(aso_blanks2) & set(eeobject['2']['2'].keys()))
                for blank in filled_keys:
                        if blank == '7':
                                aso_num = eeobject['1']['1'][blank].keys()
                                entity_info.extend([aso_num])
                                aso_keys = ['1', '2', '3', '4', '5', '6', '7']
                                for aso in aso_num:
                                        aso_list = []
                                        if aso in eeobject['1']['1'][blank].keys()[1:]:
                                                filled_aso_keys = list(set(aso_keys) & set(eeobject['1']['1'][blank][aso][eeobject['1']['1'][blank][aso].keys()[1]]))
                                        else:
                                                filled_aso_keys = list(set(aso_keys) & set(eeobject['1']['1'][blank][aso].keys()))
                                        for aso_key in filled_aso_keys:
                                                if aso in eeobject['1']['1'][blank].keys()[1:]:
                                                        aso_list.append((str(aso_key), eeobject['1']['1'][blank][aso][eeobject['1']['1'][blank][aso].keys()[1]][aso_key]))
                                                else:
                                                        aso_list.append((str(aso_key),eeobject['1']['1'][blank][aso][aso_key]))
                                        aso_entity_info.extend([aso_list])
                        elif blank == '8':
                                entity_info.extend(eeobject['1']['1'][blank].values())
                for blank in filled_keys2:
                        if blank == '1':                                
                                if 'PRub.' in eeobject['2']['2'][blank].keys():
                                        repr_num = len(eeobject['2']['2'][blank]['PRub.'].keys())
                                        for repr_ in range(1, repr_num+1):
                                                hkey = len(eeobject['2']['2'][blank]['PRub.'][str(repr_)])
                                                repr_list = []
                                                for hkey_ in eeobject['2']['2'][blank]['PRub.'][str(repr_)].keys():
                                                        repr_list.append((str(hkey_), eeobject['2']['2'][blank]['PRub.']\
                                                                  [str(repr_)][hkey_]))
                                                        
                                        repr_entity_info.extend([repr_list])
                                else:
                                        pass
                        elif blank == '3':
                                prok_num = len(eeobject['2']['2'][blank].keys())
                                for prok in range(1, prok_num+1):
                                        prok_entity_info.expand([eeobject['2']['2'][blank][str(prok)].values()])
                entity_info[-1] = aso_update(repr_entity_info, aso_entity_info)
                return(entity_info, source_info, aso_entity_info, repr_entity_info, action_info)
#(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
	if object_type == 'SPOLDZIELNIA':
                entity_info = []
                source_info = []
                aso_entity_info = []
                repr_entity_info = []
                prok_entity_info = []
                proxy_entity_info = []
                entity_blanks = ['1', '2', '3', '5']
                eeobject = eeobject.body
                filled_keys = list(set(entity_blanks) & set(eeobject['1']['1'].keys()))
                for blank in entity_blanks:
                        if blank == '2' and blank in filled_keys:
                               entity_info.extend(fill_blank(eeobject['1']['1'][blank]['1'], blank, '1'))
                               entity_info.extend(fill_blank(eeobject['1']['1'][blank]['2'], blank, '2'))
                               continue
                        elif blank == '3' and blank in filled_keys:
                                entity_info.extend([len(eeobject['1']['1'][blank].keys())])
                                continue
                        elif blank == '3' and blank not in filled_keys:
                                entity_info.extend([0])
                                continue
                        elif blank == '5' and blank in filled_keys:
                                ee_time = eeobject['1']['1'][blank]['1']
                                ee_code = '.'.join(map(str, eeobject['3']['3']['1']['1']['1']))
                                entity_info.extend([ee_time, ee_code])
                                break
                        else:
                                pass
                        entity_info.extend(fill_blank(eeobject['1']['1'][blank], blank))
                source_blanks = ['1', 'PRub.']
                if '6' in eeobject['1']['1'].keys():
                        filled_keys = list(set(source_blanks) & set(eeobject['1']['1']['6'].keys()))
                        for blank in filled_keys:
                                if blank == '1':
                                        source_info.extend([eeobject['1']['1']['6'][blank]])
                                elif blank == 'PRub.':
                                        hkey_num = len(eeobject['1']['1']['6'][blank].keys())
                                        for hkey in range(hkey_num, hkey_num+1):
                                                source_info.extend([eeobject['1']['1']['6'][blank][str(hkey)].values()])
                aso_blanks = ['7', '8']
                aso_blanks2 = ['1', '2', '3', '4'] 
                filled_keys = list(set(aso_blanks) & set(eeobject['1']['1'].keys()))
                filled_keys2 = list(set(aso_blanks2) & set(eeobject['2']['2'].keys()))
                for blank in filled_keys:
                        if blank == '7':
                                aso_num = eeobject['1']['1'][blank].keys()
                                entity_info.extend([aso_num])
                                aso_keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
                                for aso in aso_num:
                                        aso_list = []
                                        if aso in eeobject['1']['1'][blank].keys()[1:]:
                                                filled_aso_keys = list(set(aso_keys) & set(eeobject['1']['1'][blank][aso][eeobject['1']['1'][blank][aso].keys()[1]]))
                                        else:
                                                filled_aso_keys = list(set(aso_keys) & set(eeobject['1']['1'][blank][aso].keys()))
                                        for aso_key in filled_aso_keys:
                                                if aso in eeobject['1']['1'][blank].keys()[1:]:
                                                        aso_list.append((str(aso_key), eeobject['1']['1'][blank][aso][eeobject['1']['1'][blank][aso].keys()[1]][aso_key]))
                                                else:
                                                        aso_list.append((str(aso_key),eeobject['1']['1'][blank][aso][aso_key]))
                                        aso_entity_info.extend([aso_list])
                        elif blank == '8':
                                entity_info.extend(eeobject['1']['1'][blank].values())
                for blank in filled_keys2:
                        if blank == '1':                                
                                if 'PRub.' in eeobject['2']['2'][blank].keys():
                                        repr_num = len(eeobject['2']['2'][blank]['PRub.'].keys())
                                        for repr_ in range(1, repr_num+1):
                                                hkey = len(eeobject['2']['2'][blank]['PRub.'][str(repr_)])
                                                repr_list = []
                                                for hkey_ in eeobject['2']['2'][blank]['PRub.'][str(repr_)].keys():
                                                        repr_list.append((str(hkey_), eeobject['2']['2'][blank]['PRub.']\
                                                                  [str(repr_)][hkey_]))

                                                repr_entity_info.extend([repr_list])
                                else:
                                        pass
                        elif blank == '3':
                                prok_num = len(eeobject['2']['2'][blank].keys())
                                for prok in range(1, prok_num+1):
                                        prok_entity_info.expand([eeobject['2']['2'][blank][str(prok)].values()])
                        elif blank == '4':
                                eeobject['2']['2'][blank] = collections.OrderedDict(sorted(eeobject['2']['2'][blank].items()))
                                proxy_num = len(eeobject['2']['2'][blank].keys())
                                prox_keys = ['1', '2', '3', '4']
                                for proxy in range(1, proxy_num+1):
                                    prox_list = []
                                    for proxy_key in eeobject['2']['2'][blank][str(proxy)].keys():    
                                        if proxy_key in prox_keys:
                                            prox_list.append(eeobject['2']['2'][blank][str(proxy)][proxy_key])
                                        else:
                                            prox_list.append("None")
                                    proxy_entity_info.append(prox_list) 
                entity_info[-1] = aso_update(repr_entity_info, aso_entity_info,'Spol', proxy_entity_info)
                return(entity_info, source_info, aso_entity_info, repr_entity_info, proxy_entity_info)
        elif object_type == 'STOWARZYSZENIE':
                entity_info = []
                source_info = []
                aso_entity_info = []
                repr_entity_info = []
                prok_entity_info = []
                entity_blanks = ['1', '2', '3', '5']
                eeobject = eeobject.body
                filled_keys = list(set(entity_blanks) & set(eeobject['1']['1'].keys()))
                for blank in entity_blanks:
                        if blank == '2' and blank in filled_keys:
                               entity_info.extend(fill_blank(eeobject['1']['1'][blank]['1'], blank, '1'))
                               entity_info.extend(fill_blank(eeobject['1']['1'][blank]['2'], blank, '2'))
                               continue
                        elif blank == '3' and blank in filled_keys:
                                entity_info.extend([len(eeobject['1']['1'][blank].keys())])
                                continue
                        elif blank == '3' and blank not in filled_keys:
                                entity_info.extend([0])
                                continue
                        elif blank == '5' and blank in filled_keys:
                                ee_time = eeobject['1']['1'][blank]['1']
                                ee_code = '.'.join(map(str, eeobject['3']['3']['1']['1']['1']))
                                entity_info.extend([ee_time, ee_code])
                                break
                        else:
                                pass
                        entity_info.extend(fill_blank(eeobject['1']['1'][blank], blank))
                source_blanks = ['1', 'PRub.']
                if '6' in eeobject['1']['1'].keys():
                        filled_keys = list(set(source_blanks) & set(eeobject['1']['1']['6'].keys()))
                        for blank in filled_keys:
                                if blank == '1':
                                        source_info.extend([eeobject['1']['1']['6'][blank]])
                                elif blank == 'PRub.':
                                        hkey_num = len(eeobject['1']['1']['6'][blank].keys())
                                        for hkey in range(hkey_num, hkey_num+1):
                                                source_info.extend([eeobject['1']['1']['6'][blank][str(hkey)].values()])
                aso_blanks = ['2', '8']
                aso_blanks2 = ['1', '2', '3', '4'] 
                filled_keys = list(set(aso_blanks) & set(eeobject['1']['1'].keys()))
                filled_keys2 = list(set(aso_blanks2) & set(eeobject['2']['2'].keys()))
                for blank in filled_keys:
                        if blank == '2':
                                eeobject['2']['2'][blank]['PRub.'] = collections.OrderedDict(sorted(eeobject['2']['2'][blank]['PRub.'].items()))
                                aso_num = eeobject['2']['2'][blank]['PRub.'].keys()
                                #entity_info.extend([aso_num])
                                aso_keys = ['1', '2', '3', '4']
                                for aso in aso_num:
                                        sub_aso = []
                                        for filled in aso_keys:
                                                if filled in eeobject['2']['2'][blank]['PRub.'][aso].keys():
                                                        sub_aso.extend([eeobject['2']['2'][blank]['PRub.'][aso][filled]])
                                                else:
                                                        sub_aso.extend(['None'])
                                        sub_aso.extend([eeobject['2']['2']['1']['1']['1']])
                                        aso_entity_info.extend([sub_aso])
                        elif blank == '8':
                                entity_info.extend(eeobject['1']['1'][blank].values())
                for blank in filled_keys2:
                        if blank == '1':                                
                                if 'PRub.' in eeobject['2']['2'][blank].keys():
                                        repr_num = len(eeobject['2']['2'][blank]['PRub.'].keys())
                                        for repr_ in range(1, repr_num+1):
                                                hkey = len(eeobject['2']['2'][blank]['PRub.'][str(repr_)])
                                                repr_list = []
                                                for hkey_ in eeobject['2']['2'][blank]['PRub.'][str(repr_)].keys():
                                                        repr_list.append((str(hkey_), eeobject['2']['2'][blank]['PRub.']\
                                                                  [str(repr_)][hkey_]))

                                                repr_entity_info.extend([repr_list])
                                else:
                                        pass
                        elif blank == '3':
                                prok_num = len(eeobject['2']['2'][blank].keys())
                                for prok in range(1, prok_num+1):
                                        prok_entity_info.expand([eeobject['2']['2'][blank][str(prok)].values()])
                entity_info[-1] = aso_update(repr_entity_info, aso_entity_info)
                return(entity_info, source_info, aso_entity_info, repr_entity_info)
        elif object_type == 'FUNDACJA':
                entity_info = []
                source_info = []
                aso_entity_info = []
                repr_entity_info = []
                prok_entity_info = []
                entity_blanks = ['1', '2', '3', '5']
                eeobject = eeobject.body
                filled_keys = list(set(entity_blanks) & set(eeobject['1']['1'].keys()))
                for blank in entity_blanks:
                        if blank == '2' and blank in filled_keys:
                               entity_info.extend(fill_blank(eeobject['1']['1'][blank]['1'], blank, '1'))
                               entity_info.extend(fill_blank(eeobject['1']['1'][blank]['2'], blank, '2'))
                               continue
                        elif blank == '3' and blank in filled_keys:
                                entity_info.extend([len(eeobject['1']['1'][blank].keys())])
                                continue
                        elif blank == '3' and blank not in filled_keys:
                                entity_info.extend([0])
                                continue
                        elif blank == '5' and blank in filled_keys:
                                ee_time = eeobject['1']['1'][blank]['1']
                                ee_code = '.'.join(map(str, eeobject['3']['3']['1']['1']['1']))
                                entity_info.extend([ee_time, ee_code])
                                break
                        else:
                                pass
                        entity_info.extend(fill_blank(eeobject['1']['1'][blank], blank))
                source_blanks = ['1', 'PRub.']
                if '6' in eeobject['1']['1'].keys():
                        filled_keys = list(set(source_blanks) & set(eeobject['1']['1']['6'].keys()))
                        for blank in filled_keys:
                                if blank == '1':
                                        source_info.extend([eeobject['1']['1']['6'][blank]])
                                elif blank == 'PRub.':
                                        hkey_num = len(eeobject['1']['1']['6'][blank].keys())
                                        for hkey in range(hkey_num, hkey_num+1):
                                                source_info.extend([eeobject['1']['1']['6'][blank][str(hkey)].values()])
                aso_blanks = ['2', '8']
                aso_blanks2 = ['1', '2', '3', '4'] 
                filled_keys = list(set(aso_blanks) & set(eeobject['1']['1'].keys()))
                filled_keys2 = list(set(aso_blanks2) & set(eeobject['2']['2'].keys()))
                for blank in filled_keys:
                        if blank == '2':
                                eeobject['2']['2'][blank]['PRub.'] = collections.OrderedDict(sorted(eeobject['2']['2'][blank]['PRub.'].items()))
                                aso_num = eeobject['2']['2'][blank]['PRub.'].keys()
                                #entity_info.extend([aso_num])
                                aso_keys = ['1', '2', '3', '4']
                                for aso in aso_num:
                                        sub_aso = []
                                        for filled in aso_keys:
                                                if filled in eeobject['2']['2'][blank]['PRub.'][aso].keys():
                                                        sub_aso.extend([eeobject['2']['2'][blank]['PRub.'][aso][filled]])
                                                else:
                                                        sub_aso.extend(['None'])
                                        sub_aso.extend([eeobject['2']['2']['1']['1']['1']])
                                        aso_entity_info.extend([sub_aso])
                        elif blank == '8':
                                entity_info.extend(eeobject['1']['1'][blank].values())
                for blank in filled_keys2:
                        if blank == '1':                                
                                if 'PRub.' in eeobject['2']['2'][blank].keys():
                                        repr_num = len(eeobject['2']['2'][blank]['PRub.'].keys())
                                        for repr_ in range(1, repr_num+1):
                                                hkey = len(eeobject['2']['2'][blank]['PRub.'][str(repr_)])
                                                repr_list = []
                                                for hkey_ in eeobject['2']['2'][blank]['PRub.'][str(repr_)].keys():
                                                        repr_list.append((str(hkey_), eeobject['2']['2'][blank]['PRub.']\
                                                                  [str(repr_)][hkey_]))
                                                repr_entity_info.extend([repr_list])
                                else:
                                        pass
                        elif blank == '3':
                                prok_num = len(eeobject['2']['2'][blank].keys())
                                for prok in range(1, prok_num+1):
                                        prok_entity_info.expand([eeobject['2']['2'][blank][str(prok)].values()])
                entity_info[-1] = aso_update(repr_entity_info, aso_entity_info)
                return(entity_info, source_info, aso_entity_info, repr_entity_info)
        if object_type == 'ODDZIAL ZAGRANICZNEGO PRZEDSIEBIORCY':
                entity_info = []
                source_info = []
                aso_entity_info = []
                repr_entity_info = []
                prok_entity_info = []
                entity_blanks = ['1', '2']
                eeobject = eeobject.body
                filled_keys = list(set(entity_blanks) & set(eeobject['1']['1'].keys()))
                for blank in entity_blanks:
                        if blank == '2' and blank in filled_keys:
                               entity_info.extend(fill_blank(eeobject['1']['1'][blank]['1'], blank, '1'))
                               entity_info.extend(fill_blank(eeobject['1']['1'][blank]['2'], blank, '2'))
                               entity_info.extend(fill_blank(eeobject['1']['1'][blank]['3'], blank, '3'))
                               continue
                        elif blank == '3' and blank in filled_keys:
                                entity_info.extend([len(eeobject['1']['1'][blank].keys())])
                                continue
                        elif blank == '3' and blank not in filled_keys:
                                entity_info.extend([0])
                                continue
                        elif blank == '5' and blank in filled_keys:
                                ee_time = eeobject['1']['1'][blank]['1']
                                ee_code = '.'.join(map(str, eeobject['3']['3']['1']['1']['1']))
                                entity_info.extend([ee_time, ee_code])
                                break
                        else:
                                pass
                        entity_info.extend(fill_blank(eeobject['1']['1'][blank], blank))
                source_blanks = ['1', 'PRub.']
                if '6' in eeobject['1']['1'].keys():
                        filled_keys = list(set(source_blanks) & set(eeobject['1']['1']['6'].keys()))
                        for blank in filled_keys:
                                if blank == '1':
                                        source_info.extend([eeobject['1']['1']['6'][blank]])
                                elif blank == 'PRub.':
                                        hkey_num = len(eeobject['1']['1']['6'][blank].keys())
                                        for hkey in range(hkey_num, hkey_num+1):
                                                source_info.extend([eeobject['1']['1']['6'][blank][str(hkey)].values()])
                aso_blanks = ['4', '8']
                aso_blanks2 = ['1', '2', '3', '4'] 
                filled_keys = list(set(aso_blanks) & set(eeobject['2']['2'].keys()))
                filled_keys2 = list(set(aso_blanks2) & set(eeobject['2']['2'].keys()))
                for blank in filled_keys:
                        if blank == '4':
                                eeobject['2']['2'][blank] = collections.OrderedDict(sorted(eeobject['2']['2'][blank].items()))
                                aso_num = eeobject['2']['2'][blank].keys()
                                #entity_info.extend([aso_num])
                                aso_keys = ['1', '2', '3']
                                for aso in aso_num:
                                        sub_aso = []
                                        for filled in aso_keys:
                                                if filled in eeobject['2']['2'][blank][aso].keys():
                                                        sub_aso.extend([eeobject['2']['2'][blank][aso][filled]])
                                                else:
                                                        sub_aso.extend(['None'])
                                        sub_aso.extend([eeobject['2']['2']['1']['1']['1']])
                                        aso_entity_info.extend([sub_aso])
                        elif blank == '8':
                                entity_info.extend(eeobject['1']['1'][blank].values())
                for blank in filled_keys2:
                        if blank == '1':                                
                                if 'PRub.' in eeobject['2']['2'][blank].keys():
                                        repr_num = len(eeobject['2']['2'][blank]['PRub.'].keys())
                                        for repr_ in range(1, repr_num+1):
                                                hkey = len(eeobject['2']['2'][blank]['PRub.'][str(repr_)])
                                                repr_list = []
                                                for hkey_ in eeobject['2']['2'][blank]['PRub.'][str(repr_)].keys():
                                                        repr_list.append((str(hkey_), eeobject['2']['2'][blank]['PRub.']\
                                                                  [str(repr_)][hkey_]))
                                                repr_entity_info.extend([repr_list])
                                else:
                                        pass
                        elif blank == '3':
                                prok_num = len(eeobject['2']['2'][blank].keys())
                                for prok in range(1, prok_num+1):
                                        prok_entity_info.expand([eeobject['2']['2'][blank][str(prok)].values()])
                entity_info[-1] = aso_update(repr_entity_info, aso_entity_info)
                return(entity_info, source_info, aso_entity_info, repr_entity_info)
	else:
		pass



		            
def get_header_info(eeobject):
        return(eeobject.header.values())
def extract_aso_info(aso_info):
        aso_instance = []
        aso_info_sorted = sorted(aso_info, key = lambda y: int(y[0]))
        available_keys = list(map(lambda x: x[0], aso_info_sorted))
        all_keys = [str(i) for i in range(1, 13)]
        aso_info_sorted = list(map(lambda x: x[1], aso_info_sorted))
        aso_info_sorted.reverse()
        for item in all_keys:
                if item in set(all_keys) - set(available_keys):
                        aso_instance.append('None')
                else:
                        aso_instance.append(aso_info_sorted.pop())
        return(aso_instance)
def extract_aso_info_kom(aso_info):
        aso_instance = []
        aso_info_sorted = sorted(aso_info, key = lambda y: int(y[0]))
        available_keys = list(map(lambda x: x[0], aso_info_sorted))
        all_keys = [str(i) for i in range(1, 13)]
        aso_info_sorted = list(map(lambda x: x[1], aso_info_sorted))
        aso_info_sorted.reverse()
        for item in all_keys:
                if item in set(all_keys) - set(available_keys):
                        aso_instance.append('None')
                else:
                        aso_instance.append(aso_info_sorted.pop())
        return(aso_instance)
def extract_aso_info_zoo(aso_info):
        aso_instance = []
        aso_info_sorted = sorted(aso_info, key = lambda y: y[0])
        available_keys = list(map(lambda x: x[0], aso_info_sorted))
        all_keys = [str(i) for i in range(1, 6)]
        aso_info_sorted = list(map(lambda x: x[1], aso_info_sorted))
        aso_info_sorted.reverse()
        for item in all_keys:
                if item in set(all_keys) - set(available_keys):
                        aso_instance.append('None')
                else:
                        aso_instance.append(aso_info_sorted.pop())
        return(aso_instance)
def extract_repr_info_zoo(aso_info):
        aso_instance = []
        aso_info_sorted = sorted(aso_info, key = lambda y: y[0])
        available_keys = list(map(lambda x: x[0], aso_info_sorted))
        all_keys = [str(i) for i in range(1, 8)]
        aso_info_sorted = list(map(lambda x: x[1], aso_info_sorted))
        aso_info_sorted.reverse()
        for item in all_keys:
                if item in set(all_keys) - set(available_keys):
                        aso_instance.append('None')
                else:
                        aso_instance.append(aso_info_sorted.pop())
        return(aso_instance)
def extract_aso_info_akc(aso_info, typ="None"):
        if typ == "None":
            return(list(map(lambda x: x[2], aso_info)))
        else:
            return(list(map(lambda x: x[1], aso_info)))
def extract_repr_info_kom(aso_info):
        aso_instance = []
        aso_info_sorted = sorted(aso_info, key = lambda y: y[0])
        available_keys = list(map(lambda x: x[0], aso_info_sorted))
        all_keys = [str(i) for i in range(1, 5)]
        aso_info_sorted = list(map(lambda x: x[1], aso_info_sorted))
        aso_info_sorted.reverse()
        for item in all_keys:
                if item in set(all_keys) - set(available_keys):
                        aso_instance.append('None')
                else:
                        aso_instance.append(aso_info_sorted.pop())
        return(aso_instance)
def aso_update(lobject1, lobject2, typ='None', lobject3='None'):
        proxy_set = set()
        if typ == 'None':
                aso_set = set(list(map(lambda z: z[2], list(map(lambda y: extract_aso_info_zoo(y), lobject2)))))                
        elif typ == 'Spol':
                aso_set = set(list(map(lambda z: z[2], list(map(lambda y: extract_aso_info_zoo(y), lobject2))))) 
                proxy_set = set(extract_aso_info_akc(lobject3, 'Spol')) 
        else:
                aso_set = set(extract_aso_info_akc(lobject2))
        repr_set = set(list(map(lambda z: z[2], list(map(lambda x: extract_repr_info_zoo(x), lobject1)))))
        if typ == 'Spol':
             if repr_set.issubset(proxy_set) or proxy_set.issubset(repr_set):
                return(len(proxy_set | repr_set))
             else:
                return(len(proxy_set ^ repr_set))
        else:    
            if repr_set.issubset(aso_set) or aso_set.issubset(repr_set):
                return(len(aso_set | repr_set))
            else:
                return(len(aso_set ^ repr_set))
        
class SpJawna(EcoEntity):
        def write_csv(self, dirname):
                csv_entity_headers = self.csv_headers + ['TYP', 'REGON/NIP', 'INNA_DZ_USC', 'POZ_PUB', 'KRAJ_S', 'WOJ_S', 'POW_S', 'GMINA_S', 'MIEJSC_S', 'UL_A', 'NR_A', 'LOK_A', 'MIEJSC_A', 'KOD_A', 'POCZTA_A', 'KRAJ_A'] + \
                                ['LICZ_ODDZ', 'CZAS_TRWANIA', 'KOD_DZ', 'LICZB_SKOJ_POD']
                csv_source_headers = ['KRS', 'POWST', 'ZR_POWST', 'REJ', 'ZR_KRS', 'REGON/NIP']
                csv_aso_entity_headers = ['KRS', 'NAZW', 'IMIONA', 'PESEL/REG', 'TYP', 'TYP_PROK', 'ENT_KRS', 'ZWIAZ_MAL', 'UMOW_MAL', 'ROZDZ_MAJ', 'ZDOLN_CZ_PRAW', 'REPR']
                header_info = get_header_info(self)
                entity_info, source_info, aso_info = get_body_info(self)
                pathfile = dirname + '/SPJaw'
                if not os.path.isfile(pathfile+'_entity.csv'):
                        with open(pathfile+'_entity.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_entity_headers)
                else:
                        pass
                if not os.path.isfile(pathfile+'_aso.csv'):
                        with open(pathfile+'_aso.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_aso_entity_headers)
                else:
                        pass
                if not os.path.isfile(pathfile + '_source.csv'):
                        with open(pathfile + '_source.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_source_headers)
                else:
                        pass
                with open(pathfile + '_entity.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(entity_info):
                                wr.writerow(header_info+entity_info)
                        else:
                                pass
                with open(pathfile + '_aso.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(aso_info):
                                for aso in aso_info:
                                        wr.writerow([header_info[2]] + extract_aso_info(aso))
                        else:
                            pass            
                with open(pathfile + '_source.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(source_info):
                                typ = source_info[0]
                                for source in source_info[1:]:
                                        wr.writerow([header_info[2]] + [typ] + source)
                        else:
                                pass
class SpZoo(EcoEntity):
        def write_csv(self, dirname):
                csv_entity_headers = self.csv_headers + ['TYP', 'REGON/NIP', 'INNA_DZ_USC', 'POZ_PUB', 'KRAJ_S', 'WOJ_S', 'POW_S', 'GMINA_S', 'MIEJSC_S', 'UL_A', 'NR_A', 'LOK_A', 'MIEJSC_A', 'KOD_A', 'POCZTA_A', 'KRAJ_A'] + \
                                ['LICZ_ODDZ', 'CZAS_TRWANIA', 'KOD_DZ', 'KAPITAL', 'LICZB_SKOJ_POD']
                csv_source_headers = ['KRS', 'POWST', 'ZR_POWST', 'REJ', 'ZR_KRS', 'REGON/NIP']
                csv_aso_entity_headers = ['KRS', 'NAZW', 'IMIONA', 'PESEL/REG', 'ENT_KRS', 'UDZIAL', 'CALE_UDZIAL']
                csv_repr_headers = ['KRS', 'NAZW', 'IMIONA', 'PESEL/REG', 'ENT_KRS', 'FUNK', 'ZAW', 'DATA_ZAW']
                pathfile = dirname +'/SPZOO'
 
                header_info = get_header_info(self)
                entity_info, source_info, aso_info, repr_info = get_body_info(self)
                if not os.path.isfile(pathfile+'_entity.csv'):
                        with open(pathfile+'_entity.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_entity_headers)
                else:
                        pass
                if not os.path.isfile(pathfile+'_aso.csv'):
                        with open(pathfile+'_aso.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_aso_entity_headers)
                else:
                        pass
                if not os.path.isfile(pathfile + '_source.csv'):
                        with open(pathfile + '_source.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_source_headers)
                else:
                        pass
                if not os.path.isfile(pathfile + '_repr.csv'):
                        with open(pathfile + '_repr.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_repr_headers)
                else:
                        pass
                with open(pathfile+'_entity.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(entity_info):
                                wr.writerow(header_info+entity_info)
                        else:
                                pass
                with open(pathfile+'_aso.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(aso_info):
                                for aso in aso_info:
                                        wr.writerow([header_info[2]] + extract_aso_info_zoo(aso))
                        else:
                                pass
                with open(pathfile+'_repr.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(repr_info):
                                for rep in repr_info:
                                        wr.writerow([header_info[2]] + extract_aso_info_zoo(rep))
                        else:
                                pass
                with open(pathfile+'_entity.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(source_info):
                                typ = source_info[0]
                                for source in source_info[1:]:
                                        wr.writerow([header_info[2]] + [typ] + source)
                        else:
                                pass
class SpKom(EcoEntity):
        def write_csv(self, dirname):
                csv_entity_headers = self.csv_headers + ['TYP', 'REGON/NIP', 'INNA_DZ_USC', 'POZ_PUB', 'KRAJ_S', 'WOJ_S', 'POW_S', 'GMINA_S', 'MIEJSC_S', 'UL_A', 'NR_A', 'LOK_A', 'MIEJSC_A', 'KOD_A', 'POCZTA_A', 'KRAJ_A'] + \
                                ['LICZB_ODDZ', 'CZAS_TRWANIA', 'KOD_DZ',  'LICZB_SKOJ_POD']
                csv_source_headers = ['KRS', 'POWST', 'ZR_POWST', 'REJ', 'ZR_KRS', 'REGON/NIP']
                csv_aso_entity_headers = ['KRS', 'NAZW', 'IMIONA', 'PESEL/REG', 'ENT_KRS', 'ZWIAZ_MAL', 'UMOW_MAL', 'ROZDZ_MAJ', 'ZDOLN_CZ_PRAW', 'KOMAND', 'SUM_KOMAND', 'WKLAD', 'WKLAD_NPIEN',  'REPR']
               # csv_aso_entity_headers = ['KRS', 'NAZW', 'IMIONA', 'PESEL/REG', 'ENT_KRS', 'UDZIAL', 'CALE_UDZIAL']
                csv_repr_headers = ['KRS', 'NAZW', 'IMIONA', 'PESEL/REG', 'ENT_KRS']

                header_info = get_header_info(self)
                entity_info, source_info, aso_info, repr_info = get_body_info(self)
                pathfile = dirname + '/SPKOM'
                if not os.path.isfile(pathfile+'_entity.csv'):
                        with open(pathfile+'_entity.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_entity_headers)
                else:
                        pass
                if not os.path.isfile(pathfile+'_aso.csv'):
                        with open(pathfile+'_aso.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_aso_entity_headers)
                else:
                        pass
                if not os.path.isfile(pathfile + '_source.csv'):
                        with open(pathfile + '_source.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_source_headers)
                else:
                        pass
                if not os.path.isfile(pathfile + '_repr.csv'):
                        with open(pathfile + '_repr.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_repr_headers)
                else:
                        pass        
                with open(pathfile + '_entity.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(entity_info):
                                wr.writerow(header_info+entity_info)
                        else:
                                pass
                with open(pathfile + '_aso.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(aso_info):
                                for aso in aso_info:
                                        wr.writerow([header_info[2]] + extract_aso_info_kom(aso))
                        else:
                                pass
                with open(pathfile + '_repr.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(repr_info):
                                for rep in repr_info:
                                        wr.writerow([header_info[2]] + extract_repr_info_kom(rep))
                        else:
                                pass
                with open(pathfile + '_source.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(source_info):
                                typ = source_info[0]
                                for source in source_info[1:]:
                                        wr.writerow([header_info[2]] + [typ] + source)
                        else:
                                pass
class SpAkc(EcoEntity):
        def write_csv(self, dirname):
                csv_entity_headers = self.csv_headers + ['TYP', 'REGON/NIP', 'INNA_DZ_USC', 'POZ_PUB', 'KRAJ_S', 'WOJ_S', 'POW_S', 'GMINA_S', 'MIEJSC_S', 'UL_A', 'NR_A', 'LOK_A', 'MIEJSC_A', 'KOD_A', 'POCZTA_A', 'KRAJ_A'] + \
                                ['LICZ_ODDZ', 'CZAS_TRWANIA', 'KOD_DZ', 'KAPITAL_ZAK', 'KAPITAL_DOC', 'ALL_AKC', 'NOM_AKC', 'KAPITAL_WP', 'WAR_KAP_Z', 'KOD_AKC', 'SER_AKC',  'LICZB_SKOJ_POD']
                csv_action_headers = ['KRS', 'KOD_A', 'LICZB_AKC', 'RODZ_AKC']
                csv_source_headers = ['KRS', 'POWST', 'ZR_POWST', 'REJ', 'ZR_KRS', 'REGON/NIP']
                csv_aso_entity_headers = ['KRS', 'NAZW', 'IMIONA', 'PESEL/REG']
                csv_repr_headers = ['KRS', 'NAZW', 'IMIONA', 'PESEL/REG', 'ENT_KRS', 'FUNK', 'ZAW', 'DATA_ZAW']
                header_info = get_header_info(self)
                entity_info, source_info, aso_info, repr_info, action_info = get_body_info(self)
                pathfile = dirname + '/SPAKC'
                if not os.path.isfile(pathfile+'_entity.csv'):
                        with open(pathfile+'_entity.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_entity_headers)
                else:
                        pass
                if not os.path.isfile(pathfile+'_aso.csv'):
                        with open(pathfile+'_aso.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_aso_entity_headers)
                else:
                        pass
                if not os.path.isfile(pathfile + '_source.csv'):
                        with open(pathfile + '_source.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_source_headers)
                else:
                        pass
                if not os.path.isfile(pathfile + '_repr.csv'):
                        with open(pathfile + '_repr.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_repr_headers)
                else:
                        pass
                if not os.path.isfile(pathfile + '_action.csv'):
                        with open(pathfile + '_repr.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_repr_headers)
                else:
                        pass
                with open(pathfile + '_entity.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(entity_info):
                                wr.writerow(header_info+entity_info)
                        else:
                                pass
                
                with open(pathfile + '_aso.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(aso_info):
                                for aso in aso_info:
                                        wr.writerow([header_info[2]] + aso)
                        else:
                                pass
                with open(pathfile + '_repr.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(repr_info):
                                for rep in repr_info:
                                        wr.writerow([header_info[2]] + extract_aso_info_zoo(rep))
                        else:
                                pass
                with open(pathfile + '_source.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(source_info):
                                typ = source_info[0]
                                for source in source_info[1:]:
                                        wr.writerow([header_info[2]] + [typ] + source)
                        else:
                                pass
                with open(pathfile + '_action.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(action_info):
                                for source in action_info:
                                        wr.writerow([header_info[2]] + source)
                        else:
                                pass
class SpKomAkc(EcoEntity):
        def write_csv(self, dirname):
                csv_entity_headers = self.csv_headers + ['TYP', 'REGON/NIP', 'INNA_DZ_USC', 'POZ_PUB', 'KRAJ_S', 'WOJ_S', 'POW_S', 'GMINA_S', 'MIEJSC_S', 'UL_A', 'NR_A', 'LOK_A', 'MIEJSC_A', 'KOD_A', 'POCZTA_A', 'KRAJ_A'] + \
                                ['LICZ_ODDZ', 'CZAS_TRWANIA', 'KOD_DZ', 'KAPITAL_ZAK', 'KAPITAL_DOC', 'ALL_AKC', 'NOM_AKC', 'KOD_AKC', 'SER_AKC',  'LICZB_SKOJ_POD']
                csv_source_headers = ['KRS', 'POWST', 'ZR_POWST', 'REJ', 'ZR_KRS', 'REGON/NIP']
                csv_aso_entity_headers = ['KRS', 'NAZW', 'IMIONA', 'PESEL/REG', 'ENT_KRS', 'ZWIAZ_MAL', 'UMOW_MAL', 'ROZDZ_MAJ', 'ZDOLN_CZ_PRAW', 'REPR']
                csv_repr_headers = ['KRS', 'NAZW', 'IMIONA', 'PESEL/REG', 'ENT_KRS', 'FUNK', 'ZAW', 'DATA_ZAW']
                csv_action_headers = ['KRS', 'KOD_A', 'LICZB_AKC', 'RODZ_AKC']

                header_info = get_header_info(self)
                entity_info, source_info, aso_info, repr_info, action_info = get_body_info(self)
                pathfile = dirname + '/SPKAKC'
                if not os.path.isfile(pathfile+'_entity.csv'):
                        with open(pathfile+'_entity.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_entity_headers)
                else:
                        pass
                if not os.path.isfile(pathfile+'_aso.csv'):
                        with open(pathfile+'_aso.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_aso_entity_headers)
                else:
                        pass
                if not os.path.isfile(pathfile + '_source.csv'):
                        with open(pathfile + '_source.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_source_headers)
                else:
                        pass
                if not os.path.isfile(pathfile + '_repr.csv'):
                        with open(pathfile + '_repr.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_repr_headers)
                else:
                        pass
                if not os.path.isfile(pathfile + '_action.csv'):
                        with open(pathfile + '_repr.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_repr_headers)
                else:
                        pass
                with open(pathfile + "_entity.csv", 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(entity_info):
                                wr.writerow(header_info+entity_info)
                        else:
                                pass
                with open(pathfile + "_aso.csv", 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(aso_info):
                                for aso in aso_info:
                                        wr.writerow([header_info[2]] + extract_aso_info_kom(aso))
                        else:
                                pass
                with open(pathfile + '_repr.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(repr_info):
                                for rep in repr_info:
                                        wr.writerow([header_info[2]] + extract_repr_info_kom(rep))
                        else:
                                pass
                with open(pathfile + '_source.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(source_info):
                                typ = source_info[0]
                                for source in source_info[1:]:
                                        wr.writerow([header_info[2]] + [typ] + source)
                        else:
				pass
                with open(pathfile + '_action.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(action_info):
                                for source in action_info:
                                        wr.writerow([header_info[2]] + source)
                        else:
                                pass	
class Spol(EcoEntity):
        def write_csv(self, dirname):
                csv_entity_headers = self.csv_headers + ['TYP', 'REGON/NIP', 'INNA_DZ_USC', 'POZ_PUB', 'KRAJ_S', 'WOJ_S', 'POW_S', 'GMINA_S', 'MIEJSC_S', 'UL_A', 'NR_A', 'LOK_A', 'MIEJSC_A', 'KOD_A', 'POCZTA_A', 'KRAJ_A'] + \
                                ['LICZ_ODDZ', 'CZAS_TRWANIA', 'KOD_DZ', 'LICZB_SKOJ_POD']
                csv_source_headers = ['KRS', 'POWST', 'ZR_POWST', 'REJ', 'ZR_KRS', 'REGON/NIP']
                csv_aso_entity_headers = ['KRS', 'NAZW', 'IMIONA', 'PESEL/REG', 'ENT_KRS', 'UDZIAL', 'CALE_UDZIAL']
                csv_repr_headers = ['KRS', 'NAZW', 'IMIONA', 'PESEL/REG', 'ENT_KRS', 'FUNK', 'ZAW', 'DATA_ZAW']
                csv_proxy_headers = ['KRS', 'NAZW', 'IMIONA', 'PESEL', 'ZAKR']
                header_info = get_header_info(self)
                entity_info, source_info, aso_info, repr_info, proxy_info = get_body_info(self)
                pathfile = dirname + '/SPOL'
                if not os.path.isfile(pathfile+'_entity.csv'):
                        with open(pathfile+'_entity.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_entity_headers)
                else:
                        pass
                if not os.path.isfile(pathfile+'_aso.csv'):
                        with open(pathfile+'_aso.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_aso_entity_headers)
                else:
                        pass
                if not os.path.isfile(pathfile + '_source.csv'):
                        with open(pathfile + '_source.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_source_headers)
                else:
                        pass
                if not os.path.isfile(pathfile + '_repr.csv'):
                        with open(pathfile + '_repr.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_repr_headers)
                else:
                        pass
                if not os.path.isfile(pathfile + '_proxy.csv'):
                        with open(pathfile + '_proxy.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_proxy_headers)
                else:
                        pass
                with open(pathfile + '_entity.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(entity_info):
                                wr.writerow(header_info+entity_info)
                        else:
                                pass
                with open(pathfile + '_aso.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(aso_info):
                                for aso in aso_info:
                                        wr.writerow([header_info[2]] + extract_aso_info_zoo(aso))
                        else:
                                pass
                with open(pathfile + '_repr.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(repr_info):
                                for rep in repr_info:
                                        wr.writerow([header_info[2]] + extract_aso_info_zoo(rep))
                        else:
                                pass
                with open(pathfile + '_source.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(source_info):
                                typ = source_info[0]
                                for source in source_info[1:]:
                                        wr.writerow([header_info[2]] + [typ] + source)
                        else:
                                pass
                with open(pathfile + '_proxy.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(proxy_info):
                                for rep in proxy_info:
                                        wr.writerow([header_info[2]] + rep)
                        else:
                                pass
class Fund(EcoEntity):
        def write_csv(self, dirname):
                csv_entity_headers = self.csv_headers + ['TYP', 'REGON/NIP', 'POZ_PUB', 'KRAJ_S', 'WOJ_S', 'POW_S', 'GMINA_S', 'MIEJSC_S', 'UL_A', 'NR_A', 'LOK_A', 'MIEJSC_A', 'KOD_A', 'POCZTA_A', 'KRAJ_A'] + \
                                ['LICZ_ODDZ', 'CZAS_TRWANIA', 'LICZB_SKOJ_POD']
                csv_source_headers = ['KRS', 'POWST', 'ZR_POWST', 'REJ', 'ZR_KRS', 'REGON/NIP']
                csv_aso_entity_headers = ['KRS', 'NAZW', 'IMIONA', 'PESEL/REG', 'ENT_KRS', 'ORGAN']
                csv_repr_headers = ['KRS', 'NAZW', 'IMIONA', 'PESEL/REG', 'ENT_KRS', 'FUNK']
                
                header_info = get_header_info(self)
                entity_info, source_info, aso_info, repr_info = get_body_info(self)
                pathfile = dirname + '/FUND'
                if not os.path.isfile(pathfile+'_entity.csv'):
                        with open(pathfile+'_entity.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_entity_headers)
                else:
                        pass
                if not os.path.isfile(pathfile+'_aso.csv'):
                        with open(pathfile+'_aso.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_aso_entity_headers)
                else:
                        pass
                if not os.path.isfile(pathfile + '_source.csv'):
                        with open(pathfile + '_source.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_source_headers)
                else:
                        pass
                if not os.path.isfile(pathfile + '_repr.csv'):
                        with open(pathfile + '_repr.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_repr_headers)
                else:
                        pass        
                with open(pathfile + '_entity.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(entity_info):
                                wr.writerow(header_info+entity_info)
                        else:
                                pass
                with open(pathfile + '_aso.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(aso_info):
                                for aso in aso_info:
                                        wr.writerow([header_info[2]] + aso)
                        else:
                                pass
                with open(pathfile + '_repr.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(repr_info):
                                for rep in repr_info:
                                        wr.writerow([header_info[2]] + extract_aso_info_zoo(rep))
                        else:
                                pass
                with open(pathfile + '_source.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(source_info):
                                typ = source_info[0]
                                for source in source_info[1:]:
                                        wr.writerow([header_info[2]] + [typ] + source)
                        else:
                                pass
class Zagr(EcoEntity):
        def write_csv(self, dirname):
                csv_entity_headers = self.csv_headers + ['TYP', 'REGON/NIP','NAWZWA_ZAG', 'REJ_ZAG', 'PRAWA', 'INNA_DZ_USC', 'POZ_PUB', 'KRAJ_S', 'WOJ_S', 'POW_S', 'GMINA_S', 'MIEJSC_S', 'UL_A', 'NR_A', 'LOK_A', 'MIEJSC_A', 'KOD_A', 'POCZTA_A', 'KRAJ_A', 'KRAJ_ZAG', 'WOJ_ZAG', 'MIEJSC_ZAG', 'NR_ZAG', 'KOD_ZAG', 'POCZTA_ZAG', 'UL_ZAG'] + \
                                ['LICZ_ODDZ', 'CZAS_TRWANIA', 'KOD_DZ', 'KAPITAL', 'LICZB_SKOJ_POD']
                csv_source_headers = ['KRS', 'POWST', 'ZR_POWST', 'REJ', 'ZR_KRS', 'REGON/NIP']
                csv_aso_entity_headers = ['KRS', 'NAZW', 'IMIONA', 'PESEL/REG']
                csv_repr_headers = ['KRS', 'NAZW', 'IMIONA', 'PESEL/REG', 'ENT_KRS', 'FUNK']
                
                header_info = get_header_info(self)
                entity_info, source_info, aso_info, repr_info = get_body_info(self)
                pathfile = dirname + '/ZAGR'
                if not os.path.isfile(pathfile+'_entity.csv'):
                        with open(pathfile+'_entity.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_entity_headers)
                else:
                        pass
                if not os.path.isfile(pathfile+'_aso.csv'):
                        with open(pathfile+'_aso.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_aso_entity_headers)
                else:
                        pass
                if not os.path.isfile(pathfile + '_source.csv'):
                        with open(pathfile + '_source.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_source_headers)
                else:
                        pass
                if not os.path.isfile(pathfile + '_repr.csv'):
                        with open(pathfile + '_repr.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_repr_headers)
                else:
                        pass        
                with open(pathfile + '_entity.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(entity_info):
                                wr.writerow(header_info+entity_info)
                        else:
                                pass
                with open(pathfile + '_aso.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(aso_info):
                                for aso in aso_info:
                                        wr.writerow([header_info[2]] + aso)
                        else:
                                pass
                with open(pathfile + '_repr.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(repr_info):
                                for rep in repr_info:
                                        wr.writerow([header_info[2]] + extract_aso_info_zoo(rep))
                        else:
                                pass
                with open(pathfile + '_source.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(source_info):
                                typ = source_info[0]
                                for source in source_info[1:]:
                                        wr.writerow([header_info[2]] + [typ] + source)
                        else:
                                pass
class Stow(EcoEntity):
        def write_csv(self, dirname):
                csv_entity_headers = self.csv_headers + ['TYP', 'REGON/NIP', 'INNA_DZ_USC', 'POZ_PUB', 'KRAJ_S', 'WOJ_S', 'POW_S', 'GMINA_S', 'MIEJSC_S', 'UL_A', 'NR_A', 'LOK_A', 'MIEJSC_A', 'KOD_A', 'POCZTA_A', 'KRAJ_A'] + \
                                ['LICZ_ODDZ', 'CZAS_TRWANIA', 'KOD_DZ', 'LICZB_SKOJ_POD']
                csv_source_headers = ['KRS', 'POWST', 'ZR_POWST', 'REJ', 'ZR_KRS', 'REGON/NIP']
                csv_aso_entity_headers = ['KRS', 'NAZW', 'IMIONA', 'PESEL/REG', 'ENT_KRS', 'FUNK']
                csv_repr_headers = ['KRS', 'NAZW', 'IMIONA', 'PESEL/REG', 'ENT_KRS', 'FUNK']

                header_info = get_header_info(self)
                entity_info, source_info, aso_info, repr_info = get_body_info(self)
                pathfile = dirname + '/STOW'
                if not os.path.isfile(pathfile+'_entity.csv'):
                        with open(pathfile+'_entity.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_entity_headers)
                else:
                        pass
                if not os.path.isfile(pathfile+'_aso.csv'):
                        with open(pathfile+'_aso.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_aso_entity_headers)
                else:
                        pass
                if not os.path.isfile(pathfile + '_source.csv'):
                        with open(pathfile + '_source.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_source_headers)
                else:
                        pass
                if not os.path.isfile(pathfile + '_repr.csv'):
                        with open(pathfile + '_repr.csv', 'w+') as f:
                                wr = csv.writer(f, delimiter = ';')
                                wr.writerow(csv_repr_headers)
                else:
                        pass        
                with open(pathfile + '_entity.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(entity_info):
                                wr.writerow(header_info+entity_info)
                        else:
                                pass
                with open(pathfile + '_aso.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(aso_info):
                                for aso in aso_info:
                                        wr.writerow([header_info[2]] + aso)
                        else:
                                pass
                with open(pathfile + '_repr.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(repr_info):
                                for rep in repr_info:
                                        wr.writerow([header_info[2]] + extract_repr_info_kom(rep))
                        else:
                                pass
                with open(pathfile + '_source.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(source_info):
                                typ = source_info[0]
                                for source in source_info[1:]:
                                        wr.writerow([header_info[2]] + [typ] + source)
                        else:
                                pass
class Inst(EcoEntity):
        def write_csv(self):
                csv_entity_headers = self.csv_headers + ['TYP', 'REGON/NIP', 'INNA_DZ_USC', 'POZ_PUB', 'KRAJ_S', 'WOJ_S', 'POW_S', 'GMINA_S', 'MIEJSC_S', 'UL_A', 'NR_A', 'LOK_A', 'MIEJSC_A', 'KOD_A', 'POCZTA_A', 'KRAJ_A'] + \
                                ['LICZ_ODDZ', 'CZAS_TRWANIA', 'KOD_DZ', 'KAPITAL', 'LICZB_SKOJ_POD']
                csv_source_headers = ['KRS', 'POWST', 'ZR_POWST', 'REJ', 'ZR_KRS', 'REGON/NIP']
                csv_aso_entity_headers = ['KRS', 'NAZW', 'IMIONA', 'PESEL/REG', 'ENT_KRS', 'UDZIAL', 'CALE_UDZIAL']
                csv_repr_headers = ['KRS', 'NAZW', 'IMIONA', 'PESEL/REG', 'ENT_KRS', 'FUNK', 'ZAW', 'DATA_ZAW']

                header_info = get_header_info(self)
                entity_info, source_info, aso_info, repr_info = get_body_info(self)
                with open('/home/ewarchul/MFParser2/Inst_entity.csv', 'w+') as f:
                        wr = csv.writer(f, delimiter = ';')
                        wr.writerow(csv_entity_headers)
                with open('/home/ewarchul/MFParser2/Inst_aso_entity.csv', 'w+') as f:
                        wr = csv.writer(f, delimiter = ';')
                        wr.writerow(csv_aso_entity_headers)
                with open('/home/ewarchul/MFParser2/Inst_source_entity.csv', 'w+') as f:
                        wr = csv.writer(f, delimiter = ';')
                        wr.writerow(csv_source_headers)
                with open('/home/ewarchul/MFParser2/Inst_repr_entity.csv', 'w+') as f:
                        wr = csv.writer(f, delimiter = ';')
                        wr.writerow(csv_repr_headers)
                with open('/home/ewarchul/MFParser2/Inst_entity.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(entity_info):
                                wr.writerow(header_info+entity_info)
                        else:
                                pass
                with open('/home/ewarchul/MFParser2/Inst_aso_entity.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(aso_info):
                                for aso in aso_info:
                                        wr.writerow([header_info[2]] + extract_aso_info_zoo(aso))
                        else:
                                pass
                with open('/home/ewarchul/MFParser2/Inst_repr_entity.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(repr_info):
                                for rep in repr_info:
                                        wr.writerow([header_info[2]] + extract_aso_info_zoo(rep))
                        else:
                                pass
                with open('/home/ewarchul/MFParser2/Inst_source_entity.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(source_info):
                                typ = source_info[0]
                                for source in source_info[1:]:
                                        wr.writerow([header_info[2]] + [typ] + source)
                        else:
                                pass
class Krol(EcoEntity):
        def write_csv(self):
                csv_entity_headers = self.csv_headers + ['TYP', 'REGON/NIP', 'INNA_DZ_USC', 'POZ_PUB', 'KRAJ_S', 'WOJ_S', 'POW_S', 'GMINA_S', 'MIEJSC_S', 'UL_A', 'NR_A', 'LOK_A', 'MIEJSC_A', 'KOD_A', 'POCZTA_A', 'KRAJ_A'] + \
                                ['LICZ_ODDZ', 'CZAS_TRWANIA', 'KOD_DZ', 'KAPITAL', 'LICZB_SKOJ_POD']
                csv_source_headers = ['KRS', 'POWST', 'ZR_POWST', 'REJ', 'ZR_KRS', 'REGON/NIP']
                csv_aso_entity_headers = ['KRS', 'NAZW', 'IMIONA', 'PESEL/REG', 'ENT_KRS', 'UDZIAL', 'CALE_UDZIAL']
                csv_repr_headers = ['KRS', 'NAZW', 'IMIONA', 'PESEL/REG', 'ENT_KRS', 'FUNK', 'ZAW', 'DATA_ZAW']

                header_info = get_header_info(self)
                entity_info, source_info, aso_info, repr_info = get_body_info(self)
                with open('/home/ewarchul/MFParser2/SPZOO_entity.csv', 'w+') as f:
                        wr = csv.writer(f, delimiter = ';')
                        wr.writerow(csv_entity_headers)
                with open('/home/ewarchul/MFParser2/SPZOO_aso_entity.csv', 'w+') as f:
                        wr = csv.writer(f, delimiter = ';')
                        wr.writerow(csv_aso_entity_headers)
                with open('/home/ewarchul/MFParser2/SPZOO_source_entity.csv', 'w+') as f:
                        wr = csv.writer(f, delimiter = ';')
                        wr.writerow(csv_source_headers)
                with open('/home/ewarchul/MFParser2/SPZOO_repr_entity.csv', 'w+') as f:
                        wr = csv.writer(f, delimiter = ';')
                        wr.writerow(csv_repr_headers)
                with open('/home/ewarchul/MFParser2/SPZOO_entity.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(entity_info):
                                wr.writerow(header_info+entity_info)
                        else:
                                pass
                with open('/home/ewarchul/MFParser2/SPZOO_aso_entity.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(aso_info):
                                for aso in aso_info:
                                        wr.writerow([header_info[2]] + extract_aso_info_zoo(aso))
                        else:
                                pass
                with open('/home/ewarchul/MFParser2/SPZOO_repr_entity.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(repr_info):
                                for rep in repr_info:
                                        wr.writerow([header_info[2]] + extract_aso_info_zoo(rep))
                        else:
                                pass
                with open('/home/ewarchul/MFParser2/SPZOO_source_entity.csv', 'a') as f:
                        wr = csv.writer(f, delimiter = ';')
                        if len(source_info):
                                typ = source_info[0]
                                for source in source_info[1:]:
                                        wr.writerow([header_info[2]] + [typ] + source)
                        else:
                                pass

pierwsze_ = pickle.load(open('/home/ewarchul/MFParser2/mon.p'))
frame_e1 = [['176055', 'BELWEDER D. PACZUSKI SPOLKA JAWNA', '0000582602', '27.10.2015'], ['1', [['1', 'Dane podmiotu'], ['1', 'SPOLKA JAWNA'], ['2', 'REGON 142503917 NIP 5272633897'], ['3', 'BELWEDER D. PACZUSKI SPOLKA JAWNA'], ['5', 'NIE'], ['6', 'NIE']], [['2', 'Siedziba i adres podmiotu'], ['1', ['kraj', 'POLSKA'], ['wojewodztwo', 'MAZOWIECKIE'], ['powiat', 'WARSZAWA'], ['gmina', 'WARSZAWA'], ['miejscowosc', 'WARSZAWA']], ['2', ['miejscowosc', 'WARSZAWA'], ['ulica', 'TRAKT BRZESKI'], ['nr domu', '57'], ['kod pocztowy', '05-077'], ['poczta', 'WARSZAWA'], ['kraj', 'POLSKA']]], [['3', 'Oddzialy'], ['1', ['1', 'BELWEDER D. PACZUSKI SPOLKA JAWNA ODDZIAL W SULEJOWKU'], ['2', ['kraj', 'POLSKA'], ['wojewodztwo', 'MAZOWIECKIE'], ['powiat', 'MINSKI'], ['gmina', 'SULEJOWEK'], ['miejscowosc', 'SULEJOWEK']], ['3', ['miejscowosc', 'SULEJOWEK'], ['ulica', 'UL. DWORCOWA'], ['nr domu', '90'], ['kod pocztowy', '05-070'], ['poczta', 'SULEJOWEK'], ['kraj', 'POLSKA']]]], [['4', 'Informacje o umowie'], ['1', '06.10.2015 R., NOTARIUSZ RADOSLAW WALASIK, KANCELARIA NOTARIALNA W WARSZAWIE, REP. A NR 6523/2015']], [['5', 'None'], ['1', 'CZAS NIEOZNACZONY']], [['6', 'Sposob powstania spolki'], ['1', 'PRZEKSZTALCENIE'], ['2', 'PRZEKSZTALCENIE SPOLKI POD FIRMA BIURO OBROTU NIERUCHOMOSCIAMI BELWEDER SPOLKA Z OGRANICZONA ODPOWIEDZIALNOSCIA W SPOLKE JAWNA POD FIRMA BELWEDER D. PACZUSKI SPOLKA JAWNA W TRYBIE ART. 551 PAR 1 KODEKSU SPOLEK HANDLOWYCH UCHWALA O PRZEKSZTALCENIU PODJETA W DNIU 6.10.2015 R. PRZEZ NADZWYCZAJNE ZGROMADZENIE WSPOLNIKOW BIURO OBROTU NIERUCHOMOSCIAMI BELWEDER SPOLKA Z OGRANICZONA ODPOWIEDZIALNOSCIA PRZED NOTARIUSZEM RADOSLAWEM WALASIKIEM W KANCELARII NOTARIALNEJ W WARSZAWIE PRZY UL. BONIFRATERSKIEJ 8 LOK. 99, ZA REP. A NR 6523/2015'], ['PRub.', ['1', ['1', 'BIURO OBROTU NIERUCHOMOSCIAMI BELWEDER SPOLKA Z OGRANICZONA ODPOWIEDZIALNOSCIA'], ['2', 'REJESTR KRS'], ['3', '0000361090'], ['5', '142503917 -- 5272633897']]]], [['7', 'Dane wspolnikow'], ['1', ['1', 'PACZUSKI'], ['2', 'DARIUSZ MICHAL'], ['3', '72052407715'], ['5', 'TAK'], ['6', 'NIE'], ['7', 'NIE'], ['8', 'NIE']], ['2', ['1', 'PACZUSKA'], ['2', 'JOANNA'], ['3', '71111201022'], ['5', 'TAK'], ['6', 'NIE'], ['7', 'NIE'], ['8', 'NIE']]]], ['2', [['1', 'Uprawnieni do reprezentowania spolki'], ['1', ['1', 'WSPOLNICY REPREZENTUJACY SPOLKE'], ['2', 'DO REPREZENTOWANIA SPOLKI UPOWAZNIONY JEST WSPOLNIK DARIUSZ PACZUSKI JEDNOOSOBOWO']], ['PRub.', ['1', ['1', 'PACZUSKI'], ['2', 'DARIUSZ MICHAL'], ['3', '72052407715']]]]], ['3', [['1', 'Przedmiot dzialalnosci'], ['1', ['1', ['68', '31', 'Z'], 'POSREDNICTWO W OBROCIE NIERUCHOMOSCIAMI'], ['--', ['68'], 'DZIAŁALNOSC ZWIAZANA Z OBSŁUGA RYNKU NIERUCHOMOSCI'], ['--', ['64', '92', 'Z'], 'POZOSTALE FORMY UDZIELANIA KREDYTOW'], ['--', ['74', '10', 'Z'], 'DZIALALNOSC W ZAKRESIE SPECJALISTYCZNEGO PROJEKTOWANIA'], ['--', ['82', '99', 'Z'], 'POZOSTALA DZIALALNOSC WSPOMAGAJACA PROWADZENIE DZIAŁALNOSCI GOSPODARCZEJ, GDZIE INDZIEJ NIESKLASYFIKOWANA'], ['--', ['41'], 'ROBOTY BUDOWLANE ZWIAZANE ZE WZNOSZENIEM BUDYNKOW'], ['--', ['45'], 'HANDEL HURTOWY I DETALICZNY POJAZDAMI SAMOCHODOWYMI; NAPRAWA POJAZDOW SAMOCHODOWYCH'], ['--', ['46'], 'HANDEL HURTOWY, Z WYLACZENIEM HANDLU POJAZDAMI SAMOCHODOWYMI'], ['--', ['47'], 'HANDEL DETALICZNY, Z WYLACZENIEM HANDLU DETALICZNEGO POJAZDAMI SAMOCHODOWYMI'], ['--', ['49', '4'], 'TRANSPORT DROGOWY TOWAROW ORAZ DZIALALNOSC USLUGOWA ZWIAZANA Z PRZEPROWADZKAMI']]]]]
frame_e2 = [['446930', 'RYSY ARCHITEKCI SPOLKA Z OGRANICZONA ODPOWIEDZIALNOSCIA', '0000705953', '01.12.2017'], ['1', [['1', 'Dane podmiotu'], ['1', 'SPOLKA Z OGRANICZONA ODPOWIEDZIALNOSCIA'], ['3', 'RYSY ARCHITEKCI SPOLKA Z OGRANICZONA ODPOWIEDZIALNOSCIA'], ['5', 'NIE'], ['6', 'NIE']], [['2', 'Siedziba i adres podmiotu'], ['1', ['kraj', 'POLSKA'], ['wojewodztwo', 'MAZOWIECKIE'], ['powiat', 'PIASECZYNSKI'], ['gmina', 'LESZNOWOLA'], ['miejscowosc', 'MYSIADLO']], ['2', ['miejscowosc', 'MYSIADLO'], ['ulica', 'UL. TOPOLOWA'], ['nr domu', '2'], ['nr lokalu', '91'], ['kod pocztowy', '05-500'], ['poczta', 'MYSIADLO'], ['kraj', 'POLSKA']], ['3', ['Adres poczty elektronicznej', 'RS@RYSYARCHITEKCI.PL']], ['4', ['Adres strony internetowej', 'WWW.RYSYARCHITEKCI.PL']]], [['4', 'Informacje o umowie'], ['1', '23.11.2017 R.']], [['5', 'None'], ['1', 'CZAS NIEOZNACZONY'], ['3', 'WIEKSZA LICZBE UDZIALOW']], [['7', 'Dane wspolnikow'], ['1', ['1', 'SIERACZYMSKI'], ['2', 'RAFAL PIOTR'], ['3', '76012402011'], ['5', '91 UDZIALOW O LACZNEJ WARTOSCI 4.550 ZLOTYCH'], ['6', 'NIE']]], [['8', 'Kapital spolki'], ['1', '5000,00 ZL']]], ['2', [['1', 'Organ uprawniony do reprezentacji podmiotu'], ['1', ['1', 'ZARZAD'], ['2', 'DO SKLADANIA OSWIADCZEN W IMIENIU SPOLKI JEST UPOWAZNIONY KAZDY Z CZLONKOW ZARZADU SAMODZIELNIE.']], ['PRub.', ['1', ['1', 'SIERACZYNSKI'], ['2', 'RAFAL PIOTR'], ['3', '76012402011'], ['5', 'PREZES ZARZADU'], ['6', 'NIE']], ['2', ['1', 'STASZKIEWICZ'], ['2', 'MALGORZATA'], ['3', '76072200721'], ['5', 'CZLONEK ZARZADU'], ['6', 'NIE']]]]], ['3', [['1', 'Przedmiot dzialalnosci'], ['1', ['1', '71 11 Z']]]]]

frame_e3 = [['446575', 'BASICO A. PRZYBYSZ I M. KOCIKIEWICZ SPOLKA JAWNA', '0000706558', '30.11.2017'], ['1', [['1', 'Dane podmiot'], ['1', 'SPOLKA JAWNA'], ['2', 'REGON 146634993 NIP 9512366111'], ['3', 'BASICO A. PRZYBYSZ I M. KOCIKIEWICZ SPOLKA JAWNA'], ['5', 'NIE'], ['6', 'NIE']], [['2', 'Siedziba i adres podmiot'], ['1', ['kraj', 'POLSKA'], ['wojewodztwo', 'MAZOWIECKIE'], ['powiat', 'WARSZAWA'], ['gmina', 'WARSZAWA'], ['miejscowosc', 'WARSZAWA']], ['2', ['miejscowosc', 'WARSZAWA'], ['ulica', 'UL. ADAMA BRANICKIEGO'], ['nr domu', '11'], ['nr lokalu', '194'], ['kod pocztowy', '02-972'], ['poczta', 'WARSZAWA'], ['kraj', 'POLSKA']]], [['4', 'Informacje o umowie'], ['1', '26.10.2017R. UMOWA SPOLKI JAWNEJ']], [['5', 'None'], ['1', 'CZAS NIEOZNACZONY']], [['6', 'Sposob powstania spolki'], ['1', 'PRZEKSZTALCENIE'], ['2', 'UCHWALA WSP\\xd3LNIK\\xd3W SP\\xd3\\u0141KI CYWILNEJ ADAMA PRZYBYSZA I MARKA KO\\u015aCIKIEWICZA Z DNIA26.10.2017R. O DOKONANIU PRZEKSZTA\\u0141CENIA \\u0141\\u0104CZ\\u0104CEJ ICH SP\\xd3\\u0141KI CYWILNEJ PROWADZ\\u0104CEJ DZIA\\u0141ALNO\\u015a\\u0106 GOSPODARCZ\\u0104 POD NAZW\\u0104: BASICO SP\\xd3\\u0141KA CYWILNA W SP\\xd3\\u0141K\\u0118 JAWN\\u0104 W OPARCIU O PRZEPISY ART.26 \\xa7 4 KODEKSU SP\\xd3\\u0141EK HANDLOWYCH. ADAM PRZYBYSZ ZAMIESZKA\\u0141Y W POLKO UL. PER\\u0141OWA 19, 05-240 T\\u0141USZCZ, PESEL 79032916337, NIP: 762- 167-60-39, MAREK KO\\u015aCIKIEWICZ ZAMIESZKA\\u0141Y W PIASECZNIE 05-502 PRZY UL. SKRZETUSKIEGO 20, PESEL 60022203230, NIP: 527-021-32-11.'], ['PRub.', ['1', ['1', 'BASICO SPPOLKA CYWILNA MAREK KOCIKIEWICZ, ADAM PRZYBYSZ, 2. POLSKA, CENTRALNA EWIDENCJA I INFORMACJA O DZIAu0141ALNO\\u015aCI GOSPODARCZEJ'], ['5', '146634993'], ['6', '9512366111']]]], [['7', 'Dane wsp\\xf3lnik\\xf3w'], ['1', ['1', 'PRZYBYSZ'], ['2', 'ADAM'], ['3', '79032916337'], ['5', 'TAK'], ['6', 'NIE'], ['7', 'TAK'], ['8', 'NIE']], ['2', ['1', 'KO\\u015aCIKIEWICZ'], ['2', 'MAREK'], ['3', '60022203230'], ['5', 'NIE'], ['8', 'NIE']]]], ['2', [['1', 'Uprawnieni do reprezentowania sp\\xf3\\u0142ki'], ['1', ['1', 'WSP\\xd3LNICY REPREZENTUJ\\u0104CY SP\\xd3\\u0141K\\u0118'], ['2', 'KA\\u017bDY ZE WSP\\xd3LNIK\\xd3W MO\\u017bE REPREZENTOWA\\u0106 SP\\xd3\\u0141K\\u0118 SAMODZIELNIE.']], ['PRub.', ['1', ['1', 'PRZYBYSZ'], ['2', 'ADAM'], ['3', '79032916337']], ['2', ['1', 'KO\\u015aCIKIEWICZ'], ['2', 'MAREK'], ['3', '60022203230']]]]], ['3', [['1', 'Przedmiot dzialanosci'], ['1', ['1', '56 10 A RESTAURACJE I INNE STA\\u0141E PLAC\\xd3WKI GASTRONOMICZNE']], ['10', ['2', '56 10 B RUCHOME PLAC\\xd3WKI GASTRONOMICZNE']], ['2', ['2', '56 21 Z PRZYGOTOWYWANIE I DOSTARCZANIE \\u017bYWNO\\u015aCI DLA ODBIORC\\xd3W ZEWN\\u0118TRZNYCH (KATERING)']], ['3', ['2', '56 29 Z POZOSTA\\u0141A US\\u0141UGOWA DZIA\\u0141ALNO\\u015a\\u0106 GASTRONOMICZNA']], ['4', ['2', '56 30 Z PRZYGOTOWYWANIE I PODAWANIE NAPOJ\\xd3W']], ['5', ['2', '10 39 Z POZOSTA\\u0141E PRZETWARZANIE I KONSERWOWANIE OWOC\\xd3W I WARZYW']], ['6', ['2', '46 31 Z SPRZEDA\\u017b HURTOWA OWOC\\xd3W I WARZYW']], ['7', ['2', '46 32 Z SPRZEDA\\u017b HURTOWA MI\\u0118SA I WYROB\\xd3W Z MI\\u0118SA']], ['8', ['2', '46 33 Z SPRZEDA\\u017b HURTOWA MLEKA, WYROB\\xd3W MLECZARSKICH, JAJ, OLEJ\\xd3W I T\\u0141USZCZ\\xd3W JADALNYCH']], ['9', ['2', '46 34 A SPRZEDA\\u017b HURTOWA NAPOJ\\xd3W ALKOHOLOWYCH']]]]]

frame_e4 = [['23', 'ARKAD SPOLKA Z OGRANICZONA ODPOWIEDZIALNOSCIA', '0000270022', '20.12.2006'], ['1', [['1', 'Dane podmiotu'],['1', 'SPOLKA Z OGRANICZONA ODPOWIEDZIALNOSCIA'], ['3', '„ARKAD” SPOLKA Z OGRANICZONA ODPOWIEDZIALNOSCIA'], ['5', 'NIE'], ['6', 'NIE']], [['2', 'Siedziba i adres podmiotu'], ['1', ['kraj', 'POLSKA'], ['wojewodztwo', 'WIELKOPOLSKIE'], ['powiat', 'POZNANSKI'], ['gmina', 'ROKIETNICA'], ['miejscowosc', 'KIEKRZ']], ['2', ['miejscowosc', 'KIEKRZ'], ['ulica', 'STARZYNSKA'], ['nr domu', '37 C'], ['kod pocztowy', '62-090'], ['poczta', 'KIEKRZ'], ['kraj', 'POLSKA']]], [['4', 'Informacje o umowie'], ['1', '02.12.2006 R.; KANCELARIA NOTARIALNA LILIANNY DREWNIAK-ZABAW POZNANIU REP. A. 5766/2006.']], [['5', 'None'], ['1', 'CZAS NIEOZNACZONY'], ['3', 'WIEKSZA LICZBE UDZIALOW']], [['7', 'Dane wspolnikow'],['1', ['1', 'MATYSIAK'], ['2', 'TOMASZ'], ['3', '73120905236'], ['5', '25 UDZIALOW O LACZNEJ WYSOKOCI 25.000 ZŁOTYCH'], ['6', 'NIE']], ['2', ['1', 'BOGACKI'], ['2', 'PRZEMYSLAW'], ['3', '67072600314'], ['5', '25 UDZIALOW O LACZNEJ WYSOKOSCI 25.000 ZLOTYCH'], ['6', 'NIE']]], [['8', 'Kapital spolki'], ['1', '50000,00 ZL']]], ['2', [['1', 'Organ uprawniony do reprezentacji podmiotu'], ['1', ['1', 'ZARZAD'], ['2', 'DWAJCZLONKOWIE ZARZADU LACZNIE ALBO JEDEN CZLONEK ZARZADU LACZNIE Z PROKURENTEM.']], ['PRub.', ['1', ['1', 'MATYSIAK'], ['2', 'TOMASZ'], ['3','73120905236'], ['5', 'PREZES'], ['6', 'NIE']], ['2', ['1', 'BOGACKI'], ['2', 'PRZEMYSLAW'], ['3', '67072600314'], ['5', 'WICEPREZES'], ['6', 'NIE']]]]], ['3', [['1', 'Przedmiot dzialalnosci'], ['1', ['1', ['22', '1'], 'DZIALNOŚĆ WYDAWNICZA']], ['2', ['1', ['22', '2'], 'DZIALALNOSC POLIGRAFICZNA']]]]]
# ['3', ['1', ['22', '3'], 'REPRODUKCJA ZAPISANYCH NOSNIKOW INFORMACJI']], ['4', ['1', ['51'], 'HANDEL HURTOWY I KOMISOWY, Z WYLACZENIEM HANDLU POJAZDAMI SAMOCHODOWYMI, MOTOCYKLAMI']], ['5', ['1', ['52'], 'HANDEL DETALICZNY, Z WYLACZENIEM SPRZEDAZY POJAZDOW SAMOCHODOWYCH, MOTOCYKLI; NAPRAWA ARTYKULOW UZYTKU OSOBISTEGO I DOMOWEGO']], ['6', ['1', ['55'], 'HOTELE I RESTAURACJE']], ['7', ['1', ['63', '3'], 'DZIALALNOSC ZWIAZANA Z TURYSTYKA']], ['8', ['1'  ['70'], 'OBSLUGA NIERUCHOMOSCI']], ['9', ['1', ['71', '40', 'Z'], 'WYPOZYCZANIE ARTYKULOW UŻYTKU OSOBISTEGO I DOMOWEGO']], ['10', ['1', ['74', '8'], 'DZIALALNOSC KOMERCYJNA GDZIE INDZIEJ NIESKLASYFIKOWANA']], ['11', ['1', ['85', '14', 'A'], 'DZIALALNOSC FIZJOTERAPEUTYCZNA']], ['12', ['1', ['85', '14', 'D'], 'DZIALALNOSC PSYCHOLOGICZNA I PSYCHOTERAPEUTYCZNA']], ['13', ['1', ['85', '14', 'E'], 'DZIALALNOSC PARAMEDYCZNA']], ['14', ['1', ['85', '14', 'F'], 'DZIALALNOSC ZWIAZANA Z OCHRONA ZDROWIA LUDZKIEGO POZOSTALA, GDZIE INDZIEJ NIESKLASYFIKOWANA']], ['15', ['1', ['93', '04', 'Z'], 'DZIAŁALNOŚĆ ZWIĄZANA Z POPRAWA KONDYCJI FIZYCZNEJ']], ['16', ['1', ['93', '05', 'Z'], 'DZIAŁALNOŚĆ USŁUGOWA POZOSTAŁA, GDZIE INDZIEJ NIESKLASYFIKOWANA']]]]]

frame_e5 = [['13', 'BRAIN SPOLKA Z OGRANICZONA ODPOWIEDZIALNOSCIA SPOLKA KOMANDYTOWA', '0000269833', '19.12.2006'], ['1', [['1', 'Dane podmiotu'], ['1', 'SPOLKA KOMANDYTOWA'], ['3', 'BRAIN SPOLKA Z OGRANICZONA ODPOWIEDZIALNOSCIA SPOLKA KOMANDYTOWA'], ['5', 'NIE'], ['6', 'NIE']], [['2', 'Siedziba i adres podmiotu'], ['1', ['kraj', 'POLSKA'], ['wojewodztwo', 'MAZOWIECKIE'], ['powiat', 'M.ST. WARSZAWA'], ['gmina', 'M.ST. WARSZAWA'], ['miejscowosc', 'WARSZAWA']], ['2', ['miejscowosc', 'WARSZAWA'], ['ulica', 'SLONECZNA'], ['nr domu', '29'], ['kod pocztowy', '00-789'], ['poczta', 'WARSZAWA'], ['kraj', 'POLSKA']]], [['4', 'Informacje o umowie'], ['1', 'UMOWA SPOLKI ZAWARTA DNIA 27 PAZDZIERNIKA 2006 ROKU PRZED LUIZA ZIELINSKA ASESOREM NOTARIALNYM ZASTĘPCA PAWŁA BLASZCZAKA NOTARIUSZA W WARSZAWIE Z KANCELARII NOTARIALNEJ W WARSZAWIE PRZY UL. DŁUGIEJ 31; REP. A NR 18052/2006']], [['5', 'None'], ['1', 'CZAS NIEOZNACZONY']], [['6', 'Sposob powstania spolki'], ['1', 'PRZEKSZTALCENIE'], ['2', 'UCHWALA WSPOLNIKOW SPOLKI JAWNEJ: BRAIN, MALINOWSKA I KAMINSKI SPOLKA JAWNA Z SIEDZIBA W WARSZAWIE Z DNIA 27 PAZDZIERNIKA 2006 ROKU - PROTOKOL NOTARIALNY SPORZADZONY PRZEZ LUIZE ZIELIMSKA ASESORA NOTARIALNEGO, ZASTEPCE PAWLA BLASZCZAKA NOTARIUSZA W WARSZAWIE Z KANCELARII NOTARIALNEJ PRZY UL. DLUGIEJ 31 W WARSZAWIE (REP. A NR 18048/2006)'], ['PRub.', ['1', ['1', 'BRAIN, MALINOWSKA I KAMIMSKI SPOLKA JAWNA”'], ['2', 'REJESTR KRS'], ['3', '0000126785'], ['5', '015209116']]]], [['7', 'Dane wspolnikow'], ['1', ['1', 'KAMINSKI'], ['2', 'JAKUB FILIP'], ['3', '70030100232'], ['5', 'NIE'], ['8', 'NIE'], ['9', 'TAK'], ['10', '66.985, 66 PLN'], ['11', '66.985, 66 PLN'], ['12', 'TAK']], ['PRub.', ['1', ['1', '66.985, 66 PLN'], ['2', 'TAK']], ['2', ['1', 'MALINOWSKA'], ['2', 'ASIYA'], ['3', '68122412402'], ['5', 'NIE'], ['8', 'NIE'], ['9', 'TAK'], ['10', '28.707, 90 PLN'], ['11', '28.707, 90 PLN'], ['12', 'NIE']]], ['PRub.', ['1', ['1', '28.707, 90 PLN'], ['2', 'NIE']], ['3', ['1', 'BRAIN SPOLKA Z OGRANICZONA ODPOWIEDZIALNOSCIA'], ['3', '140705918'], ['4', '0000264329'], ['9', 'NIE']]]]], ['2', [['1', 'Uprawnieni do reprezentowania spolki'], ['1', ['1', 'WSPOLNICY REPREZENTUJACY SPOLKE'], ['2', 'PRAWO REPREZENTACJI PRZYSLUGUJE JEDYNIE KOMPLEMENTARIUSZOWI. KOMPLEMENTARIUSZ DZIALA PRZEZ SWOJE ORGANY. DO SKLADANIA OSWIADCZEN W IMIENIU KOMPLEMENTARIUSZA WYMAGA SIE WSPOLDZIALANIA DWOCH CZŁONKOW ZARZADU BADZ JEDNEGO CZLONKA ZARZADU LACZNIE Z PROKURENTEM. W SKLAD ZARZADU KOMPLEMENTARIUSZA WCHODZA: JAKUB FILIP KAMINSKI I ASIYA MALINOWSKA.']], ['PRub.', ['1', ['1', 'BRAIN SPOLKA Z OGRANICZONA ODPOWIEDZIALNOSCIA'], ['3', '140705918'], ['4', '0000264329']]]]], ['3', [['1', 'Przedmiot dzialalnosci'], ['1', ['1', ['74', '40', 'Z'], 'REKLAMA']], ['2', ['1', ['92', '20', 'Z'], 'DZIALALNOSC RADIOWA I TELEWIZYJNA']], ['3', ['1', ['92', '11', 'Z'], 'PRODUKCJA FILMOW I NAGRAN WIDEO']], ['4', ['1', ['92', '12', 'Z'], 'ROZPOWSZECHNIANIE FILMOW I NAGRAN WIDEO']], ['5', ['1', ['22', '14', 'Z'], 'WYDAWANIE NAGRAN DZWIĘKOWYCH']], ['6', ['1', ['22', '11', 'Z'], 'WYDAWANIE KSIZEEK']], ['7', ['1', ['22', '12', 'Z'], 'WYDAWANIE GAZET']], ['8', ['1', ['22', '13', 'Z'], 'WYDAWANIE CZASOPISM I WYDAWNICTW PERIODYCZNYCH']], ['9', ['1', ['22', '15', 'Z'], 'POZOSTAŁA DZIAŁALNOŚĆ WYDAWNICZA.']], ['10', ['1', ['74', '14', 'A'], 'DORADZTWO W ZAKRESIE PROWADZENIA DZIAŁALNOŚCI GOSPODARCZEJ I ZARZĄDZANIA']], ['11', ['1', ['74', '84', 'B'], 'POZOSTAŁA DZIAŁALNOŚĆ KOMERCYJNA, GDZIE INDZIEJ NIESKLASYFIKOWANA.']], ['12', ['1', ['74', '81', 'Z'], 'DZIAŁALNOŚĆ FOTOGRAFICZNA']]]]]

frame_e6 = [['469309', 'LEAWARE SPOLKA AKCYJNA', '0000709693', '20.12.2017'], ['20.12.2017', '1'], ['1', [['1', 'Dane podmiotu'], ['1', 'SPOLKA AKCYJNA'], ['3', 'LEAWARE SPOLKA AKCYJNA'], ['5', 'NIE'], ['6', 'NIE']], [['2', 'Siedziba i adres podmiotu'], ['1', ['kraj', 'POLSKA'], ['wojewodztwo', 'MAZOWIECKIE'], ['powiat', 'WARSZAWA'], ['gmina', 'WARSZAWA'], ['miejscowosc', 'WARSZAWA']], ['2', ['miejscowosc', 'WARSZAWA'], ['ulica', 'UL. PERKUNA'], ['nr domu', '86'], ['nr lokalu', '1'], ['kod pocztowy', '04-124'], ['poczta', 'WARSZAWA'], ['kraj', 'POLSKA']]], [['4', 'Informacje o statucie'], ['1', ['1', '14.11.2017 R., REP. A NR 10960/2017 NOTARIUSZ MAGDALENA DZIERBA, KANCELARIA NOTARIALNA W WARSZAWIE']]], [['5', 'None'], ['1', 'CZAS NIEOZNACZONY'], ['4', 'NIE'], ['5', 'NIE']], [['8', 'Kapital spolki'], ['1', '100000,00 ZL'], ['3', '100000'], ['4', '1,00 ZŁ'], ['5', '25000,00 ZŁ']], [['9', 'Emisje akcji'], ['1', ['1', 'A'], ['2', '100000'], ['3', 'AKCJE NIE SA UPRZYWILEJOWANE']], ['2', ['1', 'A']]], [['11', 'None'], ['1', 'NIE']]], ['2', [['1', 'Organ uprawniony do reprezentacji podmiotu'], ['1', ['1', 'ZARZAD'], ['2', 'xD']], ['PRub.', ['1', ['1', 'SOROKA'], ['2', 'TOMASZ ANTONI'], ['3', '80032911499'], ['5', 'PREZES ZARZADU'], ['6', 'NIE']]]], [['2', 'Organ nadzoru'], ['1', ['1', 'RADA NADZORCZA']], ['PRub.', ['1', ['1', 'SOROKA'], ['2', 'IWONA'], ['3', '80082812146']], ['2', ['1', 'WAZ'], ['2', 'GRAZYNA'], ['3', '74011011609']], ['3', ['1', 'WAZ'], ['2', 'ZBIGNIEW'], ['3', '77010519499']]]]], ['3', [['1', 'Przedmiot dzialalności'], ['1', ['1', ['62', '01', 'Z'], 'DZIAŁALNOSC ZWIAZANA Z OPROGRAMOWANIEM']], ['1', ['2', ['70', '22', 'Z'], 'POZOSTAŁE DORADZTWO W ZAKRESIE PROWADZENIA DZIAŁALNOŚCI GOSPODARCZEJ I ZARZĄDZANIA']], ['2', ['2', ['85', '59', 'B'], 'POZOSTAŁE POZASZKOLNE FORMY EDUKACJI, GDZIE INDZIEJ NIESKLASYFIKOWANE']]]]]


frame_e7 = [['469202', 'KARLIK LIMITED SPOLKA KOMANDYTOWO-AKCYJNA', '0000710436', '20.12.2017'], ['1', [['1', 'Dane podmiotu'], ['1', 'SPOLKA KOMANDYTOWO-AKCYJNA'], ['3', 'KARLIK LIMITED SPOLKA KOMANDYTOWO-AKCYJNA'], ['4', 'NIE'], ['5', 'NIE']], [['2', 'Siedziba i adres podmiotu'], ['1', ['kraj', 'POLSKA'], ['wojewodztwo', 'OPOLSKIE'], ['powiat', 'OPOLSKI'], ['gmina', 'TURAWA'], ['miejscowosc', 'KOTORZ WIELKI']], ['2', ['miejscowosc', 'KOTORZ WIELKI'], ['ulica', 'UL. POLNA'], ['nr domu', '23'], ['kod pocztowy', '46-045'], ['poczta', 'TURAWA'], ['kraj', 'POLSKA']]], [['4', 'Informacje o statucie'], ['1', ['1', '19.04.2017R. ZASTEPCA NOTARIALNY NOTARIUSZA WOJCIECHA MYGI - ALEKSANDRA RESPONDEK, KANCELARIA NOTARIALNA W OPOLU, REP. A NR 4006/2017']]], [['5', 'None'], ['1', 'CZAS NIEOZNACZONY']], [['7', 'Dane komplementariuszy'], ['1', ['1', 'KARLIK LIMITED']]], [['8', 'Kapital spolki'], ['1', '50000,00 ZL'], ['2', '500'], ['3', '100,00 ZL'], ['4', '50000,00 ZL']], [['9', 'Emisje akcji'], ['1', ['1', 'A'], ['2', '500'], ['3', 'AKCJE NIE SA UPRZYWILEJOWANE']]]], ['2', [['1', 'Uprawnieni do reprezentowania spolki'], ['1', ['1', 'KOMPLEMENTARIUSZ SAMODZIELNIE']], ['PRub.', ['1', ['1', 'KARLIK LIMITED']]]]], ['3', [['1', 'Przedmiot dzialalnosci'], ['1', ['1', ['49', '41', 'Z'], 'TRANSPORT DROGOWY TOWAROW']], ['1', ['2', ['45', '19', 'Z'], 'SPRZEDAZ HURTOWA I DETALICZNA POZOSTALYCH POJAZDOW SAMOCHODOWYCH, Z WYLACZENIEM MOTOCYKLI']], ['2', ['2', ['49', '31', 'Z'], 'TRANSPORT LADOWY PASAZERSKI, MIEJSKI I PODMIEJSKI']], ['3', ['2', ['49', '39', 'Z'], 'POZOSTALY TRANSPORT LADOWY PASAZERSKI, GDZIE INDZIEJ NIESKLASYFIKOWANY']], ['4', ['2', ['49', '42'], 'DZIALALNOSC USLUGOWA ZWIAZANA Z PRZEPROWADZKAMI']], ['5', ['2', ['68', '20', 'Z'], 'WYNAJEM I ZARZADZANIE NIERUCHOMOSCIAMI WLASNYMI LUB DZIERZAWIONYMI']], ['6', ['2', ['70', '10', 'Z'], 'DZIALALNOSC FIRM CENTRALNYCH (HEAD OFFICES) I HOLDINGOW, Z WYLACZENIEM HOLDINGOW FINANSOWYCH']], ['7', ['2', ['70', '22', 'Z'], 'POZOSTALE DORADZTWO W ZAKRESIE PROWADZENIA DZIALALNOSCI GOSPODARCZEJ I ZARZADZANIA']], ['8', ['2', ['73', '11', 'Z'], 'DZIALALNOSC AGENCJI REKLAMOWYCH']], ['9', ['2', ['77', '11', 'Z'], 'WYNAJEM I DZIERZAWA SAMOCHODOW OSOBOWYCH I FURGONETEK']]]]]

frame_e8 = [['190235', 'SPOLDZIELNIA PRODUCENTOW TRZODY CHLEWNEJ „MIR-TUCZ”', '0000684566', '28.06.2017'], ['28.06.2017', '1'], ['1', [['1', 'Dane podmiotu'], ['1', 'SPOLDZIELNIA'], ['3', 'SPOLDZIELNIA PRODUCENTOW TRZODY CHLEWNEJ „MIR-TUCZ”'], ['5', 'NIE'], ['6', 'NIE']], [['2', 'Siedziba i adres podmiotu'], ['1', ['kraj', 'POLSKA'], ['wojewodztwo', 'LODZKIE'], ['powiat', 'PIOTRKOWSKI'], ['gmina', 'GRABICA'], ['miejscowosc', 'WOLA KAMOCKA']], ['2', ['miejscowosc', 'WOLA KAMOCKA'], ['nr domu', '14'], ['kod pocztowy', '97-306'], ['poczta', 'GRABICA'], ['kraj', 'POLSKA']]], [['4', 'Informacje o statucie'], ['1', ['1', 'STATUT SPOLDZIELNI SPORZADZONY I PRZYJETY W DNIU 6 CZERWCA 2017 R.']]], [['5', 'None'], ['1', 'CZAS NIEOZNACZONY']]], ['2', [['1', 'Organ uprawniony do reprezentacji podmiotu'], ['1', ['1', 'ZARZAD SPOLDZIELNI'], ['2', 'OSWIADCZENIA WOLI ZA SPOLDZIELNIE SKLADAJA DWAJ CZLONKOWIE ZARZADU LUB JEDEN CZLONEK ZARZADU I PELNOMOCNIK']], ['PRub.', ['1', ['1', 'MIROWSKI'], ['2', 'SLAWOMIR PIOTR'], ['3', '72061910558'], ['4', 'PREZES ZARZADU'], ['5', 'NIE']], ['2', ['1', 'OLASIK'], ['2', 'ROBERT'], ['3', '72020315077'], ['4', 'WICEPREZES ZARZADU'], ['5', 'NIE']]]], [['4', 'Pelnomocnicy'], ['1', ['1', 'CHRZEST'], ['2', 'SEBASTIAN LUKASZ'], ['3', '86082815950'], ['4', 'PELNOMOCNICTWO DO DOKONYWANIA CZYNNOSCI PRAWNYCH ZWIAZANYCH Z KIEROWANIEM BIEZACA DZIALALNOSCIA SPOLDZIELNI']]]], ['3', [['1', 'Przedmiot dzialalnosci'], ['1', ['1', ['46', '23', 'Z'], 'SPRZEDAZ HURTOWA ZYWYCH ZWIERZAT'], ['None', ['01', '61', 'Z'], 'DZIALALNOSC USLUGOWA WSPOMAGAJACA PRODUKCJE ROSLINNA'], ['None', ['01', '62', 'Z'], 'DZIALALNOSC USLUGOWA WSPOMAGAJACA CHOW I HODOWLE ZWIERZAT GOSPODARSKICH'], ['None', ['10', '11', 'Z'], 'PRZETWARZANIE I KONSERWOWANIE MIESA, Z WYLACZENIEM MIESA Z DROBIU'], ['None', ['10', '13', 'Z'], 'PRODUKCJA WYROBOW Z MIESA, WLACZAJAC WYROBY Z MIESA DROBIOWEGO'], ['None', ['10', '41', 'Z'], 'PRODUKCJA OLEJOW I POZOSTALYCH TLUSZCZOW PLYNNYCH'], ['None', ['10', '91', 'Z'], 'PRODUKCJA GOTOWEJ PASZY DLA ZWIERZAT GOSPODARSKICH'], ['None', ['46', '21', 'Z'], 'SPRZEDAZ HURTOWA ZBOZA, NIEPRZETWORZONEGO TYTONIU, NASION I PASZ DLA ZWIERZAT'], ['None', ['47', '22', 'Z'], 'SPRZEDAZ DETALICZNA MIESA I WYROBOW Z MIESA PROWADZONA W WYSPECJALIZOWANYCH SKLEPACH'], ['None', ['77', '31', 'Z'], 'WYNAJEM I DZIERZAWA MASZYN I URZADZEŃ ROLNICZYCH']]]]]


frame_e9 = [['469314', 'STOWARZYSZENIE WARMINSKA MANUFAKTURA KULTURY', '0000709753', '20.12.2017'], ['1', [['1', 'Dane podmiotu'], ['1', 'STOWARZYSZENIE'], ['3', 'STOWARZYSZENIE WARMINSKA MANUFAKTURA KULTURY'], ['5', 'NIE'], ['6', 'NIE']], [['2', 'Siedziba i adres podmiotu'], ['1', ['kraj', 'POLSKA'], ['wojewodztwo', 'WARMINSKO-MAZURSKIE'], ['powiat', 'OLSZTYN'], ['gmina', 'OLSZTYN'], ['miejscowosc', 'OLSZTYN']], ['2', ['miejscowosc', 'OLSZTYN'], ['ulica', 'UL. STAROMIEJSKA'], ['nr domu', '1'], ['kod pocztowy', '10-017'], ['poczta', 'OLSZTYN'], ['kraj', 'POLSKA']]], [['4', 'Informacje o statucie'], ['1', ['1', 'STATUT PRZY JETO W DNIU 19.07.2017R. UCHWALA CZLONKOW ZALOZYCIELI NR 9/2017 Z DNIA 16.11.2017R. ZMIENIONO:  5,  15 UST.1 I UST. 3,  23 UST. 4, § 25 UST. 3, DODANO W  4 UST.3, W § 16 UST. 3, W  23 UST. 5, W  25 UST. 4, W  27 UST. 4 I UST. 5 STATUTU. UCHWALA CZLONKOW ZALOZYCIELI NR 10/2017 Z DNIA 05.12.2017R., ZMIENIONO:  22 PKT 11 STATUTU.']]], [['5', 'None'], ['1', 'CZAS NIEOZNACZONY']], [['8', 'Organ sprawujący nadzor'], ['1', 'PREZYDENT MIASTA OLSZTYN']]], ['2', [['1', 'Organ uprawniony do reprezentacji podmiotu'], ['1', ['1', 'ZARZAD'], ['2', 'DO SKLADANIA OSWIADCZEN WOLI W IMIENIU STOWARZYSZENIA, W TYM W SPRAWACH MAJATKOWYCH, UPRAWNIONYCH JEST DWOCH CZLONKOW ZARZADU DZIALAJACYCH LACZNIE.']], ['PRub.', ['1', ['1', 'BOGDANOWICZ BARTNIKOWSKA'], ['2', 'MALGORZATA'], ['3', '57052203363'], ['5', 'PREZES ZARZADU']], ['2', ['1', 'KREPULA'], ['2', 'RYSZARD JOZEF'], ['3', '54072304195'], ['5', 'CZLONEK ZARZADU']], ['3', ['1', 'BOGDANOWICZ'], ['2', 'BARBARA'], ['3', '69120203702'], ['5', 'CZLONEK ZARZADU']], ['4', ['1', 'TOS'], ['2', 'RAFAL PAWEL'], ['3', '76022502538'], ['5', 'CZLONEK ZARZADU']]]], [['2', 'Organ nadzoru'], ['1', ['1', 'KOMISJA REWIZYJNA']], ['PRub.', ['1', ['1', 'BONK'], ['2', 'PRZEMYSLAW MIKOLAJ'], ['3', '59102404292']], ['2', ['1', 'MAJCHER'], ['2', 'WALDEMAR JACEK'], ['3', '56081703051']], ['3', ['1', 'WAWER'], ['2', 'WANDA URSZULA'], ['3', '53031205960']]]]], ['3', [['1', 'Przedmiot dzialalnosci'], ['1', ['1', ['85', '52', 'Z'], 'POZASZKOLNE FORMY EDUKACJI ARTYSTYCZNEJ']], ['1', ['2', ['90', '03', 'Z'], 'ARTYSTYCZNA I LITERACKA DZIALALNOSC TWORCZA']], ['2', ['2', ['93', '29', 'Z'], 'POZOSTALA DZIALALNOSC ROZRYWKOWA I REKREACYJNA']], ['3', ['2', ['58', '11', 'Z'], 'WYDAWANIE KSIAZEK']], ['4', ['2', ['58', '19', 'Z'], 'POZOSTALA DZIALALNOSC WYDAWNICZA']]], [['3', 'Cel dzialania organizacji'], ['1', 'CELEM DZIALANIA STOWARZYSZENIA JEST PROPAGOWANIE, WZMACNIANIE I OCHRONA DZIEDZICTWA KULTUROWEGO WARMII I MAZUR ORAZ PROWADZENIE DZIALALNOSCI EDUKACYJNEJ I KULTURALNEJ ZWLASZCZA NA RZECZ DZIECI I MLODZIEZY ORAZ OSOB STARSZYCH.']]]]



frame_e10 = [['332', 'FUNDACJA BARFNE KOREPETYCJE', '0000652954', '22.12.2016'], ['1', [['1', 'Dane podmiotu'], ['1', 'FUNDACJA'], ['3', 'FUNDACJA BARFNE KOREPETYCJE'], ['5', 'NIE'], ['6', 'NIE']], [['2', 'Siedziba i adres podmiotu'], ['1', ['kraj', 'POLSKA'], ['wojewodztwo', 'MALOPOLSKIE'], ['powiat', 'OLKUSKI'], ['gmina', 'OLKUSZ'], ['miejscowosc', 'OLKUSZ']], ['2', ['miejscowosc', 'OLKUSZ'], ['ulica', 'UL. DLUGA'], ['nr domu', '1A'], ['kod pocztowy', '32-300'], ['poczta', 'OLKUSZ'], ['kraj', 'POLSKA']]], [['4', 'Informacje o statucie'], ['1', ['1', '30.09.2016 R']]], [['5', 'None'], ['1', 'CZAS NIEOZNACZONY']], [['8', 'Organ sprawujacy nadzor'], ['1', 'MINISTER SPRAW WEWNETRZNYCH I ADMINISTRACJI STAROSTA OLKUSKI']]], ['2', [['1', 'Organ uprawniony do reprezentacji podmiotu'], ['1', ['1', 'ZARZAD'], ['2', 'W PRZYPADKU ZARZADU FUNDACJI JEDNOOSOBOWEGO - PREZES ZARZADU FUNDACJI SAMODZIELNIE. W PRZYPADKU ZARZADU FUNDACJI WIELOOSOBOWEGO- W PRZYPADKU ZARZADU WIELOOSOBOWEGO KAZDY CZLONEK ZARZADU MOZE DZIALAĆ SAMODZIELNIE']], ['PRub.', ['1', ['1', 'FEDYNIAK'], ['2', 'JAGODA MARTA'], ['3', '84040609968'], ['5', 'CZLONEK ZARZADU']], ['2', ['1', 'CHOLEWIAK GORALCZYK'], ['2', 'AGNIESZKA INGA'], ['3', '86013000965'], ['5', 'PREZES ZARZADU']]]], [['2', 'Organ nadzoru'], ['1', ['1', 'RADA FUNDACJI']], ['PRub.', ['1', ['1', 'SALWEROWICZ'], ['2', 'EWA ANNA'], ['3', '91070312889']], ['2', ['1', 'GORALCZYK'], ['2', 'LUKASZ'], ['3', '86082001759']], ['3', ['1', 'BOCHENEK'], ['2', 'LUKASZ'], ['3', '81030414076']]]]], ['3', [['1', 'Przedmiot dzialalnocci'], ['1', ['1', ['47', '76', 'Z'], 'SPRZEDAZ DETALICZNA KWIATOW, ROSLIN, NASION, NAWOZOW, ZYWYCH ZWIERZAT DOMOWYCH, KARMY DLA ZWIERZAT DOMOWYCH PROWADZONA W WYSPECJALIZOWANYCH SKLEPACH'], ['None', ['46', '19', 'Z'], 'DZIALALNOSĆ AGENTOW ZAJMUJACYCH SIE SPRZEDAZA TOWAROW ROZNEGO RODZAJU'], ['None', ['46', '21', 'Z'], 'SPRZEDAZ HURTOWA ZBOZA, NIEPRZETWORZONEGO TYTONIU, NASION I PASZ DLA ZWIERZAT'], ['None', ['47', '19', 'Z'], 'POZOSTALA SPRZEDAZ DETALICZNA PROWADZONA W NIEWYSPECJALIZOWANYCH SKLEPACH'], ['None', ['46', '90', 'Z'], 'SPRZEDAZ HURTOWA NIEWYSPECJALIZOWANA'], ['None', ['47', '78', 'Z'], 'SPRZEDAZ DETALICZNA POZOSTALYCH NOWYCH WYROBOW PROWADZONA W WYSPECJALIZOWANYCH SKLEPACH'], ['None', ['47', '99', 'Z'], 'POZOSTALA SPRZEDAZ DETALICZNA PROWADZONA POZA SIECIA SKLEPOWA, STRAGANAMI I TARGOWISKAMI'], ['None', ['01', '62', 'Z'], 'DZIALALNOSĆ USLUGOWA WSPOMAGAJACA CHOW I HODOWLE ZWIERZAT GOSPODARSKICH'], ['None', ['47', '22', 'Z'], 'SPRZEDAZ DETALICZNA MIESA I WYROBOW Z MIESA PROWADZONA W WYSPECJALIZOWANYCH SKLEPACH'], ['None', ['47', '61', 'Z'], 'SPRZEDAZ DETALICZNA KSIAZEK PROWADZONA W WYSPECJALIZOWANYCH SKLEPACH']]], [['3', 'Cel dzialania organizacji'], ['1', 'INSPIROWANIE I PROMOWANIE ZDROWEGO ZYWIENIA ZWIERZAT DOMOWYCH (W SZCZEGOLNOSCI PSOW I KOTOW). PROPAGOWANIE ZYWIENIA METODA BARF - BIOLOGICALLY APPROPRIATE RAW FOOD (BIOLOGICZNIE ODPOWIEDNIA SUROWA DIETA). POMOC FUNDACJOM, STOWARZYSZENIOM I OSOBOM DZIALAJACYM NA RZECZ ZWIERZAT POPRZEZ EDUKACJE NA TEMAT ZYWIENIA PSOW I KOTOW ORAZ PROWADZENIE ZBIOREK NA TEN CEL. ORGANIZOWANIE TARGOW, SPOTKAN, SEMINARIOW, KONFERENCJI MAJACYCH PROMOWAĆ ZYWIENIE METODA BARF W KRAJU I NA SWIECIE. PRZYZNAWANIE CERTYKATOW JAKOSCI DLA WYSOKOJAKOSCIOWYCH SUPLEMENTOW DLA ZWIERZAT. PRZYZNAWANIE CERTYFIKATOW DLA OSOB, HODOWLI, WETERYNARZY, FUNDACJI I STOWARZYSZEN KARMIACYCH ZWIERZETA METODA BARF, BADŹ MAJACYCH WIEDZE W TYM ZAKRESIE. PODEJMOWANIE DZIALAN BADAWCZYCH, ANALITYCZNYCH I EDUKACYJNYCH W PRZEDMIOCIE PODNIESIENIA JAKOSCI ZYWIENIA ZWIERZAT DOMOWYCH. PODEJMOWANIE INICJATYW EDUKACYJNYCH I BADAWCZYCH W ZAKRESIE PROBLEMATYKI ZYWIENIA ZWIERZAT DOMOWYCH.']]]]




frame_e11 = [['335', 'PSMI GMBH SPOLKA Z OGRANICZONA ODPOWIEDZIALNOSCIA ODDZIAL W POLSCE', '0000654393', '22.12.2016'], ['1', [['1', 'Dane podmiotu'], ['1', 'ODDZIAL ZAGRANICZNEGO PRZEDSIEBIORCY'], ['3', 'PSMI GMBH SPOLKA Z OGRANICZONA ODPOWIEDZIALNOSCIA ODDZIAL W POLSCE'], ['4', 'PSMI GMBH'], ['5', 'HANDELSREGISTER B DES AMTSGERICHTS FRANFURKT AM MEIN, HRB 106696'], ['6', 'PRAWO NIEMIECKIE'], ['8', 'NIE'], ['9', 'NIE']], [['2', 'Siedziba i adres oddzialu'], ['1', ['kraj', 'POLSKA'], ['wojewodztwo', 'MALOPOLSKIE'], ['powiat', 'KRAKOW'], ['gmina', 'KRAKOW'], ['miejscowosc', 'KRAKOW']], ['2', ['miejscowosc', 'KRAKOW'], ['ulica', 'UL. STANISLAWA MONIUSZKI'], ['nr domu', '50'], ['kod pocztowy', '31-523'], ['poczta', 'KRAKOW'], ['kraj', 'POLSKA']], ['3', ['kraj', 'NIEMCY'], ['jednostka podzialu terytorialnego', 'KRAJ ZWIAZKOWY HESJA'], ['miejscowosc', 'FRANKFURT NAD MENEM'], ['ulica', 'WALTHER-VON-CRONBERG-PLATZ'], ['nr domu', '13'], ['nr lokalu', '--'], ['kod pocztowy', '60594'], ['poczta', 'FRANKFURT NAD MENEM']]]], ['2', [['1', 'Organ uprawniony do reprezentowania zagranicznego przedsiebiorcy'], ['1', ['1', 'ZARZAD'], ['2', 'JEZELI ZARZAD JEST JEDNOOSOBOWY, CZLONEK ZARZADU REPREZENTUJE SPOLKE SAMODZIELNIE. JEZELI ZARZAD JEST WIELOOSOBOWY, TO SPOLKA MOZE BYC REPREZENTOWANA PRZEZ DWOCH CZLONKOW ZARZADU LACZNIE LUB PRZEZ JEDNEGO CZLONKA ZARZADU WRAZ Z PROKURENTEM']], ['PRub.', ['1', ['1', 'MULLICK'], ['2', 'JAY'], ['5', 'CZLONEK ZARZADU']]]], [['4', 'Osoby reprezentujace zagranicznego przedsiebiorce w oddziale'], ['1', ['1', 'MULLICK'], ['2', 'JAY']]]], ['3', [['1', 'Przedmiot dzialalnosci'], ['1', ['1', ['46', '69', 'Z'], 'SPRZEDAZ HURTOWA POZOSTALYCH MASZYN I URZADZEN'], ['None', ['45', '31', 'Z'], 'SPRZEDAZ HURTOWA CZESCI I AKCESORIOW DO POJAZDOW SAMOCHODOWYCH, Z WYLACZENIEM MOTOCYKLI'], ['None', ['45', '32', 'Z'], 'SPRZEDAZ DETALICZNA CZESCI I AKCESORIOW DO POJAZDOW SAMOCHODOWYCH, Z WYLACZENIEM MOTOCYKLI'], ['None', ['46', '62', 'Z'], 'SPRZEDAZ HURTOWA OBRABIAREK'], ['None', ['46', '14', 'Z'], 'DZIALALNOSC AGENTOW ZAJMUJACYCH SIE SPRZEDAZA MASZYN, URZADZEN PRZEMYSLOWYCH, STATKOW I SAMOLOTOW'], ['None', ['46', '52', 'Z'], 'SPRZEDAZ HURTOWA SPRZETU ELEKTRONICZNEGO I TELEKOMUNIKACYJNEGO ORAZ CZESCI DO NIEGO']]]]]



frame_e12 = [['23', '„ARKAD” SPOLKA Z OGRANICZONA ODPOWIEDZIALNOSCIA', '0000270022', '20.12.2006'], ['20.12.2006', '1'], ['1', [['1', 'Dane podmiotu'], ['1', 'SPOLKA Z OGRANICZONA ODPOWIEDZIALNOSCIA'], ['3', '„ARKAD” SPOLKA Z OGRANICZONA ODPOWIEDZIALNOSCIA'], ['5', 'NIE'], ['6', 'NIE']], [['2', 'Siedziba i adres podmiotu'], ['1', ['kraj', 'POLSKA'], ['wojewodztwo', 'WIELKOPOLSKIE'], ['powiat', 'POZNANSKI'], ['gmina', 'ROKIETNICA'], ['miejscowosc', 'KIEKRZ']], ['2', ['miejscowosc', 'KIEKRZ'], ['ulica', 'STARZYNSKA'], ['nr domu', '37 C'], ['kod pocztowy', '62-090'], ['poczta', 'KIEKRZ'], ['kraj', 'POLSKA']]], [['4', 'Informacje o umowie'], ['1', '02.12.2006 R.; KANCELARIA NOTARIALNA LILIANNY DREWNIAK-ZABA W POZNANIU REP. A. 5766/2006.']], [['5', 'None'], ['1', 'CZAS NIEOZNACZONY'], ['3', 'WIĘKSZA LICZBĘ UDZIALOW']], [['7', 'Dane wspolnikow'], ['1', ['1', 'MATYSIAK'], ['2', 'TOMASZ'], ['3', '73120905236'], ['5', '25 UDZIALOW O LACZNEJ WYSOKOSCI 25.000 ZLOTYCH'], ['6', 'NIE']], ['2', ['1', 'BOGACKI'], ['2', 'PRZEMYSLAW'], ['3', '67072600314'], ['5', '25 UDZIALOW O LACZNEJ WYSOKOSCI 25.000 ZLOTYCH'], ['6', 'NIE']]], [['8', 'Kapital spolki'], ['1', '50000,00 ZL']]], ['2', [['1', 'Organ uprawniony do reprezentacji podmiotu'], ['1', ['1', 'ZARZAD'], ['2', 'DWAJ CZLONKOWIE ZARZADU LACZNIE ALBO JEDEN CZLONEK ZARZADU LACZNIE Z PROKURENTEM.']], ['PRub.', ['1', ['1', 'MATYSIAK'], ['2', 'TOMASZ'], ['3', '73120905236'], ['5', 'PREZES'], ['6', 'NIE']], ['2', ['1', 'BOGACKI'], ['2', 'PRZEMYSLAW'], ['3', '67072600314'], ['5', 'WICEPREZES'], ['6', 'NIE']]]]], ['3', [['1', 'Przedmiot dzialalnosci'], ['1', ['1', ['22', '1'], 'DZIALALNOSC WYDAWNICZA']], ['2', ['1', ['22', '2'], 'DZIALALNOSC POLIGRAFICZNA']], ['3', ['1', ['22', '3'], 'REPRODUKCJA ZAPISANYCH NOSNIKOW INFORMACJI']], ['4', ['1', ['51'], 'HANDEL HURTOWY I KOMISOWY, Z WYLACZENIEM HANDLU POJAZDAMI SAMOCHODOWYMI, MOTOCYKLAMI']], ['5', ['1', ['52'], 'HANDEL DETALICZNY, Z WYLACZENIEM SPRZEDAZY POJAZDOW SAMOCHODOWYCH, MOTOCYKLI; NAPRAWA ARTYKULOW UZYTKU OSOBISTEGO I DOMOWEGO']], ['6', ['1', ['55'], 'HOTELE I RESTAURACJE']], ['7', ['1', ['63', '3'], 'DZIALALNOSC ZWIAZANA Z TURYSTYKA']], ['8', ['1', ['70'], 'OBSLUGA NIERUCHOMOSCI']], ['9', ['1', ['71', '40', 'Z'], 'WYPOZYCZANIE ARTYKULOW UZYTKU OSOBISTEGO I DOMOWEGO']], ['10', ['1', ['74', '8'], 'DZIALALNOSC KOMERCYJNA GDZIE INDZIEJ NIESKLASYFIKOWANA']], ['11', ['1', ['85', '14', 'A'], 'DZIALALNOSC FIZJOTERAPEUTYCZNA']], ['12', ['1', ['85', '14', 'D'], 'DZIALALNOSC PSYCHOLOGICZNA I PSYCHOTERAPEUTYCZNA']], ['13', ['1', ['85', '14', 'E'], 'DZIALALNOSC PARAMEDYCZNA']], ['14', ['1', ['85', '14', 'F'], 'DZIALALNOSC ZWIAZANA Z OCHRONA ZDROWIA LUDZKIEGO POZOSTALA, GDZIE INDZIEJ NIESKLASYFIKOWANA']], ['15', ['1', ['93', '04', 'Z'], 'DZIALALNOSC ZWIAZANA Z POPRAWA KONDYCJI FIZYCZNEJ']], ['16', ['1', ['93', '05', 'Z'], 'DZIALALNOSC USLUGOWA POZOSTALA, GDZIE INDZIEJ NIESKLASYFIKOWANA']]]]]

frame_list =  [frame_e1, frame_e2, frame_e3, frame_e4, frame_e5, frame_e6, frame_e7, frame_e8, frame_e9, frame_e10, frame_e11, frame_e12]

def eco_type(dobject):
        if dobject['body']['1']['1']['1']['1'] == 'SPOLKA AKCYJNA':
                return(SpAkc(dobject))
        elif dobject['body']['1']['1']['1']['1'] == 'SPOLKA KOMANDYTOWA':
                return(SpKom(dobject))
        elif dobject['body']['1']['1']['1']['1'] == 'SPOLKA Z OGRANICZONA ODPOWIEDZIALNOSCIA':
                return(SpZoo(dobject))
        elif dobject['body']['1']['1']['1']['1'] == 'SPOLKA KOMANDYTOWO-AKCYJNA':
                return(SpKomAkc(dobject))
        elif dobject['body']['1']['1']['1']['1'] == 'FUNDACJA':
                return(Fund(dobject))
        elif dobject['body']['1']['1']['1']['1'] == 'STOWARZYSZENIE':
                return(Stow(dobject))
        elif dobject['body']['1']['1']['1']['1'] == 'SPOLDZIELNIA':
                return(Spol(dobject))
        elif dobject['body']['1']['1']['1']['1'] == 'ODDZIAL ZAGRANICZNEGO PRZEDSIEBIORCY':
                return(Zagr(dobject))
        elif dobject['body']['1']['1']['1']['1'] == 'SPOLKA JAWNA':
                return(SpJawna(dobject))
        else:
                exit()

def mem2csv_first(lobject, dirname='/home/ewarchul/MFParser2'):
        frame = lframe2dframe(lobject)
        temp = eco_type(frame)
        temp.fill_body(frame)
        temp.write_csv(dirname)
        print("Plik CSV utworzony.")

map(lambda x: mem2csv_first(x), frame_list)
