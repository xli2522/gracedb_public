# X. Li 2023
import json
from gracedb_public.shared_configurations import Config

class Local_config():
    ''' Local database configurations
        Return True if loaded successfully, False otherwise. '''
    def __init__(self) -> bool:
        '''return True/False indicating if the local database was loaded'''
        self.localDB_title : str = Config['localDB_title']
        self.cache_address : str = Config['cache_address']
        self._re_localDB_path()          # refresh database path
        self._re_my_localDB()            # load database content

    
    # ::content/path refresh below
    def _re_localDB_path(self) -> None:
        ''' refresh local database path
            Modified variable: localDB_path
            NOTE:   temporary sessional DB path change, 
                    will not affect system settings.
        '''
        self.localDB_path : str = '/'.join([self.cache_address, 
                                            self.localDB_title]
                                        )

    def _re_my_localDB(self) -> bool:
        ''' refresh current local DB content
            Modified variable: myLocalDB
            Return True if loaded successfully, False otherwise.
        '''
        load_status = False
        try:
            with open(self.localDB_path,'r') as f:
                self.myLocalDB = json.load(f)
            load_status = True              # successful

        except:
            print('No superevent cache in ', self.localDB_path)
            self.myLocalDB = None           # unsuccessful
            
        return load_status           
        
    # getter
    # ::user getter
    def get_myLocalDB(self) -> json:
        '''return local database content'''
        return self.myLocalDB
    
    def get_localDB_title(self) -> str:
        '''return local database file name'''
        return self.localDB_title

    def get_localDB_path(self) -> str:
        '''return local database path'''
        return self.localDB_path
    
    # internal getter
    def _get_cache_address(self) -> str:
        '''return cache address'''
        return self.cache_address

    # setter
    # ::user setter
    def set_myLocalDB(self, alt_db : json) -> None:
        ''' replace local database content
            NOTE:   - this is not the database name or path, 
                        it expects database content object.
                    - temporary sessional DB path change, 
                        will not affect system settings.
        '''
        self.myLocalDB = alt_db

    def set_localDB_title(self, alt_title : str) -> None:
        ''' set local database titile/name; refresh local database path
            NOTE:   temporary sessional DB path change, 
            will not affect system settings.
        '''
        self.localDB_title = alt_title; self._re_localDB_path()
    
    # internal setter
    def _set_cache_address(self, alt_address : str) -> None:
        '''set sessional cache address'''
        self.cache_address = alt_address; self._re_localDB_path()
    

    

    

                
                
