'''
Created on 27 Jan 2010

parses the config file

@author: kurtjx
'''

from ConfigParser import ConfigParser, Error

class MyspaceConfigMissingException(Exception):
    def __init__(self,msg):
        self.msg= '''The configuration file 'config' is missing \n\t tried: '''+str(msg)
        
class MyspaceConfigError(Exception):
    def __init__(self,msg):
        self.msg='''The 'config' file is missing some parameter: '''+ str(msg)

config = ConfigParser()
config.read(['../config', '../../../src/config','../src/config', 'config', '../../../config'])

try:
    config.read('config')
except Error:
    print 'error, no config file\n you must cp default.config config and edit\n exting...'
    raise MyspaceConfigMissingException('')
try:
    SPARQL_ENABLED = config.get('sparql', 'enable')
except Error:
    raise MyspaceConfigError('sparql: enable')
try:
    URL_BASE = config.get('urls', 'base')[1:-1]
    if URL_BASE.endswith('/'):
        URL_BASE=URL_BASE[:-1]
except Error:
    raise MyspaceConfigError('urls: base')
try:
    ENDPOINT = config.get('sparql', 'endpoint')[1:-1]
except Error:
    raise MyspaceConfigError('sparql: endpoint')
