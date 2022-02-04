from datetime import datetime
from logging.handlers import RotatingFileHandler

# constants
# select one of these two
logDirectory = '../some/directory/somewhere'
logDirectory = '.'




def setUpLogging(directory, scriptName=0, DEBUG=0):

  # set up some housekeeping
  if directory == '.':
      '''
          Get Current working Directory
      '''
      currentDirectory = os.getcwd()
      if scriptName == 0:
        logfilename = currentDirectory + "/" + os.path.basename(__file__).replace('.py','.log')
      else:
        logfilename = currentDirectory + "/" + scriptName.replace('.py','.log')
  else:
    if scriptName == 0:
      logfilename = directory + os.path.basename(__file__).replace('.py','.log')
    else:
      logfilename = directory + "/" + scriptName.replace('.py','.log')

  if DEBUG:
    print("log file name is " + logfilename)

  logging.basicConfig(
      handlers = [RotatingFileHandler(logfilename, maxBytes=1000000, backupCount=5)],
      format='%(asctime)s : %(filename)s : %(levelname)s : %(message)s', 
      level=logging.DEBUG
  ) 


  return logging

if __name__ == '__main__':

  setUpLogging(logDirectory)

  '''
  logging.debug('This is a debug message')
  logging.info('This is an info message')
  logging.warning('This is a warning message')
  logging.error('This is an error message')
  logging.critical('This is a critical message')
  '''
  logging.info('>>> BEGIN:  %s' % os.path.basename(__file__))
  totalConversionStartTime = datetime.now()
  logging.info('>>> START TIME: %s' % totalConversionStartTime)

  logging.debug('>>> Starting loop looking for files in directory')

  logging.info('====================================================================')

  logging.info('Working on file : ' + 'some filename or variable')

  newFilename = 'bla.py'
  logging.debug("New filename is " + newFilename)

  logging.info('>>> COMPLETED:  %s' % os.path.basename(__file__))

