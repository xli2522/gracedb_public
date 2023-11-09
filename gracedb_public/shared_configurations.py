# X. Li 2023
from .dynamic.util import fixdir

''' Shared (system-wide) file structure configurations
        ie: Config  -> cache, temp, _log, files addresses
                    -> local DB file name
                    -> server address
                    -> environment modes
                    -> database structure keys
                    -> data parsing setting
    ---------
    Should import/read in read-only
'''

Config : dict[str, any] = {
        # ::local file structure
        'cache_address'     :       'cached_events',
        'files_address'     :       'cached_events/files',
        '_temp_address'     :       '_temp',
        '_log_address'      :       '_log',
        
        # ::local DB title
        'localDB_title'     :       'local_superevents.json',
        
        # ::server access setting
        'server'            :       'https://gracedb.ligo.org/api',

        # ::environment mode
        'offline_mode'      :       False,

        # ::grace/local database structure setting
        # dictionary keys below; should not be changed
        'superevents'       :       'superevents',
        'event_id'          :       'superevent_id',
        'links'             :       'links',
        'files'             :       'files',

        # ::data parsing setting
        'inquiry_chunk'     :       15      # -> 15 items in drop down menu
        }

def _re_local_dir() -> None:
    # refresh local directories
    dirs : list = [
                Config[ 'cache_address'  ], 
                Config[ 'files_address'  ], 
                Config[ 'temp_address'   ], 
                Config[ '_log_address'   ]
            ]
    fixdir(dirs)

if __name__ == '__main__':
    '''set up local directories'''
    _re_local_dir()