# X. Li 2023
# short demo
import json 
import gracedb_public

from gracedb_public import dynamic
from gracedb_public.grace_configurations import Grace_config
from gracedb_public.local_configurations import Local_config
from gracedb_public.dynamic.cache import _append_local_json
from gracedb_public.dynamic.util import removedir
from gracedb_public.dynamic.parse import parse_dict
from gracedb_public.dynamic.process import get_response_dict, get_file

import os
client = Grace_config()

# show basic info
print('Server address: ', client.get_server(), '\n', 
    'Current graceid: ', client.get_graceid(), '\n',
    'Current file path: ', client.get_myFile_path())

print('Local cache path: ', client.get_cache_address(), '\n', 
    'Local _temp path: ', client._get_temp_address())

# do not send too many requests; use responsibly
send_server_request = False
if send_server_request:
    # clear the local cached events
    try:
        os.remove(r'cached_events\local_superevents.json')
    except:
        pass
    # get an updated number of superevents
    # max_count = client.server_get_superevents_count()
    # print('Superevents max count: ', max_count)

    # update superevents
    client.server_update_superevents(count=50, wait_t=1)
    # get {count} most recent superevents, wait {wait_t} s per request

local_content = client.get_myLocalDB()
# parse the database dictionary and print a summary of the dictionary
levels = [client._get_superevents_key(), client._get_links_key()]
dbProperty = parse_dict(local_content, 
                    levels=levels, 
                    event_key_all=False)
print(json.dumps(dbProperty, indent=4))

# get the first 5 event ids in the database
events = client.get_events_list(chunk=5)
print(events)

# check all links of the first superevent in the local database
links = client.get_event_links_list()
print(links)

# check the file link of the first superevent in the local database
file_link = client.get_event_files_path()
print(file_link)
    
# dictionary of files available
files_list = get_response_dict(file_link, 
            cache_dir='/'.join([client.get_files_address()]))
print(json.dumps(files_list, indent=4))

# save the bayestar.multiorder.fits,1 file
get_file(files_list['bayestar.multiorder.fits,1'], 
            cache_dir='/'.join([client.get_files_address()]))