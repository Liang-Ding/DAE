# -------------------------------------------------------------------
# Tools to read the SRM (a proprietary format) file.
# Counts read by this code and the InSite Lab (a commercial software) are consistent.
#
# Author: Liang Ding
# Email: myliang.ding@mail.utoronto.ca
# -------------------------------------------------------------------

import numpy as np

class DSRM():
    def __init__(self, srm_file_path, Fs=10E6, num_channel=4,
             dtype=np.int16, Bit_range=12, Volt_range=5):
        '''
        :param srm_file_path: The file path of a single SRM file.
        :param Fs:            The sampling rate in Hz. INT
        :param num_channel:   Number of channel in the SRM file. INT.
        :param dtype:         The data type. Usually unsigned INT (np.int16).
        :param Bit_range:     2**Bit_range for the quantification.
        :param Volt_range:    The voltage range.
        '''

        self.srm_file_path = srm_file_path
        # todo: check file accessibility.
        self.b_srm_file = True
        self.Fs = Fs
        self.num_channel = num_channel
        self.dtype = dtype
        self.bytes_per_sample = 2
        self.Bit_range = Bit_range
        self.Volt_range = Volt_range


    def read(self, offset, L):
        '''
        Start from the offset second to read a length of L second sequence from the SRM file.

        :param offset:  The offset in second. (Float)
        :param L:       The length in second. (Float)
        :return:        Counts with a shape of [self.num_channel, L*Fs]
        '''

        try:
            with open(self.srm_file_path, "rb") as f:
                precise_offset = np.round(offset, 7)
                offset_byte = int(precise_offset * self.Fs * self.bytes_per_sample * self.num_channel)
                f.seek(offset_byte)

                data_length = int(self.num_channel * int(L * self.Fs))
                if -1 == int(L):
                    dat = np.array(np.fromfile(f, self.dtype, -1), dtype=np.float)
                    num_sample = dat.__len__() // self.num_channel
                    dat = np.transpose(np.reshape(dat, (num_sample, self.num_channel)))
                else:
                    dat = np.array(np.fromfile(f, self.dtype, data_length), dtype=np.float)
                    # samples are placed in the order of [c1, c2, c3, c4]
                    dat = np.transpose(np.reshape(dat, (int(L * self.Fs), self.num_channel)))
        except:
            return None
        return dat / (2 ** (self.Bit_range - 1)) * self.Volt_range

