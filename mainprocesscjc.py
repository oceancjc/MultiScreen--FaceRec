# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from __future__ import print_function
import socket,datetime,pickle
import sys,traceback,os
from optparse import OptionParser
from loggingcjc import printlog
import loggingcjc
from facerecogcjc import faceLike, initFacedetector

import hashlib


portg = 12345
loglevelg = 2
KEY = ":&?`Lb|}7Qd[.th/O2$F9E5s!D)6w'Yn"

def MD5gen(string):
    return hashlib.md5(str(string).encode('utf-8')).hexdigest()
    
    
    
def keyVerify(string,key=''):
    now = datetime.datetime.now()
    secondranges = list(range(-3,4))
    for i in secondranges:
        timestring = ( now + datetime.timedelta(seconds=i) ).strftime('%Y%m%d%H%M%S')
        code = MD5gen(key+timestring)
        if code in string:
            printlog('Verify Success, delta is {}s'.format(i))
            return True
    printlog('Verify Fail, No key matches','ERROR')
    return False
    #timeranges = list( map(lambda x: (now+datetime.timedelta(seconds=x)).strftime('%Y%m%d%H%M%S'),secondranges) )
    


def deframer(cmd):
    res = {}
    if 'Facerecognition#$' not in cmd:
        printlog('Invalid cmd','ERROR')
        res[-1] = 'Invalid cmd'
        return res
    else:
        cmd_s = cmd.split('#$')
        res['subid'] = cmd_s[1]
        res['chnid'] = cmd_s[2]
        res['label'] = cmd_s[3]
        res['file']  = str(cmd_s[4])
        res['port']  = int( cmd_s[5] )
        res['n']     = int( cmd_s[6] )
        if len(cmd_s) != 7+res['n'] + 1:   #20180828 len(cmd_s) is 1 item longer due to the md5 code in the last position
            printlog('ID instance not equal n','ERROR')
            res = {-2:'ID instance not equal n'}
            return res
        for i in range(res['n']):
            tmp = cmd_s[7+i].split(',')[0]
            res[i] = [tmp,0]
        
        res['md5'] = str(cmd_s[-1])
        return res



def framer(eledict,facesDetected_dict):
    eles = ['Facerecognition', eledict['subid'], eledict['chnid'], eledict['label'],str(eledict['n'])]
    for i in range(eledict['n']):
        if eledict[i][0] in facesDetected_dict.keys():
            eles.append( '{},{}'.format(eledict[i][0],
                        round(1-facesDetected_dict[eledict[i][0]], 4) ) )
        else:    eles.append( '{},{}'.format(eledict[i][0],1) )
    return '#$'.join(eles)



def pickInterestLib(frameDict,faceLibDict):
    res = {}
    for i in range(frameDict['n']):
        if frameDict[i][0] in faceLibDict.keys():
            res[frameDict[i][0]] = faceLibDict[frameDict[i][0]]
        else:
            printlog("Target Person not in Lib","WARNING")
    return res


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
    
    (options, args) = parser.parse_args()
    portg = options.portg
    loglevelg = options.loglevelg

