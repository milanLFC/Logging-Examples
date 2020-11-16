import os
import logging
import sys
import subprocess
import time
sys.path.insert(0,'/home/milanp/mybin/Telegram')
from datetime import datetime
from dateutil.relativedelta import relativedelta
from M_CheckProcess import M_WaitForProcessEnd
from M_SendTelegram import M_telegram_bot_sendtext
from M_FileFunctions import M_GetFileSize
from M_FileFunctions import M_convert_bytes
from M_FileFunctions import M_CleanFileName
from M_FileFunctions import M_CreateDir
from M_FileFunctions import M_MoveFiles

# constants

supportedExtension = ".mkv"
newFolder = "NewFiles"
oldFolder = "OldFiles"
failedFolder = "FailedFiles"
directory = '../QnapTS/Video/English/Latest/test/'
directory = '.'


def diff(t_a, t_b):
    t_diff = relativedelta(t_b, t_a)  # later/end time comes first!
    return '{h}h {m}m {s}s'.format(h=t_diff.hours, m=t_diff.minutes, s=t_diff.seconds)

#print(sys.argv[0])
print('>>> BEGIN:  %s' % os.path.basename(__file__))
totalConversionStartTime = datetime.now()
print('>>> START TIME: %s ' % totalConversionStartTime)

# create results directory
M_CreateDir(newFolder)
M_CreateDir(oldFolder)
M_CreateDir(failedFolder)

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
    filemode='w',
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

logging.info('>>> BEGIN:  %s' % os.path.basename(__file__))
logging.info('>>> START TIME: %s' % totalConversionStartTime)

logging.info('Working on directory: ' + currentDirectory)

logging.debug('>>> Starting loop looking for files in directory')

for filename in os.listdir(directory):
    conversionStartTime = datetime.now()
    logging.info('====================================================================')
    if filename.endswith(supportedExtension):
        if directory == '.':
            directory = ''
        originalFullFilename = "\"" + directory +  filename + "\""
        #f = open(originalFullFilename)
        #lines = f.read()
        #print(originalFullFilename)

        # Tell the log file and Telegram that we are starting on a new file
        logging.info('Working on file : ' + originalFullFilename)
        M_telegram_bot_sendtext("Conversion STARTED - Working on file : " + originalFullFilename)

        positon_of_extension = originalFullFilename.rfind(supportedExtension)
        newFilename = originalFullFilename[:positon_of_extension] + '.HEVC.DTS.mkv"'
        newFilename = M_CleanFileName(newFilename)
        logging.debug("New filename is " + newFilename)
        print("New filename is " + newFilename)

        originalFileSize = M_GetFileSize(originalFullFilename)
        logging.info("Original file size for " + originalFullFilename + " is " + originalFileSize['size'] + originalFileSize['units'] + ' or ' + str(originalFileSize['bytes']) + ' bytes ')
        
        # alternate method to below
        #p = subprocess.Popen(["ping", "-c", "10", "www.cyberciti.biz"], stdout=subprocess.PIPE)
        #output, err = p.communicate()
        #print  output

#        cmd = "ls -la " + originalFullFilename

        cmd = '''
        tail /var/log/omxlog | stdbuf -o0 grep player_new | while read i
        do
            Values=$(omxd S | awk -F/ '{print $NF}')
            x1="${Values}"
            x7="${x1##*_}"
            x8="${x7%.*}"
            echo ${x8}
        done    
        '''

#        cmd = print("M_ConvertToH265.sh %s -o %s" % originalFullFilename newFilename)
        k = sys.argv[0].rfind("/")
        script_name = sys.argv[0][:k+1] + "M_ConvertToH265.sh"
        # =========================================================================
        # =========================================================================
        cmd = script_name + " " + originalFullFilename + " -o /tmp/" + newFilename
        # =========================================================================
        # =========================================================================
        
        logging.debug(cmd)
        # subprocess.check_output(cmd, shell=True)
        
        p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
        while True:
            nextline = p.stderr.read(1)
            if nextline == b'' and p.poll() != None:
                break
            if nextline != b'':
#                sys.stdout.write(nextline)
                sys.stdout.write(nextline.decode(sys.stdout.encoding))
                sys.stdout.flush()
        
        M_WaitForProcessEnd("ffmpeg")
        newFileSize = M_GetFileSize('/tmp/' + newFilename)
        logging.info("New file size for " + newFilename + " is " + newFileSize['size'] + newFileSize['units'] + ' or ' + str(newFileSize['bytes']) + ' bytes')

        # Move a file from the directory d1 to d2
        originalFullFilename = originalFullFilename.replace('"','')  
        newFilename = newFilename.replace('"','')  

        logging.info(">>> Moving original file from " +  originalFullFilename + " to " +  oldFolder+'/'+originalFullFilename)
        M_MoveFiles(originalFullFilename, oldFolder+'/'+originalFullFilename)

        newfile_percent_size = newFileSize['bytes'] / originalFileSize['bytes'] * 100
        if newFileSize['bytes'] > originalFileSize['bytes']:
            # conversion failed, the new file is bigger than the orignal file
            errorMsg = ' - New file is bigger than orignal - Delete new file'
            logging.info("Error: New file size for " + newFilename + " is " + str(newFileSize['bytes']) + " vs " + str(originalFileSize['bytes']))

            # Move a file from the directory d1 to d2
            logging.info(">>> Moving new file from " +  newFilename + " to " +  failedFolder+'/'+newFilename)
            #M_MoveFiles(newFilename, failedFolder+'/'+newFilename)
        else:
            if newfile_percent_size < 15:
                # converted file is only a fraction of the original file, conversion probably failed
                errorMsg = ' - Reduced size is less than 15% - probably not good'
                # Move a file from the directory d1 to d2
                logging.info(">>> Moving new file from " +  newFilename + " to " +  failedFolder+'/'+newFilename)
                #M_MoveFiles(newFilename, failedFolder+'/'+newFilename)
            else:
                # Success - i think
                errorMsg = ''
                # Move a file from the directory d1 to d2
                logging.info(">>> Moving new file from " +  newFilename + " to " +  newFolder+'/'+newFilename)
                M_MoveFiles('/tmp/'+newFilename, newFolder+'/'+newFilename)

        conversionEndTime = datetime.now()
        total_time = diff(conversionStartTime, conversionEndTime)

        M_telegram_bot_sendtext("Completed Conversion: " + originalFullFilename + " from " + originalFileSize['size'] + originalFileSize['units'] + " to " + newFileSize['size'] + newFileSize['units'] + ". Conversion time:  " + total_time + errorMsg)



        print(">>> Conversion END TIME: %s " % conversionEndTime)
        logging.info(">>> Conversion END TIME: %s " % conversionEndTime)

        print(">>> Film Conversion TIME: %s " % total_time)
        logging.info(">>> Film Conversion TIME: %s " % total_time)

        continue
    else:
        logging.warning('Ignoring file: ' + filename)
        # print("Ignoring file: " + filename)

logging.debug('>>> Ending loop looking for files in directory')
totalConversionEndTime = datetime.now()

totalRunTime = diff(totalConversionStartTime, totalConversionEndTime)
print(">>> END TIME: %s " % totalConversionEndTime)
logging.info(">>> END TIME: %s " % totalConversionEndTime)
print(">>> TOTAL SCRIPT EXECUTION TIME: %s " % totalRunTime)
logging.info(">>> TOTAL SCRIPT EXECUTION TIME: %s " % totalRunTime)


print('>>> COMPLETED:  %s' % os.path.basename(__file__))
logging.info('>>> COMPLETED:  %s' % os.path.basename(__file__))
