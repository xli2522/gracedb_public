# X. Li 2023
import requests

from dynamic.util import re_punctuation, fixdir
from dynamic.cache import cache_json, cache_file

def get_response_dict(url, cache_dir=None):
    '''A wrapper for request.get() and saves the response in local directory.'''
    files_list = requests.get(url).json()

    # cache data
    if cache_dir is not None:
        fixdir(cache_dir)
        cache_json(files_list, cache_dir, 
                    url.translate(re_punctuation())+'.json')

    return files_list

def get_file(url, cache_dir=None):
    '''A wrapper for request.get() and saves the file in local directory'''
    file_content = requests.get(url)
    
    # cache data
    if cache_dir is not None:
        fixdir(cache_dir)
        cache_file(file_content, cache_dir, 
                    url.translate(re_punctuation()))
    return file_content