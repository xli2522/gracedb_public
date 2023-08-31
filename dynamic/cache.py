# X. Li 2023
import requests
import json
import time
import os
import pandas as pd

def cache_json(content, parent_path, title):
    '''store content in temporary cache parent_path with title'''
    with open('/'.join([parent_path, title]),'w') as out:
        json.dump(content, out)

def _append_local_json(content_path, target_path, index):
    '''add json content to another json file'''
    if os.path.isfile(target_path) and os.stat(target_path).st_size!=0:
        with open(target_path,'r') as previous:
            previous_content = json.load(previous)      # dic
        with open(content_path, 'r') as myJson:
            content = json.load(myJson)[index]          # list

        with open(target_path,'w+') as out:
            previous_content[index]+=content
            json.dump(previous_content, out)

    elif not os.path.isfile(target_path) or os.stat(target_path).st_size==0:
        with open(content_path, 'r') as myJson:
            content = json.load(myJson)
        with open(target_path,'w+') as out:
            json.dump(content, out)
    else:
        raise Warning('Conditions went wrong.. Will fix..')
    return