# -------------------------------------------------------------------
# Determining the moment tensor solutions sharing the same polarity from
# the given moment tensor (mt0). Then calculate the uncertainty.
#
# Author: Liang Ding
# Email: myliang.ding@mail.utoronto.ca
# -------------------------------------------------------------------

import os.path
from MTTools.DMomentTensors import DMT_enz
from Seismology.P_polarity import calc_p_polarity
import numpy as np
import pandas as pd


def xyz2rtp(sensor_df, soruce_arr):
    '''Coordinate Converter'''
    n_sensor = len(sensor_df)
    phi = np.zeros(n_sensor)
    theta = np.zeros(n_sensor)
    theta_deg = np.zeros(n_sensor)
    phi_deg = np.zeros(n_sensor)
    dx = sensor_df.x - soruce_arr[0]
    dy = sensor_df.y - soruce_arr[1]
    dz = sensor_df.z - soruce_arr[2]

    # compute the theta and phi of sensor locations
    for i in range(n_sensor):
        if dx[i] >= 0.0 and dy[i] >= 0.0:
            if dx[i] == 0.0:
                phi[i] = 1.0 / 2 * np.pi
                phi_deg[i] = 90
            else:
                phi[i] = np.arctan(dy[i] / dx[i])
                phi_deg[i] = phi[i] * 180 / np.pi
        if dx[i] < 0.0 and dy[i] > 0.0:
            phi[i] = np.pi + np.arctan(dy[i] / dx[i])
            phi_deg[i] = 180 + np.arctan(dy[i] / dx[i]) * 180 / np.pi
        if dx[i] <= 0.0 and dy[i] <= 0.0:
            if dx[i] == 0.0:
                phi[i] = 3.0 / 2 * np.pi
                phi_deg[i] = 270
            else:
                phi[i] = np.pi + np.arctan(dy[i] / dx[i])
                phi_deg[i] = 180 + np.arctan(dy[i] / dx[i]) * 180 / np.pi
        if dx[i] > 0.0 and dy[i] < 0.0:
            phi[i] = 2.0 * np.pi + np.arctan(dy[i] / dx[i])
            phi_deg[i] = 360 + np.arctan(dy[i] / dx[i]) * 180 / np.pi
        theta[i] = np.arccos(dz[i] / np.sqrt(np.square(dx[i]) + np.square(dy[i]) + np.square(dz[i])))
        theta_deg[i] = theta[i] * 180.0 / np.pi
    return phi, theta, phi_deg, theta_deg


def grid_search_MT(sensor_df, source_xyz, strike, dip, rake,
                   colatitude, lune_longitude, fm_delta=10,
                   b_save=False, save_dir=None):

    '''
    * Estimate the resolution in strike, dip, rake around giving focal mechanism (strike, dip, rake) at the position.

    :param array_id:  str, the name of sensor array
    :param source_xyz:  array, the source position.
    :param strike:          The strike in degree,  [0, 360)
    :param dip:             The dip in degree,     [0, 90]
    :param rake:            The rake in degree,    [-90, 90]
    :param colatitude:      The colat. in deg.,    [0, 180]
    :param lune_longitude:  The lune_lon. in deg., [-30, 30]
    :param fm_delta:        The interval in degree.
    :return:
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

    # The inversion.
    print("\n* Finding the moment tensor solution ... ")
    # Grid search to find all moment tensor
    strike_arr = np.deg2rad(np.arange(0, 360, fm_delta))
    dip_arr = np.deg2rad(np.arange(0, 91, fm_delta))
    rake_arr = np.deg2rad(np.arange(-90, 91, fm_delta))
    colatitude_arr = np.deg2rad(np.arange(0, 181, fm_delta))
    longitude_arr = np.deg2rad(np.arange(-30, 31, fm_delta))
    n_record = len(strike_arr) * len(dip_arr) * len(rake_arr) * len(colatitude_arr) * len(longitude_arr)

    count_solution = 0
    if b_save and save_dir is not None:
        log_strike = np.zeros(n_record)
        log_dip = np.zeros(n_record)
        log_rake = np.zeros(n_record)
        log_colat = np.zeros(n_record)
        log_long = np.zeros(n_record)
        polarity_misfit = np.zeros(n_record)
    i_record = 0
    for s in strike_arr:
        for d in dip_arr:
            for r in rake_arr:
                for colat in colatitude_arr:
                    for colon in longitude_arr:
                        if np.mod(i_record, int(n_record/10)) == 0:
                            print('Task completed: %d ' % int(100 * i_record/n_record), '%')

                        mt_enz = DMT_enz(s, d, r, colat, colon)
                        _p_motion = np.ones(n_sensor)
                        for i in range(n_sensor):
                            _p_motion[i] = calc_p_polarity(mt_enz, theta[i], phi[i])

                        # calculate the waveform misfit
                        # the first P motion at focal planes will be deprecated.
                        _misfit = 0.0
                        _n_mis = 0
                        for i in range(n_sensor):
                            if p_polarity[i] == 0:
                                continue
                            else:
                                _misfit += np.square(np.subtract(p_polarity[i], _p_motion[i]))
                                _n_mis += 1
                        if _n_mis > 0:
                            _misfit = _misfit / _n_mis

                        # count the solution
                        if abs(_misfit) < 1e-10:
                            count_solution += 1

                        if b_save and save_dir is not None:
                            log_strike[i_record] = np.round(s, 4)
                            log_dip[i_record] = np.round(d, 4)
                            log_rake[i_record] = np.round(r, 4)
                            log_colat[i_record] = np.round(colat, 4)
                            log_long[i_record] = np.round(colon, 4)
                            polarity_misfit[i_record] = _misfit
                        i_record += 1

    if b_save and save_dir is not None:
        result_df = pd.DataFrame({
            "strike": log_strike,
            "dip": log_dip,
            "rake": log_rake,
            "colatitude": log_colat,
            "longitude": log_long,
            "misfit": polarity_misfit,
        })

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        try:
            file_path = os.path.join(save_dir, "inversion_results.csv" )
            result_df.to_csv(file_path)
        except:
            result_df.to_csv('inversion_results.csv')

    print("Task completed: 100 %")
    print('******************')
    print("Result:")
    print("%d solution(s) found!\nThe estimated uncertainty is %.2f" % (count_solution, 100 * count_solution/n_record), '%')
    print("Done!")
    print('******************')

    return np.round(count_solution/n_record, 4)


