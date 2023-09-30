# X. Li 2023
import functools
from datetime import datetime
import os

from gracedb_public.shared_configurations import Config
from dynamic.util import fixdir

shared_config = Config()

def logging(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Log the function name and arguments
        fixdir(shared_config.get_log_address())
        file_path = '/'.join([shared_config.get_log_address(), 'log.txt'])
        mode = 'a'
        # limit logging content to 100 char
        args_short = ' '.join(map(str, args))[:100]
        kwargs_short = ' '.join(map(str, kwargs))[:100]

        # log function name, time, and inputs
        if not os.path.isfile(file_path): mode = 'w'
        with open(file_path, str(mode)) as log_file:
            log_file.write(f'{datetime.now()}  {func.__name__}\n\
args: {args_short}\nkwargs: {kwargs_short}\n')

        # Call the original function
        result = func(*args, **kwargs)
        return result
    return wrapper