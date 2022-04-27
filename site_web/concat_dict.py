
## CONCATENATION OF DICT2 IN DICT1
def concat_dict_ET(dict1, dict2):
    for name in dict2:
        if name in dict1:
            ## Add occurences
            dict1[name][0] += dict2[name][0]

## CONCATENATION OF DICT2 IN DICT1
def concat_dict_OU(dict1, dict2):
    for name in dict2:
        if name not in dict1:
            dict1[name] = dict2[name]
        else:
            ## Add occurences
            dict1[name][0] += dict2[name][0]