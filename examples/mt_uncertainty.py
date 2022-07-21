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


def grid_search_MTI(sensor_df, source_xyz, p_polarity, fm_delta=10,
                    inv_type='full', b_save=False, save_dir=None):

    '''
    Inverting the full moment tensor solutions with first P-wave polarity and grid search and
    Calculating the uncertainty.

    :param sensor_df:   The sensor positions, (pandas.DataFrame)
    :param source_xyz:  The source location, (numpy array.)
    :param p_polarity:  The observed p-polarity with the same order of sensor in the sensor_df.
    :param fm_delta:    The interval in degree of grid search.
    :param inv_type:    The inversion type, 'full' - full moment tensor (default)
                                            'dc'   - double-couple
                                            'dev'  - deviatoric (dc+clvd)
    :return:
    '''

    n_sensor = len(sensor_df)
    # convert sensor location from cartesian to sphere coordinates.
    phi, theta, phi_deg, theta_deg = xyz2rtp(sensor_df, source_xyz)

    # Grid search to find all moment tensor
    strike_arr = np.deg2rad(np.arange(0, 360, fm_delta))
    dip_arr = np.deg2rad(np.arange(0, 91, fm_delta))
    rake_arr = np.deg2rad(np.arange(-90, 91, fm_delta))

    # Inversion type, default: full moment tensor.
    _inv_type = str(inv_type).lower().strip()
    if _inv_type.__contains__('dc'):
        print("\n* Finding the Double-couple moment tensor solutions ... ")
        colatitude_arr = np.deg2rad(np.array([90]))
        longitude_arr = np.deg2rad(np.array([0]))
    elif _inv_type.__contains__('dev'):
        print("\n* Finding the deviatoric moment tensor solutions ... ")
        colatitude_arr = np.deg2rad(np.array([90]))
        longitude_arr = np.deg2rad(np.arange(-30, 31, fm_delta))
    else:
        print("\n* Finding the full moment tensor solutions ... ")
        colatitude_arr = np.deg2rad(np.arange(0, 181, fm_delta))
        longitude_arr = np.deg2rad(np.arange(-30, 31, fm_delta))

    result_df = _grid_search(n_sensor, theta, phi, p_polarity,
                 strike_arr, dip_arr, rake_arr, colatitude_arr, longitude_arr)

    print("Inversion completed: 100 %")
    print('*****Result*****')
    uncertainty = _quantify_uncertainty(result_df)
    if b_save and save_dir is not None:
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        try:
            file_path = os.path.join(save_dir, "inversion_results_%s_d%.1f.csv" % (_inv_type, fm_delta))
            result_df.to_csv(file_path)
        except:
            result_df.to_csv("inversion_results_%s_d%.1f.csv" % (_inv_type, fm_delta))

    print("The estimated uncertainty is %.4f" % uncertainty, '%')
    print("Done!")
    print('******************')


def _grid_search(n_sensor, theta, phi, p_polarity,
                 strike_arr, dip_arr, rake_arr, colatitude_arr, longitude_arr):

    '''
    Inverting the full moment tensor solutions with first P-wave polarity and grid search and
    Calculating the uncertainty.

    :param sensor_df:   The sensor positions, (pandas.DataFrame)
    :param source_xyz:  The source location, (numpy array.)
    :param p_polarity:  The observed p-polarity with the same order of sensor in the sensor_df.
    :param fm_delta:    The interval in degree of grid search.
    :return:
    '''

    n_record = len(strike_arr) * len(dip_arr) * len(rake_arr) * len(colatitude_arr) * len(longitude_arr)
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

                        log_strike[i_record] = np.round(s, 4)
                        log_dip[i_record] = np.round(d, 4)
                        log_rake[i_record] = np.round(r, 4)
                        log_colat[i_record] = np.round(colat, 4)
                        log_long[i_record] = np.round(colon, 4)
                        polarity_misfit[i_record] = _misfit
                        i_record += 1

    # create a DataFrame object to store the inversion result.
    result_df = pd.DataFrame({
        "strike": log_strike,
        "dip": log_dip,
        "rake": log_rake,
        "colatitude": log_colat,
        "longitude": log_long,
        "misfit": polarity_misfit,
    })
    return result_df


def _quantify_uncertainty(result_df):
    '''Count the solution and calculate the uncertainty.'''
    # count the solution
    n_record = len(result_df)
    n_solution = len(result_df[result_df['misfit'] < 1e-10])
    print("%d solution(s) found! "% n_solution)
    return np.round(n_solution / n_record * 100, 4)

