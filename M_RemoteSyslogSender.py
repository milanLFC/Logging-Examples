import logging
import logging.handlers
'''

on RPi open up port 514 for syslog reception

  vi /etc/rsyslog.conf

add

  module(load="imudp")
  input(type="imudp" port="514")

  module(load="imtcp")
  input(type="imtcp" port="514")

restart rsyslog with

  suso systemctl restart rsyslog

check the logfile

  tail -f /var/log/syslog

'''
myLogger = logging.getLogger('syslog')
myLogger.setLevel(logging.INFO)

handler = logging.handlers.SysLogHandler(address=('x.x.x.x',514))

myLogger.addHandler(handler)
myLogger.info("Hello Hello !")

