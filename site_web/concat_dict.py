
## CONCATENATION OF DICT2 IN DICT1
def concat_dict_AND(dict1, dict2):
    dict_new = {}
    for name in dict1:
        if name in dict2:
            ## Add elem + occurences
            dict_new[name] =  dict1[name]
            dict_new[name][0] += dict2[name][0]
    return dict_new


## CONCATENATION OF DICT2 IN DICT1
def concat_dict_OR(dict1, dict2):
    dict_new = dict1
    for name in dict2:
        if name not in dict1:
            dict_new[name] = dict2[name]
        else:
            ## Add occurences
            dict_new[name][0] += dict2[name][0]
    return dict_new