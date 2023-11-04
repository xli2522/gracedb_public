# X. Li 2023
import functools
from datetime import datetime
import os

from gracedb_public.shared_configurations import Config
from gracedb_public.dynamic.util import fixdir

def logging(func : object) -> any:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> any:
        # Log the function name and arguments
        fixdir(Config['_log_address'])
        file_path : str = '/'.join([Config['_log_address'], 'log.txt'])
        mode      : str = 'a'
        # limit logging content to 100 char
        args_short      : str = ' '.join(map(str, args))[:100]
        kwargs_short    : str = ' '.join(map(str, kwargs))[:100]

        # log function name, time, and inputs
        if not os.path.isfile(file_path): mode = 'w'
        with open(file_path, str(mode)) as log_file:
            log_file.write(f'{datetime.now()}  {func.__name__}\n\
args: {args_short}\nkwargs: {kwargs_short}\n')

        # Call the original function
        return func(*args, **kwargs)
    return wrapper