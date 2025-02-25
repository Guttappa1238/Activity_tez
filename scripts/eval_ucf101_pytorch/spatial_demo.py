#!/usr/bin/env python

import os, sys
import collections
import numpy as np
import cv2
import math
import random
import time
import argparse

import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim
import torch.utils.data
import torchvision.transforms as transforms
import torchvision.datasets as datasets

from sklearn.metrics import confusion_matrix

datasetFolder="../../datasets"
sys.path.insert(0, "../../")
import models
from VideoSpatialPrediction import VideoSpatialPrediction
from VideoTemporalPrediction import VideoTemporalPrediction


os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"   
os.environ["CUDA_VISIBLE_DEVICES"]="1"

model_names = sorted(name for name in models.__dict__
    if name.islower() and not name.startswith("__")
    and callable(models.__dict__[name]))

dataset_names = sorted(name for name in datasets.__all__)

parser = argparse.ArgumentParser(description='PyTorch Two-Stream Action Recognition RGB Test Case')

parser.add_argument('--dataset', '-d', default='window',
                    choices=["ucf101", "hmdb51", "window"],
                    help='dataset: ucf101 | hmdb51')
parser.add_argument('--arch', '-a', metavar='ARCH', default='rgb_resnet18',
                    choices=model_names)
parser.add_argument('-s', '--split', default=6, type=int, metavar='S',
                    help='which split of data to work on (default: 1)')
parser.add_argument('-w', '--window', default=3, type=int, metavar='V',
                    help='validation file index (default: 3)')

parser.add_argument('-t', '--tsn', dest='tsn', action='store_true',
                    help='TSN Mode')

parser.add_argument('-v', '--val', dest='window_val', action='store_true',
                    help='Window Validation Selection')
multiGPUTest=False
def buildModel(model_path,num_categories):
    model = models.__dict__[args.arch](pretrained=False, num_classes=num_categories)
    params = torch.load(model_path)
    if args.tsn:
        new_dict = {k[7:]: v for k, v in params['state_dict'].items()} 
        model_dict=model.state_dict() 
        model_dict.update(new_dict)
        model.load_state_dict(model_dict)
    elif multiGPUTest:
        model=torch.nn.DataParallel(model)
        new_dict={"module."+k: v for k, v in params['state_dict'].items()} 
        model.load_state_dict(new_dict)
    else:
        model.load_state_dict(params['state_dict'])
    model.cuda()
    model.eval()   
    return model


