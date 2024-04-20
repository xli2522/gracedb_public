import  matplotlib.pyplot        as plt
import  gracedb_public.pixView   as pixView

# skymap projection and visualization
# Flat Resolution Sky Map
filename_ligo = \
        r'https://gracedb.ligo.org/api/superevents/MS240410u/'+\
        r'files/bayestar.fits.gz,1'

skymap = pixView.get_map_file(filename_ligo, index='nested') 
fig = pixView.mollview( skymap, index='nested', title='Test Mollweide', 
                        get_fig=False, 
                        save_fig=True, 
                        save_path='tests/test_Mollweide_flat.png')
plt.close()

# Multiorder Sky Map
multiorder_ligo = \
        r'https://gracedb.ligo.org/api/superevents/'+\
        r'MS240410u/files/bayestar.multiorder.fits,1'
skymap = pixView.get_map_file(multiorder_ligo, index='uniq') 
skymap = skymap['UNIQ']#['UNIQ']
fig = pixView.mollview( skymap, index='uniq', title='Test Mollweide Multiorder', 
                        get_fig=False, 
                        save_fig=True, 
                        save_path='tests/test_Mollweide_multi_scatter.png')
plt.close()

# No Map
skymap = None
fig = pixView.mollview( skymap, index='uniq', title='Test Mollweide No Map', 
                        get_fig=False, 
                        save_fig=True, 
                        save_path='tests/test_Mollweide_no_map.png')
plt.close()