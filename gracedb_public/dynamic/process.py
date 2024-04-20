# X. Li 2023
# system/Python-built-in dependencies
import  requests
import  json
import  os
from    typing          import Union

# gracedb_public custom dependencies
from    gracedb_public.dynamic.util         import re_punctuation, fixdir
from    gracedb_public.dynamic.cache        import cache_json, cache_file
from    gracedb_public.dynamic.logging      import logging
from    gracedb_public.\
                shared_configurations       import Config

@logging
def get_response_dict(url : str, cache_dir : str = None) -> dict:
    '''
    A wrapper for request.get() and saves the response in local directory.
    
    Parameters
    ----------
    url : str
        url to be requested
    cache_dir : str
        directory to store the response
    
    Returns
    -------
    data_dict
        response dictionary containing the requested data
    '''
    data_dict : dict = requests.get(url).json()

    # cache data
    if cache_dir is not None:
        fixdir(cache_dir)
        cache_json(data_dict, cache_dir, 
                    url.translate(re_punctuation())+'.json')

    return data_dict

@logging
def get_file(url            : Union[str, list[str]], 
             cache_dir      : str   = Config['files_address'],
             offline_mode   : bool  = Config['offline_mode'],
             local_files    : bool  = Config['local_files_first']
             ) -> dict[str, bool]:
    '''
    A wrapper for request.get() and saves the file in local directory
    
    Parameters
    ----------
    url : str
        url to be requested 
    cache_dir : str
        directory to store the file
    offline_mode : bool
        whether to enable offline mode
    local_files : bool
        whether to check local cache first

    Returns
    -------
    get_files_status
        status of the files
    '''
    file_urls = url if isinstance(url, list) else [str(url)]
    get_files_status = {}
    
    if cache_dir is not Config['files_address']:
        fixdir(cache_dir)
            
    for file_url in file_urls:
        file_url        : str  = str(file_url)
        file_title      : str  = str(file_url.translate(re_punctuation()))
        
        if offline_mode or local_files:
            # if offline mode or check local cache first options are enabled
            # check local cache first
            exists = if_cached(file_url, cache_dir)
            if exists:
                # if file exists in local cache, add True to status dict
                # and continue to the next file
                get_files_status[file_url] = True
                continue
            
            else: 
                if not offline_mode:
                    # if not offline_mode, and the file is not available locally
                    # try to get the file from the server by passing
                    pass
                
                elif offline_mode:
                    # if offline_mode, and the file is not available locally
                    # add False to status dict
                    get_files_status[file_url] = False
                    continue
        
        # if offline mode is not enabled and the file is not available locally
        # try to get the file from the server, add True to status dict
            
        file_content    : json = requests.get(file_url)
        
        get_files_status[file_title] = True

        # cache data
        cache_file(file_content, cache_dir, file_title)

    return get_files_status

def if_cached(url : str, cache_dir : str) -> bool:
    '''
    Check if the file is cached

    Parameters
    ----------
    url : str
        url to be checked
    cache_dir : str
        directory to check

    Returns
    -------
    bool
        whether the file is cached
    '''
    return os.path.exists(
            os.path.join(cache_dir, url.translate(re_punctuation())))