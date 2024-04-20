# X. Li 2023
import json
import warnings
import os
from typing import Union, Optional

from gracedb_public.shared_configurations import Config, _re_local_dir

from gracedb_public.dynamic import util, cache

class Local_config(object):
    ''' Local database configurations (the parent of Grace Config).
        -> Grace_configurations(Local_config)
    ---------
        Contains all local database and file access information.
        Deals with accessing local database and files.
        Methods for refreshing, re-ordering database, and files.
    ---------
        DB_load_success True if loaded successfully, False otherwise. 
    '''

    def __init__(self) -> None:
        ''' Load local database.
        ---------
            NOTE:   DB_load_success True/False indicating 
                    if the local database was loaded.
        '''
        # ::local database title
        self.localDB_title          : str = Config['localDB_title']
        # ::local file structure
        self.cache_address          : str = Config['cache_address']
        self.files_address          : str = Config['files_address']
        self._temp_address          : str = Config['_temp_address']
        # ::local default inquiry chunk size
        self.local_inquiry_chunk    : int = Config['inquiry_chunk']
        self._re_inquiry_position()
        
        # ::database parsing keys
        self._superevents_key       : str = Config['superevents']
        self._event_id_key          : str = Config['event_id']
        self._links_key             : str = Config['links']
        self._files_key             : str = Config['files']
        
        # set up local directories
        _re_local_dir()             # Config function
        
        # load database content
        self._re_my_localDB()        
        
        # other sessional variables
        self._warn_skips = (os.path.dirname(__file__),)      # for warnings.warn()
        
    # ::content/path refresh below
    def _re_localDB_path(self) -> None:
        ''' Refresh local database path.
        ---------
            Modified:   localDB_path
                        -> (new cache dir / new DB title)
        ---------
            NOTE:   temporary sessional DB path change, 
                    will not affect system settings.
        '''
        self.localDB_path : str = '/'.join([self.cache_address, 
                                            self.localDB_title]
                                        )

    def _re_my_localDB(self) -> bool:
        ''' Refresh current local DB content.
        ---------
            Modified:   myLocalDB
                        -> new DB .json content in dict
        ---------
            Return True if loaded successfully, False otherwise.
        '''
        self._re_localDB_path()
        try:
            with open(self.localDB_path,'r') as f:
                self.myLocalDB      : dict = json.load(f)
            self.DB_load_success    : bool = True              # successful

        except:
            print('No superevent cache in ', self.localDB_path)
            self.myLocalDB          : dict = None           # unsuccessful
            self.DB_load_success    : bool = False
        return self.DB_load_success       
   
    def _re_inquiry_position(self) -> None:
        ''' Refresh current inquiry position and inquiry chunk.
        ---------
            Modified:   inquiry_start_position
                        -> reset to 0
                        local_inquiry_chunk
                        -> reset to default Config setting
        '''
        self.local_inquiry_chunk    : int = Config['inquiry_chunk']
        self.inquiry_start_position : int = 0

    def _sort_localDB(self, 
                      db_key : Optional[str] = None) -> None:
        ''' Sort local database by db_key.
        ---------
            Modified:   myLocalDB
                        -> sorted by db_key
        '''
        if db_key is None: db_key = self._event_id_key
        self.myLocalDB[self._superevents_key].sort(
            key=lambda x: x[str(db_key)], reverse=True)
        
        # save sorted database in _temp directory before overwriting in cache
        cache.cache_json(self.myLocalDB, self._temp_address, self.localDB_title)
        # save in cache
        cache.cache_json(self.myLocalDB, self.cache_address, self.localDB_title)
        # remove _temp local DB if successful
        os.remove('/'.join([self._temp_address, self.localDB_title]))
            
    # Database variable getters and setters 
    # getter ---------------------------------------------
    # ::user getter
    def get_DB_load_status(self)-> bool:
        '''return initial database loading status'''
        return self.DB_load_success
    
    def get_myLocalDB(self) -> dict:
        '''return local database content'''
        return self.myLocalDB
    
    def get_localDB_title(self) -> str:
        '''return local database file name'''
        return self.localDB_title

    def get_localDB_path(self) -> str:
        '''return local database path'''
        return self.localDB_path
    
    def get_inquiry_position(self) -> int:
        '''return inquiry start position'''
        return self.inquiry_start_position

    def get_local_inquiry_chunk(self) -> int:
        '''return local inquiry chunk'''
        return self.local_inquiry_chunk
    
    # ::internal getter ------------------------------------
    def _get_cache_address(self) -> str:
        '''return cache address'''
        return self.cache_address
    
    def _get_files_address(self) -> str:
        '''get current files_address'''
        return self.files_address
    
    # ::internal database keys
    def _get_superevents_key(self) -> str:
        '''get current database superevents key'''
        return self._superevents_key 
    
    def _get_links_key(self) -> str:
        '''get current database links key'''
        return self._links_key 
    
    def _get_files_key(self) -> str:
        '''get current database files key'''
        return self._files_key 
    
    def _get_event_id_key(self) -> str: 
        '''get current database event id key'''
        return self._event_id_key
    
    
    # setter ---------------------------------------------
    # ::user setter
    def set_localDB_title(self, alt_title : str) -> None:
        ''' Set local database titile/name; refresh local database path.
        ---------
            NOTE:   Temporary sessional DB path change, 
                    will not affect system settings.
        '''
        self.localDB_title = alt_title; self._re_localDB_path()
    
    def set_inquiry_position(self, alt_pos : int) -> None:
        ''' Set current inquiry position.
        ---------
            NOTE:   Temporary inquiry position change,
                    will be set to 0 once _re_inquiry_position() is called.
        '''
        self.inquiry_start_position = alt_pos

    def set_local_inquiry_chunk(self, alt_chunk : int) -> None:
        ''' Set current inquiry chunk.
            -> allow user toggle
        ---------
            NOTE:   Temporary inquiry chunk change,
                    will be set to default value once 
                    _re_inquiry_position() is called.
        '''
        self.local_inquiry_chunk = alt_chunk

    # ::internal setter ------------------------------------
    def _set_myLocalDB(self, alt_db : dict) -> None:
        ''' Replace local database content.
            -> replace entire loaded .json database object
        ---------
            NOTE:   Expects database loaded .json dict content object.
        '''
        self.myLocalDB = alt_db
        
    def _set_cache_address(self, alt_address : str) -> None:
        '''set sessional cache address'''
        self.cache_address = alt_address; self._re_localDB_path()
    
    def _set_files_address(self, alt_address : str) -> None:
        '''set sessional files address'''
        self.files_address = alt_address
         
    def _set_superevents_key(self, alt_key : str) -> None:
        '''set sessional superevents key; should not be changed'''
        self._superevents_key = alt_key; self._re_manual_path()
        
    def _set_links_key(self, alt_key : str) -> None:
        '''set sessional superevents links key; should not be changed'''
        self._links_key = alt_key; self._re_manual_path()
        
    def _set_files_key(self, alt_key : str) -> None:
        '''set sessional superevents files key; should not be changed'''
        self._files_key = alt_key; self._re_manual_path()
        

    # Database content getters
    # getter ---------------------------------------------
    # ::user getter
    # NOTE: considering the small number of items this program gets,
    #       use lists when possible for simplicity.
    def get_events_list(self, start : int = 0, chunk  : int = 15) -> list:
        ''' get events list from int(start) to int(start+chunk)
        ---------
            Return selected event id list
        '''
        out         : list = []
        selected    : dict = self.myLocalDB[
                                self._superevents_key][start:start+chunk]
        for i in selected: out.append(i[self._event_id_key])
        return out
    
    def get_event_links_list(self, ordered_event_id : int = 0) -> list:
        ''' get event links list
        ---------
            Return selected list
        '''
        selected    : dict = self.myLocalDB[self._superevents_key][
                                            ordered_event_id][
                                            self._links_key].keys()
        return list(selected)
    
    def get_event_files_path(self, ordered_event_id : int = 0) -> str:
        ''' get event files path
        ---------
            Return files api path for specified event id.
        '''
        selected    : str = self.myLocalDB[ self._superevents_key][
                                            ordered_event_id][
                                            self._links_key][
                                            self._files_key]
        return selected
    
    def get_event_dict(self, ordered_event_id : int = 0) -> dict:
        ''' get all event dict content
        ---------
            Return full event dictionary content
        '''
        return self.myLocalDB[ self._superevents_key][ordered_event_id]
    
    # def _get_event_files_list(self) -> list:
    # only responsible for checking local files
    #     return list

    # clean and clear ---------------------------------------------
    # ::user clear
    def clear_db_cache(self) -> None:
        ''' clear all cached databases, use with caution'''
        warnings.warn('clear all cached databases', 
                      stacklevel=2)
        util.removedir(self.cache_address)

    def clear_files(self) -> None:
        ''' clear all locally stored files, use with caution'''
        warnings.warn('clear all files',
                      stacklevel=2)
        util.removedir(self.files_address)
        
    def clear_logs(self) -> None:
        ''' clear all locally generated logs, use with caution'''
        warnings.warn('clear all logs',
                      stacklevel=2)
        util.removedir(self._log_address)
        
    # Database status/statistics getters
    # getter ---------------------------------------------
    # ::user getter
    def get_localDB_size(self) -> float:
        ''' get local database size
        ---------
            Return local database size in MB
        '''
        return util.getSize(self.localDB_path)
    
    def get_local_file_size(self) -> float:
        ''' get local file size
        ---------
            Return local file size in MB
        '''
        return util.get_dirSize(self.files_address)
    
    def get_local_number_of_files(self) -> int:
        ''' get local number of files
        ---------
            Return local number of files
        '''
        return util.getNumberofFiles(self.files_address)
    
    def get_localDB_number_of_events(self) -> int:
        ''' get local number of events
        ---------
            Return local number of events
        '''
        return len(self.myLocalDB[self._superevents_key])
    