# X. Li 2024
# astropy - fits, healpix, tests

import numpy as np
import matplotlib.pyplot as plt
# from astropy.io import fits
from astropy.table import QTable
from astropy import units as u

# HEALPix
import astropy_healpix as ah

if __name__ == '__main__':
    skymap = QTable.read(
        r'tests\test_data\httpsgracedb.ligo.'
        r'orgapisupereventsMS231103xfilesbayestar.multiorder.fits1'
        )

    # most probable location
    i = np.argmax(skymap['PROBDENSITY'])            # find the most probable pixel
    # find the UNIQ value of the most probable pixel
    uniq = skymap[i]['UNIQ']    
    # convert the probability density to per square degree
    density = skymap[i]['PROBDENSITY'] * (np.pi / 180)**2
    # find the level and pixel number of the most probable pixel   
    level, ipix = ah.uniq_to_level_ipix(uniq)                       
    nside = ah.level_to_nside(level)
    ra_max, dec_max = ah.healpix_to_lonlat(ipix, nside, order='nested')

    print('Most probable location: ', ra_max.deg, ra_max.deg, sep=' ')

    # the entire probability map 
    level, ipix = ah.uniq_to_level_ipix(skymap['UNIQ'])
    nside = ah.level_to_nside(level)
    ra, dec = ah.healpix_to_lonlat(ipix, nside, order='nested')

    print(level.shape, ipix.shape, ra.shape, dec.shape, sep=' ')

    # find credible levels
    i = np.flipud(np.argsort(skymap['PROBDENSITY']))
    sorted_credible_levels = np.cumsum(skymap['PROBDENSITY'][i])
    credible_levels = np.empty_like(sorted_credible_levels)
    credible_levels[i] = sorted_credible_levels

    plt.figure()
    plt.subplot(111, projection="mollweide",  facecolor='LightCyan')
    plt.scatter(ra, dec, c=credible_levels[i])
    plt.scatter(ra_max, dec_max, c='r', label='Probability Peak')
    plt.title('Mollweide Projection Test, Credible Levels')
    plt.legend()
    plt.colorbar()
    plt.grid(True)
    plt.savefig('tests/healpix_mollweide.png')