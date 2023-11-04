# X. Li 2023
import requests
import json

from gracedb_public.dynamic.util import re_punctuation, fixdir
from gracedb_public.dynamic.cache import cache_json, cache_file
from gracedb_public.dynamic.logging import logging

@logging
def get_response_dict(url : str, cache_dir : str = None) -> dict:
    '''A wrapper for request.get() and saves the response in local directory.'''
    files_list : dict = requests.get(url).json()

    # cache data
    if cache_dir is not None:
        fixdir(cache_dir)
        cache_json(files_list, cache_dir, 
                    url.translate(re_punctuation())+'.json')

    return files_list

@logging
def get_file(url : str, cache_dir : str = None) -> str:
    '''A wrapper for request.get() and saves the file in local directory'''
    file_content    : json = requests.get(url)
    file_title      : str = url.translate(re_punctuation())
    
    # cache data
    if cache_dir is not None:
        fixdir(cache_dir)
        cache_file(file_content, cache_dir, file_title)
    return file_title