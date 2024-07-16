# X. Li 2024
# This file contains functions for updating local cached events
# 
# More on this: some events and their associated files are removed from the
# server after a certain period of time. To keep the local demo database 
# up-to-date, the local cached demo events should be updated when needed.

# gracedb_public dependencies
from gracedb_public.grace_configurations import Grace_config

if __name__ == '__main__':

    Grace_config().clear_db_cache()     # should see a warning message
    Grace_config().server_update_superevents(count=100, wait_t=1)

