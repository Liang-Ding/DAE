# -------------------------------------------------------------------
# An example of using the mt_uncertainty.py
#
# Author: Liang Ding
# Email: myliang.ding@mail.utoronto.ca
# -------------------------------------------------------------------

import sys

sys.path.insert(1, '/home/dingl/repository/TimGit/DAE_github/')


from examples.mt_uncertainty import grid_search_MT
import pandas as pd
import numpy as np


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

    # the interval of grid search
    fm_delta = 10

    # whether to store the misfit by moment tensor as file (save_dir)
    b_save = True
    save_dir = './'
    grid_search_MT(sensor_df, source_xyz, strike, dip, rake,
                   colatitude, lune_longitude, fm_delta=fm_delta,
                   b_save=b_save, save_dir=save_dir)


if __name__ == '__main__':
    determine_uncertainty()
