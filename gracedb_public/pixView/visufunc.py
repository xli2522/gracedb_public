# basic dependencies
import  numpy               as      np
import  matplotlib.pyplot   as      plt

# astropy healpix algorithms
import  astropy_healpix     as      hp
from    astropy.io          import  fits

# GraceDB-public custom projection settings
from    .projections import  mollweide_header

# astropy projection functions
from    reproject           import  (reproject_from_healpix, 
                                    reproject_to_healpix)
from    astropy.wcs         import  WCS
from    astropy.visualization.wcsaxes.frame \
                            import  EllipticalFrame

# GraceDB-public custom pixView functions
import  gracedb_public.pixView.util \
                            as util

# system/Python-built-in dependencies
from    typing              import  Union, Optional
import  time

def get_map_file(filename    : str, 
                 index       : str   = 'nested',
                 ext         : int   = 1,
                 validate    : bool  = False) -> np.array:
    """
    Get the map from the fits file.

    Parameters
    ----------
    filename : str
        The path to the fits file. Can be an url or local address.
    index : str, optional
        The index of the map. Default is 'nested'.
    ext : int, optional
        The extension number of the map in the fits file. Default is 1.
    Returns
    -------
    map : np.array
        The map.
    """
    map_key = util.index_to_map_key(index)

    with fits.open(filename) as hdu:
        map = hdu[ext].data
    
    return map

def mollview(map        : Optional[np.array]    =       None, 
             index      : str                   =       'nested',
             validate   : bool                  =       True,
             title      : Optional[str]         =       None,
             cmap       : str                   =       'viridis',
             interpolation: str                 =       'nearest',
             cbar       : bool                  =       True,
             get_fig    : bool                  =       True,
             save_fig   : bool                  =       False,
             save_path  : Optional[str]         =       None
             ) -> Optional[plt.Figure]:

    """
    Create a Mollweide projection figure of the map.

    Parameters
    ----------
    map : 1D array
        An array containing the map to be plotted.
    index : str, optional
        The index of the map. Default is 'nested'.
    validate : bool, optional
        If True, validate the nside of the map. Default is True.
    title : str, optional
        The title of the plot. Default is None.
    cmap : str, optional
        The colormap of the plot. Default is 'viridis'.
    interpolation : str, optional
        The interpolation method. Default is 'nearest'.
    cbar : bool, optional
        If True, show colorbar. Default is True.
    get_fig : bool, optional
        If True, return the figure. Default is True.
    save_fig : bool, optional
        If True, save the figure. Default is False.
    save_path : str, optional
        The path to save the figure. Default is None.
    
    Returns
    -------
    fig : `~matplotlib.figure.Figure`
        The figure. Only returned if get_fig is True.
    """
    if map is None: 
        map = util.get_dummy_map_data()
        index = 'nested'
    
    if      index ==    'uniq'      : pass
    elif    index ==    'nested'    : nested = True
    elif    index ==    'ring'      : nested = False
    else: 
        raise ValueError('index should be either "uniq", "nested", or "ring".')
    
    map_key = util.index_to_map_key(index)
    
    # map = util.to_map_key_pair(map, map_key) 

    if validate: util.validate_nside(map[map_key], index)
    
    if index == 'uniq':
        level, ipix = hp.uniq_to_level_ipix(map[map_key])
        nside = hp.level_to_nside(level)
        ax = plt.subplot(1,1,1, projection="mollweide",  facecolor='LightCyan')
        lon, lat = hp.healpix_to_lonlat(ipix, nside, order='nested')
        lon_array, lat_array = [np.array(lon) -  np.pi, np.array(lat)]
        fig = ax.scatter(lon_array, lat_array, 
                                c=map[map_key], 
                                marker='s', s=3, cmap=cmap)
        
    if index in ['nested', 'ring']:
        ax = plt.subplot(1,1,1, projection=WCS(mollweide_header),
                    frame_class=EllipticalFrame)
        array, footprint = reproject_from_healpix((map[map_key], 'icrs'),
                                            mollweide_header, nested=nested)

        fig = ax.imshow(array, cmap=cmap, interpolation=interpolation)
        ax.coords.grid(color='white')
        ax.coords['ra'].set_ticklabel(color='white')

    if title is None: title = 'Mollweide Projection'
    ax.set_title(title)

    # additional ax settings
    if cbar: plt.colorbar(fig, orientation='horizontal')
    if save_fig: 
        if save_path is None: save_path = str(time.time())+'.png'
        else: plt.savefig(save_path)
    if get_fig: return ax.figure
    
    return 