#portg,loglevelg = optiondeal()
##cmd = r'Facerecognition#$111#$222#$hello#$D:\Unistar\MultiScreen--FaceRec\test0.png#$5556#$3#$xidada,0#$HuGe,0#$cjc,0'
#logfileg = 'log@{}@{}.txt'.format(int(portg), datetime.datetime.now().strftime('%Y_%m_%d') )
#loglevelg = 2
#loggingcjc.setloglevel(loglevelg)
#loggingcjc.setlogfilePath(logfileg)
#
#try:
#    with open(r'./face lib/face.lib','rb') as f:
#        facelib = pickle.load(f)
#except:
#    printlog(traceback.format_exc(),'ERROR')
#    facelib = {}
#  #r = faceRecog(facelib,'test0.png')
#server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
#try:
#    server.bind( ('127.0.0.1',int(portg)) )
#except:
#    printlog('Can not create UDP socket ... Program Ends', 'ERROR')
#    sys.exit()
#printlog('===================== Face Recog Start =============================')
#printlog("My IP:127.0.0.1:{}\tLog Level:{}".format(portg,loglevelg))
#interestfacelib={}
#faces_dict={}
#faceDetecor = initFacedetector()
#while True:
#    try:
#        data,addr_from = server.recvfrom(32768)
#    except:
#        printlog(traceback.format_exc(),'ERROR')
#        continue
#    printlog('+++++ CMD receive: '+str(data))
#    if 'close' in str(data):   
#        printlog(r'----- CMD processing finished & Program Ends')
#        sys.exit()
#    r_dict = deframer( str(data) )
#    if len(r_dict) is 1: 
#        server.sendto("Not valid, check your command\n".encode('utf-8'),addr_from)
#    elif not facelib:
#        addr2reply = (addr_from[0],r_dict['port'])
#        s = framer(r_dict,{})
#        server.sendto(s.encode('utf-8'), addr2reply )
#        printlog("Send Message to {}:Empyt Face Lib, Please check".format(addr2reply),"WARNING")
#    else:
#        addr2reply = (addr_from[0],r_dict['port'])
#        if not os.path.exists(r_dict['file']):
#            s = framer(r_dict,{})
#            server.sendto(s.encode('utf-8'), addr2reply )
#            #server.sendto("Image to Recog Face Not Exist ...".encode('utf-8'),addr2reply )
#            printlog("Send Message to {}:Image to Recog Face Not Exist ...".format(addr2reply), "ERROR")
#            continue
#        interestfacelib = pickInterestLib(r_dict,facelib)
#        if not interestfacelib:
#            s = framer(r_dict,{})
#            printlog("Interested Faces not in Lib @pickInterestLib","WARNING")
#        else:
#            faces_dict = faceRecog(interestfacelib,r_dict['file'],faceDetecor)
#            s = framer(r_dict,faces_dict)
#        try:
#            server.sendto(s.encode('utf-8'), (addr_from[0],r_dict['port']) )
#            printlog( 'Message sent to {}:{}'.format(addr_from[0],r_dict['port']) )
#        except:
#            printlog('Message sent fail: Check the remote address {}:{}'.format(addr_from[0],r_dict['port']),'ERROR')
#    printlog(r'----- CMD processing finished ')
    


   
if __name__ == '__main__':
    #portg,loglevelg = optiondeal()
    #cmd = r'Facerecognition#$111#$222#$hello#$D:\Unistar\MultiScreen--FaceRec\test0.png#$5556#$3#$xidada,0#$HuGe,0#$cjc,0'
    os.chdir(os.path.split(os.path.realpath(__file__))[0])
    optiondeal()
    logfileg = 'log@{}@{}.txt'.format(int(portg), datetime.datetime.now().strftime('%Y_%m_%d') )
    loggingcjc.setloglevel(loglevelg)
    loggingcjc.setlogfilePath(logfileg)
    
    try:
        with open(r'./face lib/face.lib','rb') as f:
            facelib = pickle.load(f)
    except:
        printlog(traceback.format_exc(),'ERROR')
        facelib = {}
    
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    try:
        server.bind( ('127.0.0.1',int(portg)) )
    except:
        printlog('Can not create UDP socket ... Program Ends', 'ERROR')
        sys.exit()
    printlog('===================== Face Recog Start =============================')
    printlog("My IP:127.0.0.1:{}\tLog Level:{}".format(portg,loglevelg))
    interestfacelib={}
    faces_dict={}
    faceDetecor = initFacedetector()
    while True:
        try:
            data,addr_from = server.recvfrom(32768)
        except:
            printlog(traceback.format_exc(),'ERROR')
            continue
        printlog('+++++ CMD receive: '+str(data))
        if 'close' in str(data):   
            printlog(r'----- CMD processing finished & Program Ends')
            sys.exit()
        r_dict = deframer( str(data) )
        if len(r_dict) is 1: 
            server.sendto("Not valid, check your command".encode('utf-8'),addr_from)
        #20180828: Add keyverify branch to verify the md5string in the last of frame
        elif not keyVerify(r_dict['md5'],KEY):
            server.sendto("Verification failure !".encode('utf-8'),addr_from)
        elif not facelib:
            addr2reply = (addr_from[0],r_dict['port'])
            s = framer(r_dict,{})
            server.sendto(s.encode('utf-8'), addr2reply )
            printlog("Send Message to {}:Empyt Face Lib, Please check".format(addr2reply),"WARNING")
        else:
            addr2reply = (addr_from[0],r_dict['port'])
            if not os.path.exists(r_dict['file']):
                s = framer(r_dict,{})
                server.sendto(s.encode('utf-8'), addr2reply )
                #server.sendto("Image to Recog Face Not Exist ...".encode('utf-8'),addr2reply )
                printlog("Send Message to {}:Image to Recog Face Not Exist ...".format(addr2reply), "ERROR")
                continue
            interestfacelib = pickInterestLib(r_dict,facelib)
            if not interestfacelib:
                s = framer(r_dict,{})
                printlog("Interested Faces not in Lib @pickInterestLib","WARNING")
            else:
                faces_dict = faceLike(interestfacelib,r_dict['file'],faceDetecor)
                s = framer(r_dict,faces_dict)
            try:
                server.sendto(s.encode('utf-8'), (addr_from[0],r_dict['port']) )
                printlog( 'Message sent to {}:{}'.format(addr_from[0],r_dict['port']) )
            except:
                printlog('Message sent fail: Check the remote address {}:{}'.format(addr_from[0],r_dict['port']),'ERROR')
        printlog(r'----- CMD processing finished ')
        
            
    
    
    
    
    
    
    
    
    
    
    
