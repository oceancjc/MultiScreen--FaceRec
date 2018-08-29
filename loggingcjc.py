# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 23:06:33 2018

@author: oceancjc
"""
from __future__ import print_function
import datetime,logging


loglevelg = 1
logfileg = ''
logger = 0



def setloglevel(level):
    global loglevelg
    loglevelg = level
    
    
    
def getloglevel():
    global loglevelg
    return loglevelg



def setlogfilePath(path):
    global logfileg
    logfileg = path
    
    
    
def getlogfilePath():
    global logfileg
    return logfileg    


#
#def printlog(content, title = 'INFO' ):
#    global loglevelg
#    timestick ='[{} {}]'.format( datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), title )
#    if loglevelg == 1:
#        print(timestick + content)
#    elif loglevelg == 2:
#        global logfileg
#        f = open(logfileg,'a+')
#        print( timestick + content, file = f) #print into file
#        f.close()
#        print(timestick + content)
        
        

def setupLog():
    global logger,loglevelg,logfileg
    logger = logging.getLogger('cjc') 
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s %(levelname)s] %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
    if loglevelg == 2:
        handler = logging.FileHandler(logfileg)
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    elif loglevelg == 88:
        handler = logging.FileHandler(logfileg)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(formatter)
        logger.addHandler(console)
        return 

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger.addHandler(console)
    
    
    
    
def printlog(content, title = 'INFO'):
    global logger
    if 'INFO'    in title:    logger.info(content)
    elif 'ERR'   in title:    logger.error(content)
    elif 'WARN'  in title:    logger.warning(content)
    elif 'DEBUG' in title:    logger.debug(content)
       
   
   
   