def main():
    global args
    args = parser.parse_args()
    
    if args.tsn:    
        modelLocation="./checkpoint/"+args.dataset+"_tsn_"+args.arch+"_split"+str(args.split)
    else:
        modelLocation="./checkpoint/"+args.dataset+"_"+args.arch+"_split"+str(args.split)

    model_path = os.path.join('../../',modelLocation,'model_best.pth.tar') 
    
    if args.dataset=='ucf101':
        frameFolderName = "ucf101_frames"
    elif args.dataset=='hmdb51':
        frameFolderName = "hmdb51_frames"
    elif args.dataset=='window':
        frameFolderName = "window_frames"
    data_dir=os.path.join(datasetFolder,frameFolderName)
    


    if args.window_val:
        val_fileName = "window%d.txt" %(args.window)
    else:
        if 'rgb' in args.arch:
            val_fileName = "val_rgb_split%d.txt" %(args.split)
        else:
            val_fileName = "val_flow_split%d.txt" %(args.split)

    val_file=os.path.join(datasetFolder,'settings',args.dataset,val_fileName)
    
    start_frame = 0
    if args.dataset=='ucf101':
        num_categories = 101
    elif args.dataset=='hmdb51':
        num_categories = 51
    elif args.dataset=='window':
        num_categories = 3

    model_start_time = time.time()
    spatial_net=buildModel(model_path,num_categories)
    model_end_time = time.time()
    model_time = model_end_time - model_start_time
    print("Action recognition model is loaded in %4.4f seconds." % (model_time))

    
    f_val = open(val_file, "r")
    val_list = f_val.readlines()
    print("we got %d test videos" % len(val_list))

    line_id = 1
    match_count_mean = 0
    match_count_max = 0
    match_count_3_mean = 0
    match_count_5_mean = 0
    match_count_7_mean = 0
    match_count_10_mean = 0
    match_count_30_mean = 0
    match_count_50_mean = 0
    match_count_70_mean = 0
    match_count_100_mean = 0
    y_true=[]
    y_pred_mean=[]
    y_pred_3_mean=[]
    y_pred_5_mean=[]
    y_pred_7_mean=[]
    y_pred_10_mean=[]
    y_pred_30_mean=[]
    y_pred_50_mean=[]
    y_pred_70_mean=[]
    y_pred_100_mean=[]
    y_pred_max=[]
    timeList=[]
    #result_list = []
    for line in val_list:
        line_info = line.split(" ")
        clip_path = os.path.join(data_dir,line_info[0])
        duration = int(line_info[1])
        input_video_label = int(line_info[2]) 
        
        start = time.time()
        
        if 'rgb' in args.arch:
            spatial_prediction = VideoSpatialPrediction(
                    clip_path,
                    spatial_net,
                    num_categories,
                    start_frame,
                    duration)
        else:
            spatial_prediction = VideoTemporalPrediction(
                    clip_path,
                    spatial_net,
                    num_categories,
                    start_frame,
                    duration)
        
        end = time.time()
        estimatedTime=end-start
        timeList.append(estimatedTime)
        avg_spatial_pred_mean = np.mean(spatial_prediction, axis=1)
        avg_spatial_pred_max = np.max(spatial_prediction, axis=1)
        spatial_sorted = np.sort(spatial_prediction, axis=1)
        avg_spatial_sorted_three=np.mean(spatial_sorted[:,-3:],axis=1)
        avg_spatial_sorted_five=np.mean(spatial_sorted[:,-5:],axis=1)
        avg_spatial_sorted_seven=np.mean(spatial_sorted[:,-7:],axis=1)
        avg_spatial_sorted_ten=np.mean(spatial_sorted[:,-10:],axis=1)
        avg_spatial_sorted_thirty=np.mean(spatial_sorted[:,-30:],axis=1)
        avg_spatial_sorted_fifty=np.mean(spatial_sorted[:,-50:],axis=1)
        avg_spatial_sorted_seventy=np.mean(spatial_sorted[:,-70:],axis=1)
        avg_spatial_sorted_hundred=np.mean(spatial_sorted[:,-100:],axis=1)

        pred_index_mean = np.argmax(avg_spatial_pred_mean)
        pred_index_max = np.argmax(avg_spatial_pred_max)
        pred_index_three = np.argmax(avg_spatial_sorted_three)
        pred_index_five = np.argmax(avg_spatial_sorted_five)
        pred_index_seven = np.argmax(avg_spatial_sorted_seven)
        pred_index_ten = np.argmax(avg_spatial_sorted_ten)
        pred_index_thirty = np.argmax(avg_spatial_sorted_thirty)
        pred_index_fifty = np.argmax(avg_spatial_sorted_fifty)
        pred_index_seventy = np.argmax(avg_spatial_sorted_seventy)
        pred_index_hundred = np.argmax(avg_spatial_sorted_hundred)
        
        # print("Estimated Time  %0.4f" % estimatedTime)
        # print("Sample %d/%d: GT: %d, Prediction with mean: %d" % (line_id, len(val_list), input_video_label, pred_index_mean))
        # print("Sample %d/%d: GT: %d, Prediction with max: %d" % (line_id, len(val_list), input_video_label, pred_index_max))
        # print("Sample %d/%d: GT: %d, Prediction with 3-mean: %d" % (line_id, len(val_list), input_video_label, pred_index_three))
        # print("Sample %d/%d: GT: %d, Prediction with 5-mean: %d" % (line_id, len(val_list), input_video_label, pred_index_five))
        # print("Sample %d/%d: GT: %d, Prediction with 7-mean: %d" % (line_id, len(val_list), input_video_label, pred_index_seven))
        # print("Sample %d/%d: GT: %d, Prediction with 10-mean: %d" % (line_id, len(val_list), input_video_label, pred_index_ten))
        # print("Sample %d/%d: GT: %d, Prediction with 30-mean: %d" % (line_id, len(val_list), input_video_label, pred_index_thirty))
        # print("Sample %d/%d: GT: %d, Prediction with 50-mean: %d" % (line_id, len(val_list), input_video_label, pred_index_fifty))
        # print("Sample %d/%d: GT: %d, Prediction with 50-mean: %d" % (line_id, len(val_list), input_video_label, pred_index_seventy))
        # print("Sample %d/%d: GT: %d, Prediction with 100-mean: %d" % (line_id, len(val_list), input_video_label, pred_index_hundred))
        # print("------------------")
        if pred_index_mean == input_video_label:
            match_count_mean += 1
        if pred_index_max == input_video_label:
            match_count_max += 1
        if pred_index_three == input_video_label:
            match_count_3_mean += 1
        if pred_index_five == input_video_label:
            match_count_5_mean += 1
        if pred_index_seven == input_video_label:
            match_count_7_mean += 1
        if pred_index_ten == input_video_label:
            match_count_10_mean += 1
        if pred_index_thirty == input_video_label:
            match_count_30_mean += 1
        if pred_index_fifty == input_video_label:
            match_count_50_mean += 1
        if pred_index_seventy == input_video_label:
            match_count_70_mean += 1
        if pred_index_hundred == input_video_label:
            match_count_100_mean += 1
        line_id += 1
        y_true.append(input_video_label)
        y_pred_mean.append(pred_index_mean)
        y_pred_max.append(pred_index_max)
        y_pred_3_mean.append(pred_index_three)
        y_pred_5_mean.append(pred_index_five)
        y_pred_7_mean.append(pred_index_seven)
        y_pred_10_mean.append(pred_index_ten)
        y_pred_30_mean.append(pred_index_thirty)
        y_pred_50_mean.append(pred_index_fifty)
        y_pred_70_mean.append(pred_index_seventy)
        y_pred_100_mean.append(pred_index_hundred)
        
    print(confusion_matrix(y_true,y_pred_mean))

    print("Accuracy with mean calculation is %4.4f" % (float(match_count_mean)/len(val_list)))
    # print("Accuracy with max calculation is %4.4f" % (float(match_count_max)/len(val_list)))
    # print("Accuracy with 3-mean calculation is %4.4f" % (float(match_count_3_mean)/len(val_list)))
    # print("Accuracy with 5-mean calculation is %4.4f" % (float(match_count_5_mean)/len(val_list)))
    # print("Accuracy with 7-mean calculation is %4.4f" % (float(match_count_7_mean)/len(val_list)))
    # print("Accuracy with 10-mean calculation is %4.4f" % (float(match_count_10_mean)/len(val_list)))
    # print("Accuracy with 30-mean calculation is %4.4f" % (float(match_count_30_mean)/len(val_list)))
    # print("Accuracy with 50-mean calculation is %4.4f" % (float(match_count_50_mean)/len(val_list)))
    # print("Accuracy with 70-mean calculation is %4.4f" % (float(match_count_70_mean)/len(val_list)))
    # print("Accuracy with 100-mean calculation is %4.4f" % (float(match_count_100_mean)/len(val_list)))
    print(modelLocation)
    print("Mean Estimated Time %0.4f" % (np.mean(timeList)))
    resultDict={'y_true':y_true,'y_pred_mean':y_pred_mean,'y_pred_max':y_pred_max,'y_pred_3_mean':y_pred_3_mean,
                'y_pred_5_mean':y_pred_5_mean,'y_pred_7_mean':y_pred_7_mean,'y_pred_10_mean':y_pred_10_mean,
                'y_pred_30_mean':y_pred_30_mean,'y_pred_50_mean':y_pred_50_mean,'y_pred_70_mean':y_pred_70_mean,
                'y_pred_100_mean':y_pred_100_mean}
    
    np.save('results/%s.npy' %(args.dataset+"_tsn_"+args.arch+"_split"+str(args.split)), resultDict) 

