# X. Li 2023
import json
from .dynamic.util import fixdir

'''Shared (system-wide) file structure configurations
        ie: Config  -> cache, temp, and _log addresses
                    -> server addresses
                    -> environment modes
    should import/read in read-only
'''

Config : dict[str, any] = {
        # ::local file structure
        # directory names below
        'cache_address'     :       'cached_events',
        'files_address'     :       'cached_events/files',
        '_temp_address'     :      '_temp',
        '_log_address'      :       '_log',
        
        # ::local DB title
        'localDB_title'     :       'local_superevents.json',
        
        # ::server access setting
        'offline_mode'      :       False,
        'server'            :       'https://gracedb.ligo.org/api',

        # ::grace/local database structure setting
        # dictionary keys below; should not be changed
        'superevents'       :       'superevents',
        'links'             :       'links',
        'files'             :       'files'

        }

def _re_local_dir() -> None:
    # refresh local directories
    dirs : list = [
                Config['cache_address'], 
                Config['files_address'], 
                Config['temp_address'], 
                Config['_log_address']
            ]
    fixdir(dirs)

if __name__ == '__main__':
    _re_local_dir()