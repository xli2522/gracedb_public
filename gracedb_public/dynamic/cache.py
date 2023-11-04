# X. Li 2023
import json
import os

from gracedb_public.dynamic.logging import logging

# default json indentation = 4
@logging
def cache_json(content : json, parent_path : str, title : str) -> None:
    '''store content in cache parent_path with title'''
    with open('/'.join([parent_path, title]),'w') as out:
        json.dump(content, out, indent=4)
    return

def _append_local_json(content_path : str, 
                       target_path  : str, 
                       index        : str) -> None:
    '''add json content to another json file'''
    if os.path.isfile(target_path) and os.stat(target_path).st_size!=0:
        with open(target_path,'r') as previous:
            previous_content = json.load(previous)      # dict
        with open(content_path, 'r') as myJson:
            content = json.load(myJson)[index]          # list

        with open(target_path,'w+') as out:
            previous_content[index]+=content
            json.dump(previous_content, out, indent=4)

    elif not os.path.isfile(target_path) or os.stat(target_path).st_size==0:
        with open(content_path, 'r') as myJson:
            content = json.load(myJson)
        with open(target_path,'w+') as out:
            json.dump(content, out, indent=4)
    else:
        raise Warning('Conditions went wrong.. Will fix..')
    return

@logging
def cache_file(content : json, parent_path : str, title : str) -> None:
    '''store file in cache parent_path with title'''
    open('/'.join([parent_path, title]), 'wb').write(content.content)
    return