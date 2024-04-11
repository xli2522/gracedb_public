import matplotlib.pyplot as plt
# from gracedb_public.pixView.visufunc import get_map, mollview
import gracedb_public.pixView as pixView

# skymap projection and visualization

filename_ligo = \
r'https://gracedb.ligo.org/api/superevents/MS240410u/files/bayestar.fits.gz,1'
skymap = pixView.get_map(filename_ligo) 
fig = pixView.mollview( skymap, nest=False, title='Test Mollweide', 
                        get_fig=False, 
                        save_fig=True, 
                        save_path='tests/Test_Mollweide.png')
plt.close()
