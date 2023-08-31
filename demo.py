# X. Li 2023
# short demo
from gracedb_public.grace_configurations import Grace_config
from gracedb_public.local_configurations import Local_config
from dynamic.cache import _append_local_json
from dynamic.util import removedir
import os
client = Grace_config()

# show basic info
print('Server address: ', client.get_server(), '\n', 
    'Current graceid: ', client.get_graceid(), '\n',
    'Current file path: ', client.get_manual_path())

print('Local cache path: ', client.get_cache_address(), '\n', 
    'Local _temp path: ', client.get_temp_address())

# do not send too many requests; use responsibly
send_server_request = True
if send_server_request:
    # clear the local cached events
    try:
        os.remove(r'cached_events\local_superevents.json')
    except:
        pass
    # get an updated number of superevents
    max_count = client.get_superevents_count()
    print('Superevents max count: ', max_count)

    # update superevents
    client.update_superevents(count=50, wait_t=1)
    # get {count} most recent superevents, wait {wait_t} s per request

# initialize local configurations
local = Local_config()
local_content = local.get_myLocalDB()[client._get_superevents()]
# print(local_content)