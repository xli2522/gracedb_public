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

# system/Python-built-in dependencies
from    typing              import  Union, Optional
import  time

def get_map(filename    : str, 
            ext         : int   = 1,
            validate    : bool  = True) -> np.array:
    """
    Get the map from the fits file.

    Parameters
    ----------
    filename : str
        The path to the fits file. Can be an url or local address.
    ext : int, optional
        The extension number of the map in the fits file. Default is 1.
    validate : bool, optional
        If True, validate the nside of the map. Default is True.
    Returns
    -------
    map : np.array
        The map.
    """

    with fits.open(filename) as hdu:
        map = hdu[ext].data['PROB']

    if validate:
        nside = hp.npix_to_nside(len(map))
        hp.core._validate_nside(nside)
    
    return map


def mollview(map        : Optional[np.array]    =       None, 
             nest       : bool                  =       False,
             validate   : bool                  =       True,
             title      : Optional[str]         =       None,
             cmap       : str                   =       'viridis',
             interpolation: str                 =       'nearest',
             cbar       : bool                  =       True,
             get_fig    : bool                  =       False,
             save_fig   : bool                  =       False,
             save_path  : Optional[str]         =       None
             ) -> Optional[plt.Figure]:

    """
    Create a Mollweide projection figure of the map.

    Parameters
    ----------
    map : 1D array
        An array containing the map to be plotted.
    nest : bool, optional
        If True, ordering scheme is NESTED. Default is False.
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
        If True, return the figure. Default is False.
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
        # if map is not provided, 
        # or nside check goes wrong
        # create a blank map to prevent error
        map = np.zeros(12) + np.inf

    # imput map validation
    if validate:
        nside = hp.npix_to_nside(len(map))      # get nside of map
        hp.core._validate_nside(nside)          # check if nside is valid

    array, footprint = reproject_from_healpix((map, 'icrs'),
                                           mollweide_header, nested=True)
    # create figure
    ax = plt.subplot(1,1,1, projection=WCS(mollweide_header),
                    frame_class=EllipticalFrame)
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