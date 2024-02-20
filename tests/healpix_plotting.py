# X. Li 2024
# astropy - fits, healpix, tests
#
# see: 
# https://emfollow.docs.ligo.org/userguide/tutorial/multiorder_skymaps.html
# https://astropy-healpix.readthedocs.io/en/latest/

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
    i = np.argmax(skymap['PROBDENSITY'])        # find the most probable pixel
    # find the UNIQ value of the most probable pixel
    uniq = skymap[i]['UNIQ']    
    # convert the probability density to per square degree
    density = skymap[i]['PROBDENSITY'] * (np.pi / 180)**2
    # find the level and pixel number of the most probable pixel   
    level, ipix = ah.uniq_to_level_ipix(uniq)                       
    nside = ah.level_to_nside(level)
    lon_max, lat_max = ah.healpix_to_lonlat(ipix, nside, order='nested')

    print('Most probable location: ', lon_max.deg, lat_max.deg, sep=' ')

    # the entire probability map 
    level, ipix = ah.uniq_to_level_ipix(skymap['UNIQ'])
    nside = ah.level_to_nside(level)
    lon, lat = ah.healpix_to_lonlat(ipix, nside, order='nested')

    print(level.shape, ipix.shape, lon.shape, lat.shape, sep=' ')

    # find credible levels
    i = np.flipud(np.argsort(skymap['PROBDENSITY']))
    sorted_credible_levels = np.cumsum(skymap['PROBDENSITY'][i])
    credible_levels = np.empty_like(sorted_credible_levels)
    credible_levels[i] = sorted_credible_levels

    # shift longitude values by pi rad
    lon_array, lat_array = [np.array(lon) - np.pi, np.array(lat)]

    plt.figure()
    plt.subplot(111, projection="mollweide",  facecolor='LightCyan')

    cred_levelMap = plt.scatter(lon_array, lat_array, 
                                c=credible_levels[i], 
                                marker='s', s=3, cmap='twilight_shifted')
 
    plt.scatter(np.array(lon_max)-np.pi, lat_max,  
                                c='r', marker='*', label='Probability Peak')
    plt.title('Mollweide Projection Test, Credible Levels')
    plt.legend()
    plt.colorbar(cred_levelMap)
    plt.grid(True)
    plt.savefig('tests/healpix_mollweide.png')

    # find the 90% probability region
    # Ref:
    # https://emfollow.docs.ligo.org/userguide/tutorial/multiorder_skymaps.html

    # Sort the pixels of the sky map by descending probability density.
    skymap.sort('PROBDENSITY', reverse=True)
    # Find the area of each pixel.
    level, ipix = ah.uniq_to_level_ipix(skymap['UNIQ'])
    pixel_area = ah.nside_to_pixel_area(ah.level_to_nside(level))
    # Calculate the probability within each pixel: 
    # the pixel area times the probability density.
    prob = pixel_area * skymap['PROBDENSITY']
    # Calculate the cumulative sum of the probability.
    cumprob = np.cumsum(prob)
    # Find the pixel for which the probability sums to 0.9 (90%).
    i = cumprob.searchsorted(0.9)
    # The area of the 90% credible region is simply 
    # the sum of the areas of the pixels up to that one.
    area_90 = pixel_area[:i].sum()
    print(area_90.to_value(u.deg**2))

    # Keep only the pixels that are within the 90% credible region.
    skymap = skymap[:i]     # the skymap PROBDENSITY was reverse sorted earlier
    # Sort the pixels by their UNIQ pixel index.
    skymap.sort('UNIQ')
    # Delete all columns except for the UNIQ column.
    skymap90P = skymap['UNIQ',]
    # Write to a FITS file.
    # skymap90P.write('90percent.moc.fits')

    skymap90P.info()
    # the entire probability map 
    level90P, ipix90P = ah.uniq_to_level_ipix(skymap90P['UNIQ'])
    nside90P = ah.level_to_nside(level90P)
    lon, lat = ah.healpix_to_lonlat(ipix90P, nside90P, order='nested')

    print(r'90% confidence region:', 
          level.shape, ipix.shape, 
          lon.shape, lat.shape, sep=' ')

    # shift longitude values by pi rad
    lon_array, lat_array = [np.array(lon) - np.pi, np.array(lat)]

    plt.figure()
    plt.subplot(111, projection="mollweide",  facecolor='LightCyan')

    map90Pregion = plt.scatter(lon_array, lat_array, 
                                c=skymap90P['UNIQ'], 
                                marker='s', s=3, cmap='twilight_shifted')
    plt.title('90% Confidence Region')
    plt.colorbar(map90Pregion)
    plt.grid(True)
    plt.savefig('tests/healpix_90p_region.png')
