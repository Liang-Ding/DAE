# -------------------------------------------------------------------
# An example of using the mt_uncertainty.py
#
# Author: Liang Ding
# Email: myliang.ding@mail.utoronto.ca
# -------------------------------------------------------------------

from examples.mt_uncertainty import grid_search_MT, xyz2rtp
from MTTools.DMomentTensors import DMT_enz
from Seismology.P_polarity import calc_p_polarity

import pandas as pd
import numpy as np


def get_p_polarity(sensor_df, source_xyz, strike, dip, rake, colatitude, lune_longitude):
    '''
    To create the first P polarity data at sensor positions.
    (The synthetic example uses those polarities as data.)

    :param sensor_df:   The sensor positions, (pandas.DataFrame)
    :param source_xyz:  The source location, (numpy array.)
    :param strike:          The strike in degree,  [0, 360)
    :param dip:             The dip in degree,     [0, 90]
    :param rake:            The rake in degree,    [-90, 90]
    :param colatitude:      The colat. in deg.,    [0, 180]
    :param lune_longitude:  The lune_lon. in deg., [-30, 30]
    '''

    n_sensor = len(sensor_df)
    # convert sensor location from cartesian to sphere coordinates.
    phi, theta, phi_deg, theta_deg = xyz2rtp(sensor_df, source_xyz)

    # The forward
    # compute the p polarity at sensors with the given moment tensor:
    # (strike, dip, rake, colatitude, lune_longitude)
    strike_rad         = np.deg2rad(strike)
    rake_rad           = np.deg2rad(rake)
    dip_rad            = np.deg2rad(dip)
    colatitude_rad     = np.deg2rad(colatitude)
    lune_longitude_rad = np.deg2rad(lune_longitude)
    mt_enz = DMT_enz(strike_rad, dip_rad, rake_rad, colatitude_rad, lune_longitude_rad)
    p_polarity = np.zeros(n_sensor)
    for i in range(n_sensor):
        p_polarity[i] = calc_p_polarity(mt_enz, theta[i], phi[i])

    return p_polarity


def determine_uncertainty():
    '''
    Example of using the mt_uncertainty.py
    '''

    # read the sensor locations
    sensor_location = "./examples/sensor_array_1.csv"
    sensor_df = pd.read_csv(sensor_location)

    # user-specified source location in the cubic sample with a unit length.
    source_xyz = [0.5, 0.5, 0.5]

    # user-specified moment tensor that is parameterized by
    # strike, dip, rake, co-latitude, and longitude on lune.
    strike = 0
    dip = 90
    rake = 0
    colatitude = 90
    lune_longitude = 0

    # load the 'observed' P-wave polarity
    p_polarity = get_p_polarity(sensor_df, source_xyz, strike, dip, rake, colatitude, lune_longitude)

    # the interval of grid search
    fm_delta = 10

    # Store the misfit by moment tensor as file if b_save=True and save_dir is set.
    b_save = True
    save_dir = './'
    grid_search_MT(sensor_df, source_xyz, p_polarity,
                   fm_delta=fm_delta, b_save=b_save, save_dir=save_dir)


if __name__ == '__main__':
    determine_uncertainty()
