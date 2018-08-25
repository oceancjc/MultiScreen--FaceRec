# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 23:06:33 2018

@author: oceancjc
"""
import datetime,logging


portg = 12345
loglevelg = 1
logfileg = ''

def printlog(content, title = 'INFO' ):
    global loglevelg
    timestick ='[{} {}]'.format( datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), title )
    if loglevelg == 1:
        print(timestick + content)
    elif loglevelg == 2:
        global logfileg
        f = open(logfileg,'a+')
        print( timestick + content, file = f) #print into file
        f.close()
        print(timestick + content)
        
        

def setupLog(loglevel):
   logger = logging.getLogger() 
   logger.setLevel(logging.INFO)
   formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s')
   if loglevel == 2:
       global logfileg
       handler = logging.FileHandler(logfileg)
       handler.setLevel(logging.INFO)
       handler.setFormatter(formatter)
       logger.addHandler(handler)
   console = logging.StreamHandler()
   console.setLevel(logging.INFO)
   console.setFormatter(formatter)
   logger.addHandler(console)