if __name__ == "__main__":
    main()




    # # spatial net prediction
    # class_list = os.listdir(data_dir)
    # class_list.sort()
    # print(class_list)

    # class_index = 0
    # match_count = 0
    # total_clip = 1
    # result_list = []

    # for each_class in class_list:
    #     class_path = os.path.join(data_dir, each_class)

    #     clip_list = os.listdir(class_path)
    #     clip_list.sort()

    #     for each_clip in clip_list:
            # clip_path = os.path.join(class_path, each_clip)
            # spatial_prediction = VideoSpatialPrediction(
            #         clip_path,
            #         spatial_net,
            #         num_categories,
            #         start_frame)

            # avg_spatial_pred_fc8 = np.mean(spatial_prediction, axis=1)
            # # print(avg_spatial_pred_fc8.shape)
            # result_list.append(avg_spatial_pred_fc8)
            # # avg_spatial_pred = softmax(avg_spatial_pred_fc8)

            # pred_index = np.argmax(avg_spatial_pred_fc8)
            # print("GT: %d, Prediction: %d" % (class_index, pred_index))

            # if pred_index == class_index:
            #     match_count += 1
#             total_clip += 1

#         class_index += 1

#     print("Accuracy is %4.4f" % (float(match_count)/total_clip))
#     np.save("ucf101_split1_resnet_rgb.npy", np.array(result_list))

# if __name__ == "__main__":
#     main()
