import json

def dict_decoder(bainry_dict):
    data = {}
    for k,v in bainry_dict:
        data[k.dcode("utf_8")] = json.loads(v)
    return data