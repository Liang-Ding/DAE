# -------------------------------------------------------------------
# An example of source localization in cylindrical coordination.
#
# Author: Liang Ding
# Email: myliang.ding@mail.utoronto.ca
# -------------------------------------------------------------------

from DLOC.DCylinder import DLocCylinder, dist_cylinder
import numpy as np

def example():
    # Diameter:
    # 51.13mm
    # 50.92mm
    # 50.72mm

    radius = (51.13 + 50.92 + 50.72) / 3 / 2
    height = 97.1       # mm
    velocity = 3.333   # mm/us (millimeter/microsecond)  = 3333m/s

    # Four sensors
    sensors = np.array([[radius, 0.0, -15.0],
                        [radius, 270, -30.0],
                        [radius, 180, -45.0],
                        [radius, 90, -60.0]])


    ########################################
    # todo: replace the (t_array) with your picking result.
    # data preparation for the synthetic test.
    # randomly select a source to compute the first break.
    source = np.array([10, 25, -40])
    t_array = []
    for s in sensors:
        t_array.append(dist_cylinder(s, source)/velocity)
    t_array = np.asarray(t_array)
    # remove the initial time.
    t_array = t_array - np.min(t_array)
    ########################################


    # inversion
    dloc = DLocCylinder(radius, height, velocity)
    dloc.set_sensor(sensors)
    # initial solution [s, theta, z, initial_time].
    q0 = np.array([5.0, 10.0, -20.0, 0.0])
    dloc.get_location(q0, t_array, epsilon=0.5, num_iter=10000)

    print("location={} \ninitial time={}, \nMSE={}".format(dloc.q[:3], dloc.q[3], dloc.Uq(dloc.q)))


if __name__ == '__main__':
    example()


