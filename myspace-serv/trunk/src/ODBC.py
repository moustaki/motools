'''
Created on May 28, 2009

@author: kurtjx
'''

import pyodbc
from ConfigParser import ConfigParser, Error


class ODBC:
    '''
    a connection thru odbc to virtuoso
    '''
    def __init__(self):
        '''
        Constructor
        '''
        config = ConfigParser()
        config.read('configuration')
        self.cursor = None
        try:
            self.user = config.get('ODBC', 'user')[1:-1]    # horrible kludge to get rid of quotes
            self.host = config.get('ODBC', 'host')[1:-1]
            self.pwd = config.get('ODBC', 'pass')[1:-1]
            self.dsn = config.get('ODBC', 'dsn')[1:-1]
        except Error, err:
            log('FAILED: could not configure ODBC connection - '+str(err))
        else:
            self.connect()
        
    def connect(self):
        '''
            make the connection
        '''
        self.connect = pyodbc.connect('DSN='+self.dsn+';UID='+self.user+';PWD='+self.pwd+';HOST='+self.host)
        