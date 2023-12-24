# X. Li 2023

def parse_dict( content_dict  : dict[str, str],
                levels : list[str] = ['superevents','links'], 
                event_key_all : bool = False) -> dict:
    '''parse the superevents json dictionary for information structure'''
    L1 = list(content_dict.keys())
    # expect ['numRows', 'superevents', 'links']

    L2 = list(content_dict[levels[0]][0].keys())
    if event_key_all:
        for label in content_dict[levels[0]]:
            for i in list(label.keys()):
                L2.append(i) if i not in L2 else L2
    # expect 'superevents':
    # ['superevent_id', 'gw_id', 'category', 'created', 'submitter', 
    # 'em_type', 't_start', 't_0', 't_end', 'far', 'time_coinc_far', 
    # 'space_coinc_far', 'labels', 'links', 'preferred_event_data']

    L3 = list(content_dict[levels[0]][0][levels[1]].keys())
    # expect 'links':
    # ['labels', 'logs', 'files', 'self', 'voevents', 'emobservations']

    return {'Database':L1, levels[0]:L2, levels[1]:L3}