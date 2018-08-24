# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import socket,datetime,time,logging
import sys
from optparse import OptionParser

portg = 12345
loglevelg = 2
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
   


def deframer(cmd):
    res = {}
    if 'Facerecognition#$' not in cmd:
        printlog('ERROR','Invalid cmd')
        res[-1] = 'Invalid cmd'
        return res
    else:
        cmd_s = cmd.split('#$')
        res['subid'] = cmd_s[1]
        res['chnid'] = cmd_s[2]
        res['label'] = cmd_s[3]
        res['file']  = cmd_s[4]
        res['port']  = int( cmd_s[5] )
        res['n']     = int( cmd_s[6] )
        if len(cmd_s) != 7+res['n']:
            printlog('ID instance not equal n','ERROR')
            res = {-2:'ID instance not equal n'}
            return res
        for i in range(res['n']):
            tmp = cmd_s[7+i]
            res[i] = tmp
        return res



def framer(eledict):
    eles = ['Facerecognition', eledict['subid'], eledict['chnid'], eledict['label'], eledict['file'],\
            str(eledict['port']), str(eledict['n'])]
    for i in range(eledict['n']):
        eles.append(eledict[i])
    return '#$'.join(eles)



def optiondeal():
    parser = OptionParser() 
    usage = "usage: %prog [options] arg1 arg2"  
    parser = OptionParser(usage=usage) 
    
    global portg, loglevelg
    parser.add_option("-p", "--port", 
                      action="store", dest="portg",default='12345',type='int',
                      help="Port for UDP server") 
    
    parser.add_option("-l", "--logLevel", 
                      action="store", dest="loglevelg",default='1',type='int',
                      help="Log Enable for program, 0 to disable, 1 to enable") 
    
    return portg, loglevelg
    
    
#if __name__ == '__main__':
portg,loglevelg = optiondeal()
#cmd = r'Facerecognition#$111#$222#$hello#$C:\123.png#$5556#$3#$xidada,0#$huge,0#$cjc,0'
logfileg = 'log@{}@{}.txt'.format(int(portg), datetime.datetime.now().strftime('%Y_%m_%d') )
#TODO: Loading the face lib dict
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    server.bind( ('127.0.0.1',int(portg)) )
except:
    printlog('Can not create UDP socket ... Program Ends', 'ERROR')
    sys.exit()
printlog('Face Recog Start...')
while True:
    data,addr_from = server.recvfrom(32768)
    printlog('+++++ CMD receive: '+str(data))
    r_dict = deframer( str(data) )
    if len(r_dict) is 1: 
        pass
        server.sendto("Not valid, check your command\n".encode('utf-8'),addr_from)
    else:
        s = framer(r_dict)
        #Send the frame s to the correspoing address in deframer's result
        try:
            server.sendto(s.encode('utf-8'), (addr_from[0],r_dict['port']) )
            printlog( 'Message sent to {}:{}'.format(addr_from[0],r_dict['port']) )
        except:
            printlog('Message sent fail: Check the remote address {}:{}'.format(addr_from[0],r_dict['port']),'ERROR')
    printlog(r'----- CMD processing finished ')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
