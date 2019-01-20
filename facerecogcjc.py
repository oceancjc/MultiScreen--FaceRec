# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 14:31:32 2018

"""
from __future__ import print_function
import sys,os,traceback,datetime
import dlib,glob
import cv2
import numpy as np
import time
from optparse import OptionParser
import loggingcjc
from loggingcjc import printlog
        


def initFacedetector():
    detectfacefromimg = dlib.get_frontal_face_detector()
    predictor_path = r"./model/face_feature.bin"
    face_rec_model_path = r"./model/resnet.bin"
    if not os.path.exists(predictor_path):
        printlog('Critical File not found:{}'.format(predictor_path))
        return -1
    if not os.path.exists(face_rec_model_path):
        printlog('Critical File not found:{}'.format(face_rec_model_path))
        return -2    
    predictor = dlib.shape_predictor(predictor_path)
    facerec = dlib.face_recognition_model_v1(face_rec_model_path)
    return detectfacefromimg, predictor, facerec


    
def faceLibGen(faces_folder_path, detector):
    [detectfacefromimg, predictor, facerec] = detector

    #win = dlib.image_window()

# Now process all the images
    descriptors = []
    face_libs = []
    if os.path.exists(faces_folder_path) == False:
        printlog('Path Not Exist, Pls check... Program Ends','ERROR')
        sys.exit()
    for f in glob.glob(os.path.join(faces_folder_path, "*.png")):
        #f = f.encode('gbk')
        printlog("Processing file: {}".format(f))
        #img = io.imread(f)
        img = cv2.imdecode(np.fromfile(f,dtype=np.uint8),-1)[:,:,:3]
        #img = cv2.imread(f)[:,:,:3]
        face_libs.append(os.path.split(f)[-1][:-4])
        #win.clear_overlay()
        #win.set_image(img)
        cv2.imshow("Image",img)
        cv2.waitKey(1)
        dets = detectfacefromimg(img, 1)
        printlog("Number of faces detected: {}".format(len(dets)))
        if len(dets) > 1:
            printlog('Model Picture shall contain one face only. Skip this...','WARNING')
            continue
    # Now process each face we found.
        for k, d in enumerate(dets):
            shape = predictor(img, d)#d = rectangle
            
            #win.clear_overlay()
            #win.add_overlay(d)
            #win.add_overlay(shape)
    
            face_descriptor = facerec.compute_face_descriptor(img, shape)
            #print(face_descriptor)
    
            v = np.array(face_descriptor)  
            descriptors.append(v)

            time.sleep(0.5)
        cv2.destroyAllWindows()
    return dict(zip(face_libs,descriptors))



#def faceRecog1(libdict,imgpath):
#    try:
#        #img = io.imread(imgpath)
#        img = cv2.imread(imgpath)
#    except:
#        printlog("No img found at {}".format(imgpath),'ERROR' )
#        return []
#    detectfacefromimg = dlib.get_frontal_face_detector()
#    predictor_path = r"./model/face_feature.bin"
#    face_rec_model_path = r"./model/resnet.bin"
#    predictor = dlib.shape_predictor(predictor_path)
#    facerec = dlib.face_recognition_model_v1(face_rec_model_path)
#    target = img[:,:,0:3]
#    dets = detectfacefromimg(target, 1)
#    printlog("Number of faces detected: {}".format(len(dets)))
#    results = [['NONE',0.45]]*len(dets)
#    for k, d in enumerate(dets):
#        shape = predictor(target,d)
#        face_descriptor = facerec.compute_face_descriptor(target, shape)
#        v_target = np.array(face_descriptor)
#        
#        distance = {}
#        for i in libdict.keys():
#            distance[i] = np.linalg.norm(libdict[i]-v_target)
#            if distance[i] < results[k][1]:    results[k] = [i,distance[i]]
#            printlog("Difference to {} is {}".format(i, distance[i]))
#    return results


    
def faceRecog(libdict,imgpath,detector):
    start = time.time()
    
    try:
        #target = io.imread(imgpath)[:,:,:3]
        target = cv2.imdecode(np.fromfile(imgpath,dtype=np.uint8),-1)[:,:,:3]
    except:
        printlog(traceback.format_exc(),'ERROR')
        printlog("No img found at {}".format(imgpath),'ERROR' )
        return {}
    [detectfacefromimg, predictor, facerec] = detector

    dets = detectfacefromimg(target, 1)
    printlog("Number of faces detected: {}".format(len(dets)))
    result_dict = {}
    for k, d in enumerate(dets):
        shape = predictor(target,d)
        face_descriptor = facerec.compute_face_descriptor(target, shape)
        v_target = np.array(face_descriptor)
        
        distance = {}
        for i in libdict.keys():
            distance[i] = np.linalg.norm(libdict[i]-v_target)
            if distance[i] < .45:    result_dict[i] = distance[i]
            printlog("Difference to {} is {}".format(i, distance[i]))
    stop = time.time()
    printlog("Time Consumption:{}s".format(stop-start),"INFO")
    return result_dict



def faceLike(libdict,imgpath,detector,maxfaceOnce = 5):
    start = time.time()
    
    try:
        target = cv2.imdecode(np.fromfile(imgpath,dtype=np.uint8),-1)[:,:,:3]
        #target = cv2.imread(imgpath)[:,:,:3]
    except:
        printlog(traceback.format_exc(),'ERROR')
        printlog("No img found at {}".format(imgpath),'ERROR' )
        return {}
    [detectfacefromimg, predictor, facerec] = detector

    dets = detectfacefromimg(target, 1)
    num_faces = len(dets)
    printlog("Number of faces detected: {}".format(num_faces))
    result_dict = {}
    if num_faces > maxfaceOnce:
        printlog("To much faces detected, threashold is {}".format(maxfaceOnce),'ERROR')
        return result_dict
    for k, d in enumerate(dets):
        shape = predictor(target,d)
        face_descriptor = facerec.compute_face_descriptor(target, shape)
        v_target = np.array(face_descriptor)
        
        distance = {}
        for i in libdict.keys():
            distance[i] = np.linalg.norm(libdict[i]-v_target)
            #if distance[i] < .45:    result_dict[i] = distance[i]
            result_dict[i] = distance[i]
            printlog("Difference to {} is {}".format(i, distance[i]))
    stop = time.time()
    printlog("Time Consumption:{}s".format(stop-start),"INFO")
    return result_dict


loglevelg = 1
def optiondeal():
    parser = OptionParser() 
    usage = "usage: %prog [options] arg1 arg2"  
    parser = OptionParser(usage=usage) 
    
    global loglevelg
    
    parser.add_option("-l", "--logLevel", 
                      action="store", dest="loglevelg",default='1',type='int',
                      help="Log Enable for program, 0 to disable, 1 to enable") 
    
    (options, args) = parser.parse_args()
    loglevelg = options.loglevelg
    
    
import pickle

if __name__ == "__main__":
    logfileg = 'LibGenlog@{}.txt'.format(datetime.datetime.now().strftime('%Y_%m_%d') )
    loggingcjc.setloglevel(loglevelg)
    loggingcjc.setlogfilePath(logfileg)
    loggingcjc.setupLog()
    
    faceDetector = initFacedetector()
    if faceDetector == -1 or faceDetector== -2:
        printlog('Critical Error: No AI model exists, Program Ends','ERROR')
        sys.exit()
    facelib = faceLibGen(r'face lib',faceDetector)
    if not facelib:
        printlog('Empty Lib ... Program Ends','ERROR')
        sys.exit()
    try:
        with open(r'./face lib/face.lib','wb') as f:
            pickle.dump(facelib,f)
    except:
        printlog(traceback.format_exc(),'ERROR')
        sys.exit()

    

     




