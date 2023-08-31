# X. Li 2023
import json
from gracedb_public.shared_configurations import Config
from dynamic.util import fixdir

class Local_config(Config):
    '''Operate locally with cached_events data'''
    def __init__(self, myLocalDB=None):
        Config.__init__(self)
        self.localDB_title = 'local_superevents.json'
        self.localDB_path = '/'.join([self.cache_address, self.localDB_title])
        # self._re_localDB_path()

        if myLocalDB is not None:
            self.myLocalDb = myLocalDB
        else:
            
            try:
                with open(self.localDB_path,'r') as f:
                    
                    self.myLocalDb = json.load(f)
            except:
                print('No local superevent cache in',self.localDB_path)
                self.myLocalDb = None

    def _re_localDB_path(self):
        self.localDB_path = '/'.join([self.cache_address, self.localDB_title])

    # getter
    # ::user getter
    def get_myLocalDB(self):
        return self.myLocalDb
    
    def get_localDB_title(self):
        return self.localDB_title

    def get_localDB_path(self):
        return self.localDB_path

    # setter
    # ::user setter
    def set_myLocalDB(self, alt_db):
        self.myLocalDb = alt_db

    def set_localDB_title(self, alt_title):
        self.localDB_title = alt_title; self._re_localDB_path()
    

    

    

                
                
