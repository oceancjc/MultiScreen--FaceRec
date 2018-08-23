# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import datetime
from optparse import OptionParser

port = 12345
loglevel = 1
logfile = 'log@{}.txt'.format( datetime.datetime.now().strftime('%Y_%m_%d') )

def printlog(content):
    global loglevel
    timestick ='[{}]'.format( datetime.datetime.now().strftime('%Y-%m-%d %H:%M%S') )
    if loglevel == 1:
        print(timestick + content)
    elif loglevel == 2:
        global logfile
        f = open(logfile,'ab+')
        print(timestick + content,file = logfile) #print into file
        f.close()


def deframer(cmd):
    res = {}
    if 'Facerecognition#$' not in cmd:
        printlog('Invalid cmd')
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
            printlog('ID instance not equal n')
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
    
    global port
    parser.add_option("-p", "--port", 
                      action="store", dest="port",default='12345',type='int',
                      help="Port for UDP server") 
    '''
    parser.add_option("-h", "--help", 
                      action="store", dest="csvname",default='',type='int',
                      help="-p xxx to enable the program with udp server listening at port xxx") 
    '''
    return port
    
    
if __name__ == '__main__':
    port = optiondeal()
    cmd = r'Facerecognition#$111#$222#$hello#$C:\123.png#$5556#$3#$xidada,0#$huge,0#$cjc,0'
    #TODO: Loading the face lib dict
    printlog('Face Recog Start...')
    while True:
        #TODO: recfrom and pickup the sender's address & port
        r = deframer(cmd)
        if len(r) is 1:    
            #TODO: send back an error message to the frame sender, need to know sender's address and port
            continue
        else:
            s = framer(r)
            #TODO: send the frame s to the correspoing address in deframer's result
            printlog( 'Message sent to {}:{}'.format(address,r['port']) )
    
    
    
    
    
    
    
    
    
    
    
    
    
    
