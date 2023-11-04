# X. Li 2023
import json
from .dynamic.util import fixdir

Config : dict = {
        'cache_address'     :       'cached_events',
        'temp_address'      :       '_temp',
        '_log_address'      :       '_log'
            }

def _re_local_dir() -> None:
    # refresh local directories
    dirs : list = [
                cache_address, 
                _temp_address, 
                _log_address
            ]
    fixdir(dirs)

if __name__ == '__main__':
    _re_local_dir()