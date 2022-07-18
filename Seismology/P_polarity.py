# -------------------------------------------------------------------
# Calculate the first motion polarity based on the azimuth and take-off angle.
# (Homogenous model)
#
# Author: Liang Ding
# Email: myliang.ding@mail.utoronto.ca
# -------------------------------------------------------------------

import numpy as np

def calc_p_polarity(mt_enz, theta, phi):
    '''
    Compute the P motion direction.
     (ref: Peter M. Shearer, 2009. EQ.(9.22), P253)

     ! Only the polarity is available

    :param mt_enz: Moment tensor in E(X1) -- N(X2) -- Z(X3) (right-hand coordinate system.)
    :param theta:  The $\theta$ start from +X3, in radius.
    :param pi:     The $\phi$, start from (X1), in radius.
    :return: Positive(+1) or Negative (-1)
    '''

    vec = np.array([np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)])
    mt_matrix = np.array([[mt_enz[0], mt_enz[3], mt_enz[4]],
                           [mt_enz[3], mt_enz[1], mt_enz[5]],
                           [mt_enz[4], mt_enz[5], mt_enz[2]]])
    sum = 0
    for i in range(3):
        for j in range(3):
            sum += vec[i] * vec[j] * mt_matrix[i, j]

    if sum < -1e-6:
        return int(-1)
    elif sum > 1e-6:
        return int(1)
    else:
        # at the focal plane
        return int(0)
