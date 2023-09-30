# X. Li 2023
import json
from dynamic.util import fixdir

class Config():
    '''Local file dir configurations:
        - cache dir: 
            - cached_events/    for user access
            - _temp/           for intermediate tasks
    '''
    def __init__(self):
        self.cache_address = 'cached_events'
        self._temp_address = '_temp'
        self._log_address = '_log'

        self._re_local_dir()

    def _re_local_dir(self):
        # refresh local directories
        dirs = [self.cache_address, self._temp_address, self._log_address]
        fixdir(dirs)

    # getter
    # ::user getter
    def get_cache_address(self):
        return self.cache_address
    
    def get_temp_address(self):
        return self._temp_address

    def get_log_address(self):
        return self._log_address

    # setter
    # ::user setter
    def set_cache_address(self, alt_cache):
        self.cache_address = alt_cache; self._re_local_dir()
    
    def set_temp_address(self, alt_temp):
        self._temp_address = alt_temp; self._re_local_dir()
    
    def set_log_address(self, alt_log):
        self._log_address = alt_log; self._re_local_dir()