from os import name
import cv2
import numpy as np
import sys
import random
import json

file_list='./hand_single/labels.txt'
json_path='./hand_single/json_file/'
img_path='./hand_single/JPEGImages/'

def json_w(img_name,landmarks):
    img=cv2.imread(img_path+img_name)

    coco_output = {
        "shapes": [],
        "flags": {}, 
        "version": "4.5.9", 
        "imageData": None
        }
    for item in landmarks:
        list1=[]
        list1.append(int(item[0]))
        list1.append(int(item[1]))
        seg_info = {"shape_type": "point",'points': [list1], "group_id":None ,"label": "1", "flags": {}}
        coco_output["shapes"].append(seg_info)

    coco_output[ "imageHeight"]=img.shape[0]
    coco_output[ "imageWidth"]=img.shape[1]
    coco_output["imagePath"]=str(img_name)
    
    name=img_name.split(".")[0]
    full_path=json_path+name+'.json'
    print(coco_output)
        
    
    with open( full_path, 'w') as f:
        json.dump(coco_output, f)
 

with open(file_list, 'r') as f:
    lines = f.readlines()
    for i,j in enumerate(lines):
        if(len(j)>1):
            c=j.strip().split()
            landmark = np.asarray(c[0:42], dtype=np.float32)
            img_name=c[-1]
            print(img_name,type(landmark) )
            landmarks = landmark.reshape((-1,2))
            json_w(img_name,landmarks)

            

             



