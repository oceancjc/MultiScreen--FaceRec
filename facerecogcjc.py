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

    win = dlib.image_window()

# Now process all the images
    descriptors = []
    face_libs = []
    if os.path.exists(faces_folder_path) == False:
        printlog('Path Not Exist, Pls check... Program Ends','ERROR')
        sys.exit()
    for f in glob.glob(os.path.join(faces_folder_path, "*.png")):
        printlog("Processing file: {}".format(f))
        #img = io.imread(f)
        img = cv2.imread(f)
        face_libs.append(os.path.split(f)[-1][:-4])
        win.clear_overlay()
        win.set_image(img)

        dets = detectfacefromimg(img, 1)
        printlog("Number of faces detected: {}".format(len(dets)))
        if len(dets) > 1:
            printlog('Model Picture shall contain one face only. Skip this...','WARNING')
            continue
    # Now process each face we found.
        for k, d in enumerate(dets):
            shape = predictor(img, d)#d = rectangle
            
            win.clear_overlay()
            win.add_overlay(d)
            #win.add_overlay(shape)
    
            face_descriptor = facerec.compute_face_descriptor(img, shape)
            #print(face_descriptor)
    
            v = np.array(face_descriptor)  
            descriptors.append(v)

            dlib.hit_enter_to_continue()
        
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
        target = cv2.imread(imgpath)[:,:,:3]
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



def faceLike(libdict,imgpath,detector):
    start = time.time()
    
    try:
        target = cv2.imread(imgpath)[:,:,:3]
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
            #if distance[i] < .45:    result_dict[i] = distance[i]
            result_dict[i] = distance[i]
            printlog("Difference to {} is {}".format(i, distance[i]))
    stop = time.time()
    printlog("Time Consumption:{}s".format(stop-start),"INFO")
    return result_dict



import pickle

if __name__ == "__main__":
    logfileg = 'LibGenlog@{}.txt'.format(datetime.datetime.now().strftime('%Y_%m_%d') )
    loggingcjc.setloglevel(1)
    loggingcjc.setlogfilePath(logfileg)
    loggingcjc.setupLog()
    
    faceDetecor = initFacedetector()
    facelib = faceLibGen(r'face lib',faceDetecor)
    if not facelib:
        printlog('Empty Lib ... Program Ends','ERROR')
        sys.exit()
    try:
        with open(r'./face lib/face.lib','wb') as f:
            pickle.dump(facelib,f)
    except:
        printlog(traceback.format_exc(),'ERROR')
        sys.exit()

    

     




