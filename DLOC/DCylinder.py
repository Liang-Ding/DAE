# -------------------------------------------------------------------
# Source localization for Acoustic Emission (AE) test.
# Homogeneous samples.
#
# Author: Liang Ding
# Email: myliang.ding@mail.utoronto.ca
# -------------------------------------------------------------------

import numpy as np

def dist_cylinder(p1, p2):
    '''Return the distance between two points in cylindrical coordinate.'''
    return np.sqrt(np.power((p1[0] * np.cos(np.deg2rad(p1[1])) - p2[0] * np.cos(np.deg2rad(p2[1]))), 2) +
                   np.power((p1[0] * np.sin(np.deg2rad(p1[1])) - p2[0] * np.sin(np.deg2rad(p2[1]))), 2) +
                   np.power(p1[2] - p2[2], 2))


class DLocCylinder():
    '''Source localization in Cylindrical Coordinate '''
    def __init__(self, radius, height, velocity):
        self.radius = radius
        self.height = - 1.0 * np.fabs(height) # all are negative.
        self.velocity = velocity    # homo model.

        self.b_sensor = False
        self.Nq = 4  # XYZT
        self.MIN_DT = 1E-6


    def set_sensor(self, sensors):
        '''
        Set sensor location [s, theta, z]
        x = s * cos(theta)
        y = s * sin(theta)
        z = z
        '''

        self.sensors = sensors
        self.n_sensor = len(self.sensors)
        self.b_sensor = True


    def set_q(self, q):
        '''Set initial location.'''
        self.q = q
        self.dUdq(q)


    def Uq(self, q):
        '''Mean square error.  '''
        dt = 0
        for i in range(self.n_sensor):
            l = dist_cylinder(self.sensors[i], q[:3])
            dt += np.square(l/self.velocity + q[3] - self.t_array[i])
        return dt/self.n_sensor


    def dUdq(self, q):
        '''Compute the gradient.'''
        self.dU_dqi = np.zeros(self.Nq)

        df_ds = 0
        df_dtheta = 0
        df_dz = 0
        df_dt = 0
        for i in range(self.n_sensor):
            l = dist_cylinder(q, self.sensors[i])
            dt = q[3] + l/self.velocity - self.t_array[i]
            A = 1.0 / l
            df_ds += dt * A * ((q[0] * np.cos(np.deg2rad(q[1])) - self.sensors[i][0] * np.cos(np.deg2rad(self.sensors[i][1]))) * np.cos(np.deg2rad(q[1]))+
                          (q[0] * np.sin(np.deg2rad(q[1])) - self.sensors[i][0] * np.sin(np.deg2rad(self.sensors[i][1]))) * np.sin(np.deg2rad(q[1])))
            df_dtheta += dt * A * (-1.0 * np.sin(np.deg2rad(q[1])) * self.sensors[i][0] * np.cos(np.deg2rad(self.sensors[i][1])) -
                               np.cos(np.deg2rad(q[1])) * self.sensors[i][0] * np.sin(np.deg2rad(self.sensors[i][1])))
            df_dz += dt * A * (q[2] - self.sensors[i][2])
            df_dt += dt
        self.dU_dqi[0] = 2.0 / self.velocity / self.n_sensor * df_ds
        self.dU_dqi[1] = 2.0 / self.velocity / self.n_sensor * df_dtheta
        self.dU_dqi[2] = 2.0 / self.velocity / self.n_sensor * df_dz
        self.dU_dqi[3] = 2.0 * df_dt / self.n_sensor


    def get_location(self, q0, t_array, epsilon, num_iter=100):
        '''Localization.'''
        if len(t_array) != len(self.sensors):
            print("Incompatible sensor and time.")
            return False

        self.t_array = t_array
        self.set_q(q0)
        for _ in range(num_iter):
            if np.fabs(self.Uq(self.q)) < self.MIN_DT:
                break

            _q = self.q.copy()
            _q -= epsilon * self.dU_dqi
            if _q[0] > self.radius:
                _q[0] = self.radius
            elif _q[0] < 0:
                _q[0] = 0
            if _q[1] > 360:
                _q[1] -= 360
            if _q[2] > 0:
                _q[2] = 0
            elif _q[2] < self.height:
                _q[2] = self.height

            self.set_q(_q)

