# -------------------------------------------------------------------
# An example of getting sensor locations from SeisCloud (https://seis.cloud)
#
# Author: Liang Ding
# Email: myliang.ding@mail.utoronto.ca
# -------------------------------------------------------------------

from DArrays.AEDesigner import Designer

def get_sensors_and_save():

    designer = Designer()

    # sensor locations on the block sample
    saving_filepath = "sensor_block_n20.csv"
    designer.get_sensors_on_blocks(nsensor=20, p1x=32.5, p1y=-32.5, p1z=65,
                                   p2x=-32.5, p2y=32.5, p2z=-65, saving_filepath=saving_filepath)

    # sensor locations on the cylinder sample
    saving_filepath = "sensor_cylinder_n20.csv"
    designer.get_sensors_on_cylinders(nsensor=20, radius=50, height=100,
                                     saving_filepath=saving_filepath)


if __name__ == '__main__':
    get_sensors_and_save()
