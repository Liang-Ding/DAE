# -------------------------------------------------------------------
# The example to utilize the Manual picker.
#
# Author: Liang Ding
# Email: myliang.ding@mail.utoronto.ca
# -------------------------------------------------------------------


from DPickers.DManual import DMPickerWnd
import numpy as np


def try_DMPickerWnd():
    data_array = np.random.random((16, 100))
    fn = 500
    dt = 1 / fn
    save_path = "./out.csv"
    t0 = '20210520T18:00:00, EVT1'
    num_tr = data_array.__len__()
    for tr in range(num_tr):
        data_array[tr] = data_array[tr] / np.max(np.fabs(data_array[tr]))

    # initial window to pick.
    DMPickerWnd(data_array, t0, dt, save_path)



if __name__ == '__main__':
    try_DMPickerWnd()
