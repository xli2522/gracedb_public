# X. Li 2023

import requests
import time

from tqdm import tqdm

from gracedb_public.shared_configurations import Config
from gracedb_public.local_configurations import Local_config
from gracedb_public.dynamic.cache import cache_json, _append_local_json
from gracedb_public.dynamic.util import re_punctuation, fixdir, removedir
from gracedb_public.dynamic.logging import logging

class Grace_config(Local_config):
    '''Communicate with GraceDB for updated information'''
    def __init__(self, server : str='https://gracedb.ligo.org/api') -> None:
        self._server        : str = server
        self._inquiry_chunk : int = 30        # slow to no server response 
                                        # for larger chunk size; do not change
        # determine with https://gracedb.ligo.org/apiweb/
        # publicly accessible api methods only
        self._superevents   : str = 'superevents'

        # manual dir names
        self._graceid       : str = '{graceid}'
        self._files         : str = 'files'
        self._myFile        : str = '{myFile}'

        self._re_manual_path()          

        # initialize file structure config   
        self.local_config = Local_config()

    def _re_manual_path(self) -> None:
        # refresh manual api path
        self._manual_path = '/'.join([self._server, self._superevents,
        self._graceid, self._files, self._myFile])

    # getter
    # ::user getter
    def get_server(self) -> str:
        return self._server

    def get_myFiles(self) -> str:
        return self._myFile
    
    def get_graceid(self) -> str:
        return self._graceid
    
    def get_manual_path(self) -> str:
        return self._manual_path

    # ::internal getter
    def _get_superevents(self) -> str:
        return self._superevents
    
    def _get_cache_address(self) -> str:
        return Config['cache_address']
    
    def _get_temp_address(self) -> str:
        return Config['temp_address']

    def _get_log_address(self) -> str:
        return Config['_log_address']
    
    # setter
    # ::user setter
    def set_server(self, alt_server : str) -> None:
        self._server = alt_server; self._re_manual_path()

    def set_myFiles(self, alt_label : str) -> None:
        self._myFiles = alt_label; self._re_manual_path()
    
    # ::internal setter
    def _set_superevents(self, alt_superLabel : str) -> None:
        self._superevents = alt_superLabel; self._re_manual_path()

    def _set_files(self, alt_filesLabel : str) -> None:
        self._files = alt_filesLabel; self._re_manual_path()
        
    # other methods;
    # all variables refering to properties of the gracedb server daatabase
    # if not specified otherwise

    @logging
    def get_superevents_count(self) -> int:
        '''get the superevents total count by making one superevents request'''
        # Method 1:
        # superevents_count_info = requests.get(
        # '/'.join([self._server, self._superevents,'?count=1'])
        # ).json()['links']
        # last_url = superevents_count_info['last']
        # idx1 = last_url.index('start=')
        # idx2 = last_url.index('&count=')
        # superevents_count = int(float(last_url[idx1+len('start='): idx2]))

        # Method 2:
        superevents_count : str = requests.get(
        '/'.join(
            [self._server, self._superevents,'?count=1'])
            ).json()['numRows']
        return int(superevents_count)
    
    # NOTE: [FEATURE] sleep dec?
    @logging
    def update_superevents(self, 
                           start  : int = None, 
                           count  : int = None, 
                           wait_t : [int, float] = 0) -> None:
        '''get updated superevents information from gracedb server'''
        max_count : int = self.get_superevents_count()
        if isinstance(count, (int, float)) and count <= max_count:
            count = int(count)
        else: count = max_count

        if isinstance(start, (int, float)) and start + count <= max_count:
            start = int(start)
        else: start = 0

        # NOTE: [FEATURE] pack chunked requests?
        inquiry_remain  : int = count
        itr_round       : int = 0           # saves else condition
        temp_dir        : str = '/'.join([self._get_temp_address(), 
                                            str(time.time())])
        fixdir(temp_dir)
        if count > self._inquiry_chunk:
            inquiry_round, inquiry_remain = divmod(count,
                                                    self._inquiry_chunk)
            
            for itr_round in tqdm(range(0, inquiry_round), 
                                    desc='Superevents request chunks: '):
                api_path : str = '/'.join(
                [self._server, self._superevents,
                '?start='+str(start+itr_round*self._inquiry_chunk)+ \
                '&count='+str(self._inquiry_chunk)])
                time.sleep(wait_t)

                temp_superList : object = requests.get(api_path).json()
                cache_json(temp_superList, 
                    temp_dir, api_path.translate(re_punctuation())+'.json')

                # append to local
                _temp_content_path = '/'.join([temp_dir, 
                        api_path.translate(re_punctuation())+'.json'])
                _append_local_json(_temp_content_path, 
                                    self.local_config.get_localDB_path(), 
                                    self._get_superevents())
            itr_round+=1
        api_path = '/'.join(
            [self._server, self._superevents,
            '?start='+str(start+itr_round*self._inquiry_chunk)+ \
            '&count='+str(inquiry_remain)])
        temp_superList = requests.get(api_path).json()
        cache_json(temp_superList, 
                    temp_dir, api_path.translate(re_punctuation())+'.json')
        
        # append to local
        _temp_content_path = '/'.join([temp_dir, 
                api_path.translate(re_punctuation())+'.json'])
        _append_local_json(_temp_content_path, 
                            self.local_config.get_localDB_path(), 
                            self._get_superevents())
        removedir(temp_dir)

        return 