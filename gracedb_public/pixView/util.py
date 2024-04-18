import astropy_healpix as hp
import numpy as np
import astropy.io.fits as fits
from typing import Union, Dict

def index_to_map_key(index: str) -> str:
    """
    Converts the index to the map key.

    Parameters
    ----------
    index (str): The index of the map.

    Returns
    -------
    map_key (str): The map key.
    """
    if      index == 'nested'   : map_key = 'PROB'
    elif    index == 'ring'     : map_key = 'PROB'
    elif    index == 'uniq'     : map_key = 'UNIQ'
    else: raise ValueError('index should be either "uniq", "nested" or "ring".')
    
    return map_key

def validate_nside(map: np.ndarray, index: str) -> None:
    """
    Validates the nside of a map.
    A custom wrapper for the astropy_healpix function core._validate_nside. It 
    deals with the uniq indexing scheme for multi-order skymaps in addition to
    the nested and ring indexing schemes.
    
    Parameters
    ----------
    map (np.ndarray): The healpix map to validate.

    Returns
    -------
    None
    """
    # map_key = index_to_map_key(index)
    
    if index == 'uniq': 
        level, _ = hp.uniq_to_level_ipix(map)
        
        nside = hp.level_to_nside(level)
    else: 
        nside = hp.npix_to_nside(len(map))
    
    hp.core._validate_nside(nside)
    
    return

def get_dummy_map_data() -> np.array:
    """
    Creates a dummy map to prevent errors when no map is provided.

    Returns
    -------
    np.arange(NPIX): A dummy map.
    """
    return np.arange(12288)

# def to_map_key_pair(map     : Union[fits.fitsrec.FITS_rec, 
#                                     np.ndarray, dict], 
#                     map_key   : str
#                     ) ->      Union[fits.fitsrec.FITS_rec, 
#                                     Dict[str, np.array]]:
#     """
#     Converts the given map and index into a map key pair if not already.
    
#     NOTE: The 'map key pair' is allowed to be a dictionary, or a FITS_rec object,
#     or a numpy array.

#     Parameters
#     ----------
#         map (Union[fits.fitsrec.FITS_rec, np.ndarray, dict]): The input map.
#         map_key (str): The index used to generate the map key.

#     Returns
#     -------
#         Union[fits.fitsrec.FITS_rec, Dict[str, np.array]]: The map key pair.

#     Raises
#     ------
#         KeyError: If the map key is not found in the map.
#     """
#     # map_key = index_to_map_key(index)
    
#     try: map[map_key]
#     except IndexError: map = {map_key: map}
#     except KeyError: raise KeyError(f'The map key {map_key} is not in the map.')
#     else: map = {map_key: get_dummy_map_data()}
    
#     return map