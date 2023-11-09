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
    ''' GraceDB database configurations (both server and local)
        Grace_config --> user and server interactions
        Grace_config is based on Local_config
    ---------    
        Initializes local configurations automatically.
    ---------
    Details:
        Server interaction part --> obtain local copies of the database
        Local  interaction part --> access and process data
    '''
    def __init__(self) -> None:
        super().__init__()
        # ::server interaction settings
        self._offline_mode          : bool = Config['offline_mode']
        self._server                : str  = Config['server']
        
        self._server_inquiry_chunk  : int = 30
        # slow to no server response for larger chunk size; do not change
        # determine with https://gracedb.ligo.org/apiweb/
        # publicly accessible api methods only

        # ::local _log, _temp interaction settings
        # NOTE: these directory methods were not included in Local_config
        # as they are not part of the GraceDB database
         
        # directory names; should not be changed
        self._temp_address  : str = Config['_temp_address']
        self._log_address   : str = Config['_log_address']

        # ::database parsing related; dynacmic
        self.graceid                : str = '{graceid}'
        self.ordered_event_id       : int = 0
        self.myFile                 : str = '{myFile}'
        
        self._re_myFile_path()

    def _re_myFile_path(self) -> None:
        '''refresh api path to myFile'''
        self._myFile_path = '/'.join([  self._server, 
                                        super()._get_superevents_key(),
                                        self.graceid, 
                                        super()._get_files_key(), 
                                        self.myFile]
                                )


    # getter
    # ::user getter
    # current event and file information
    def get_server(self) -> str:
        '''reutrn the current server address'''
        return self._server
    
    def get_graceid(self) -> str:
        '''return the current event id'''
        return self.graceid
    
    def get_myFile(self) -> str:
        '''return the current file name/title'''
        return self.myFile
    
    def get_myFile_path(self) -> str:
        '''return the current file path'''
        return self._myFile_path

    # current local file structure directories
    def get_cache_address(self) -> str:
        '''get current cache_address
        Wrapper for Local_config internal method _get_cache_address'''
        return super()._get_cache_address()
    
    def get_files_address(self) -> str:
        '''get current files_address
        Wrapper for Local_config internal method _get_files_address'''
        return super()._get_files_address()
    
    # ::internal getter 
    # internal current local file structure directories
    def _get_temp_address(self) -> str:
        '''get current temp address'''
        return self._temp_address

    def _get_log_address(self) -> str:
        '''get current log address'''
        return self._log_address
    
    # setter
    # ::user setter
    def set_server(self, alt_server : str) -> None:
        '''set sessional api server address'''
        self._server = alt_server; self._re_myFile_path()

    def set_myFile(self, alt_title : str) -> None:
        '''set myFile name/title; refresh file path'''
        self.myFile = alt_title; self._re_myFile_path()
    
    # ::internal setter
    # internal set database key

    # internal event and file information
    def _set_myFile_path(self, alt_path : str) -> None:
        ''' set temporary path to current file; should not use 
            Will be used when local cache check and update function is enabled.
        ---------
            NOTE:   updating file path should be done through refresh
                    myFile path function not set myFile path.
        '''
        self._myFile_path = alt_path
        
    
    # ::other methods;
    # all variables refering to properties of the gracedb server daatabase
    # if not specified otherwise

    # ::server communications and local DB update
    @logging
    def server_get_superevents_count(self) -> int:
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
            [self._server, self._superevents_key,'?count=1'])
            ).json()['numRows']
        return int(superevents_count)
    
    # NOTE: [FEATURE] sleep dec?
    @logging
    def server_update_superevents(self, 
                           start  : int = None, 
                           count  : int = None, 
                           wait_t : [int, float] = 1) -> None:
        '''get updated superevents information from gracedb server'''
        max_count : int = self.server_get_superevents_count()
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
        if count > self._server_inquiry_chunk:
            inquiry_round, inquiry_remain = divmod(count,
                                                    self._server_inquiry_chunk)
            
            for itr_round in tqdm(range(0, inquiry_round), 
                                    desc='Superevents request chunks: '):
                api_path : str = '/'.join(
                [self._server, super()._get_superevents_key(),
                '?start='+str(start+itr_round*self._server_inquiry_chunk)+ \
                '&count='+str(self._server_inquiry_chunk)])
                time.sleep(wait_t)

                temp_superList : object = requests.get(api_path).json()
                cache_json(temp_superList, 
                    temp_dir, api_path.translate(re_punctuation())+'.json')

                # append to local
                _temp_content_path = '/'.join([temp_dir, 
                        api_path.translate(re_punctuation())+'.json'])
                _append_local_json(_temp_content_path, 
                                    super().get_localDB_path(), 
                                    super()._get_superevents_key())
            itr_round+=1
        api_path = '/'.join(
            [self._server, super()._get_superevents_key(),
            '?start='+str(start+itr_round*self._server_inquiry_chunk)+ \
            '&count='+str(inquiry_remain)])
        temp_superList = requests.get(api_path).json()
        cache_json(temp_superList, 
                    temp_dir, api_path.translate(re_punctuation())+'.json')
        
        # append to local
        _temp_content_path = '/'.join([temp_dir, 
                api_path.translate(re_punctuation())+'.json'])
        _append_local_json(_temp_content_path, 
                            super().get_localDB_path(), 
                            super()._get_superevents_key())
        removedir(temp_dir)

        return
    
    ######################################################################
    # Database content getters
    # Wrapper
    # getter ---------------------------------------------
    # ::user getter
    def get_events_list(self, start : int = 0, chunk  : int = 15) -> list:
        ''' get events list from int(start) to int(start+chunk)
        ---------
            Return selected event id list
        ---------
            Wrapper for Local_config internal method get_events_list
        '''
        return super().get_events_list(start, chunk)
    
    def get_event_links_list(self, ordered_event_id : int = 0) -> list:
        ''' get event links list
        ---------
            Return selected list
        ---------
            Wrapper for Local_config internal method get_event_links_list
        '''
        return super().get_event_links_list(ordered_event_id)
    
    def get_event_files_path(self, ordered_event_id : int = 0) -> str:
        ''' get event files path
        ---------
            Return files api path for specified event id.
        ---------
            Wrapper for Local_config internal method get_event_files_path
        '''
        return super().get_event_files_path(ordered_event_id)
    
    def get_event_dict(self, ordered_event_id : int = 0) -> dict:
        ''' get all event dict content
        ---------
            Return full event dictionary content
        ---------
            Wrapper for Local_config internal method get_event_dict
        '''
        return super().get_event_dict(ordered_event_id)