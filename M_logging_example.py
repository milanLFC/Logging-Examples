import logging
import os
import time
from datetime import datetime

# constants
# select one of these two
directory = '../some/directory/somewhere'
directory = '.'

# set up some housekeeping
if directory == '.':
    '''
        Get Current working Directory
    '''
    currentDirectory = os.getcwd()
    logfilename = currentDirectory + "/" + os.path.basename(__file__).replace('.py','.log')
else:
    logfilename = directory + os.path.basename(__file__).replace('.py','.log')

print("log file name is " + logfilename)

logging.basicConfig(
    filename=logfilename,
    filemode='a',
    format='%(asctime)s : %(filename)s : %(levelname)s : %(message)s', 
    level=logging.DEBUG
) 

'''
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')
'''

# some example log entries
logging.info('>>> BEGIN:  %s' % os.path.basename(__file__))
totalConversionStartTime = datetime.now()
logging.info('>>> START TIME: %s' % totalConversionStartTime)

logging.info('Working on directory: ' + currentDirectory)

logging.debug('>>> Starting loop looking for files in directory')

logging.info('====================================================================')

logging.info('Working on file : ' + 'some filename or variable')

newFilename = 'bla.py'
logging.debug("New filename is " + newFilename)

logging.info('>>> COMPLETED:  %s' % os.path.basename(__file__))
