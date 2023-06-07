# -------------------------------------------------------------------
# Tools to request sensor locations from SeisCloud (https://seis.cloud)
#
# Author: Liang Ding
# Email: myliang.ding@mail.utoronto.ca
# Data: Jun. 7th, 2023
# -------------------------------------------------------------------

from DArrays import dbBase
import requests


class Designer(dbBase):
    '''
    Request sensor array from SeisCloud (https://seis.cloud).
    '''

    def __init__(self, db_url=None, db_port=None):
        super().__init__(db_url=db_url, db_port=db_port)

    def __check(self):
        '''Check input data'''
        pass

    def __request_block(self, nsensor, p1x, p1y, p1z, p2x, p2y, p2z, saving_filepath):
        ''' Requst sensor locations on block samples form SeisCloud. '''

        if self.db_port is None:
            ip_addr = self.db_url
        else:
            ip_addr = '%s:%s' % (self.db_url, self.db_port,)

        request_cmd = '%s/aeblocks?' \
                      'nsensor=%d&' \
                      'p1x=%.4f&' \
                      'p1y=%.4f&' \
                      'p1z=%.4f&' \
                      'p2x=%.4f&' \
                      'p2y=%.4f&' \
                      'p2z=%.4f&'\
                      % (ip_addr, nsensor, p1x, p1y, p1z,  p2x, p2y, p2z)

        # request SGT from remote database
        r = requests.get(request_cmd)
        if r.status_code == 200:
            try:
                text = r.content.decode()
            except:
                raise ValueError
        else:
            raise ValueError

        # save to file
        with open(saving_filepath, 'w') as f:
            f.write(text)


    def __request_cylinder(self, nsensor, radius, height, saving_filepath):
        ''' Requst sensor locations on cylinder samples form SeisCloud. '''

        if self.db_port is None:
            ip_addr = self.db_url
        else:
            ip_addr = '%s:%s' % (self.db_url, self.db_port,)

        request_cmd = '%s/aecylinders?' \
                      'nsensor=%d&' \
                      'radius=%.4f&' \
                      'height=%.4f&' \
                      % (ip_addr, nsensor, radius, height)

        # request SGT from remote database
        r = requests.get(request_cmd)
        if r.status_code == 200:
            try:
                text = r.content.decode()
            except:
                raise ValueError
        else:
            raise ValueError

        # save to file
        with open(saving_filepath, 'w') as f:
            f.write(text)


    def get_sensors_on_blocks(self, nsensor, p1x, p1y, p1z, p2x, p2y, p2z, saving_filepath):
        self.__request_block(nsensor, p1x, p1y, p1z, p2x, p2y, p2z, saving_filepath)

    def get_sensors_on_cylinders(self, nsensor, radius, height, saving_filepath):
        self.__request_cylinder(nsensor, radius, height, saving_filepath)



