#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 16:02:52 2019

@author: esat
"""

import os
import sys
import numpy as np
import math
import cv2
import scipy.io as sio

import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim
import torch.utils.data
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torchvision.models as models

sys.path.insert(0, "../../")
import video_transforms

soft=nn.Softmax(dim=1)
def VideoSpatialPrediction_lstm2(
        vid_name,
        net,
        num_categories,
        start_frame=0,
        num_frames=0,
        num_seg=16
        ):

    if num_frames == 0:
        imglist = os.listdir(vid_name)
        newImageList=[]
        for item in imglist:
            if 'img' in item:
               newImageList.append(item) 
        duration = len(newImageList)
    else:
        duration = num_frames

    clip_mean = [0.485, 0.456, 0.406]
    clip_std = [0.229, 0.224, 0.225]
    normalize = video_transforms.Normalize(mean=clip_mean,
                                     std=clip_std)
    
    val_transform = video_transforms.Compose([
            video_transforms.ToTensor(),
            normalize,
        ])

    # selection
    #step = int(math.floor((duration-1)/(num_samples-1)))
    dims = (224,224,3,duration)
    dims = (256,340,3,duration)
    average_duration = int(duration / num_seg)
    offsets = []
    for seg_id in range(num_seg):
        offsets.append(int((average_duration - 1 + 1)/2 + seg_id * average_duration))
    imageList=[]
    imageList1=[]
    imageList2=[]
    imageList3=[]
    imageList4=[]    
    imageList5=[]  
    imageList6=[]
    imageList7=[]
    imageList8=[]
    imageList9=[]    
    imageList10=[]  
    interpolation = cv2.INTER_LINEAR
    
    for index in offsets:
        img_file = os.path.join(vid_name, 'img_{0:05d}.jpg'.format(index+1))
        img = cv2.imread(img_file, cv2.IMREAD_UNCHANGED)
        img = cv2.resize(img, dims[1::-1],interpolation)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_flip = img[:,::-1,:].copy()
        imageList1.append(img[16:240, 60:284, :])
        imageList2.append(img[:224, :224, :])
        imageList3.append(img[:224, -224:, :])
        imageList4.append(img[-224:, :224, :])
        imageList5.append(img[-224:, -224:, :])
        imageList6.append(img_flip[16:240, 60:284, :])
        imageList7.append(img_flip[:224, :224, :])
        imageList8.append(img_flip[:224, -224:, :])
        imageList9.append(img_flip[-224:, :224, :])
        imageList10.append(img_flip[-224:, -224:, :])


    imageList=imageList1+imageList2+imageList3+imageList4+imageList5+imageList6+imageList7+imageList8+imageList9+imageList10
    
    rgb_list=[]     

    for i in range(len(imageList)):
        cur_img = imageList[i]
        cur_img_tensor = val_transform(cur_img)
        rgb_list.append(np.expand_dims(cur_img_tensor.numpy(), 0))
         
    input_data=np.concatenate(rgb_list,axis=0)   
    with torch.no_grad():
        imgDataTensor = torch.from_numpy(input_data).type(torch.FloatTensor).cuda()
        output = net(imgDataTensor)
#        outputSoftmax=soft(output)
        result = output.data.cpu().numpy()
        prediction=np.argmax(np.mean(result,0))
        
    return prediction
