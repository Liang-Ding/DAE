# -------------------------------------------------------------------
# Connect to the remote database, SeisCloud (https://seis.cloud).
#
# Author: Liang Ding
# Email: myliang.ding@mail.utoronto.ca
# Data: Jun. 7th, 2023
# -------------------------------------------------------------------

class dbBase():
    '''
    The remote database.
    '''
    def __init__(self, db_url=None, db_port=None):
        '''
        The base class of SeisClient.
        The address to the database on SeisCloud.

        :param db_url:  The url.
        :param db_port: The port.
        '''
        if db_url is None and db_port is None:
            self.db_url = "https://db.seis.cloud"
            self.db_port = None
        else:
            self.db_url = db_url
            self.db_port = db_port