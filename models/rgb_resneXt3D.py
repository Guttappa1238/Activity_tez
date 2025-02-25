#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 11:45:05 2019

@author: esat
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import math
from functools import partial
from .NLB.NLBlockND import NLBlockND

from .BERT.bert import BERT, BERT2, BERT3, BERT4, BERT5, BERT6
from .BERT.embedding import BERTEmbedding
__all__ = ['rgb_resneXt3D64f101','rgb_resneXt3D64f101_bert10XX','rgb_resneXt3D64f101_bert10XY','rgb_resneXt3D16f101'
           ,'rgb_resneXt3D64f101_bert10XY2'
           ,'rgb_resneXt3D64f101_16fweight','rgb_resneXt3D64f101_bert10XY_16fweight','rgb_resneXt3D64f101_bert10XY_nonPreTrained',
           'rgb_mars_resnext3D64f101', 'flow_mars_resnext3D64f101', 'flow_resneXt3D64f101', 'rgb_resneXt3D64f101_224', 
           'rgb_resneXt3D64f101_student_mars', 'rgb_resneXt3D64f101_student_MARS',
           'flow_resneXt3D64f101_bert10XY', 'flow_resneXt3D64f101_bert10S', 'rgb_resneXt3D64f101_bert10S', 
           'rgb_resneXt3D64f101_bert10XYS', 'rgb_resneXt3D64f101_bert2S', 'flow_resneXt3D64f101_bert2S', 'flow_resneXt3D64f101_bert10SS',
           'rgb_resneXt3D64f101_bert', 'rgb_resneXt3D64f101_bert10S_MARS', 
           'rgb_resneXt3D64f101_bert10B_MARS', 'rgb_resneXt3D64f101_bert10S_MARS2', 'rgb_resneXt3D64f101_bert10S_MARS3'
           ,'rgb_resneXt3D64f101_bert10S_MARS4', 'rgb_resneXt3D64f101_bert10S_MARS5', 'rgb_resneXt3D64f101_bert10S_MARS6',
           'rgb_resneXt3D64f101_bert10S_MARS7', 'rgb_resneXt3D64f101_pooling3', 
           'rgb_resneXt3D64f101_pooling', 'rgb_resneXt3D64f101_NLB', 'rgb_resneXt3D64f101_lstm', 'rgb_resneXt3D64f101_adamw'
           , 'rgb_resneXt3D64f101_adamw_modified', 'rgb_resneXt3D64f101_lstm2', 'rgb_resneXt3D64f101_NLB2'
           , 'rgb_resneXt3D64f101_pooling2', 'rgb_resneXt3D64f101_NLB3', 'rgb_resneXt3D64f101_NLB4'
           , 'rgb_resneXt3D64f101_bert10SS_MARS', 'rgb_resneXt3D64f101_bert10SS_MARS_copy', 'rgb_resneXt3D64f101_bert10SS_MARS5'
           , 'rgb_resneXt3D64f101_bert10SS_MARS6', 'rgb_resneXt3D64f101_bert10SS_MARS_copy2', 'rgb_resneXt3D64f101_bert10SS_MARS_copy3'
           ,'rgb_resneXt3D64f101_bert10S2', 'rgb_resneXt3D64f101_bert10S_single_head', 'rgb_resneXt3D64f101_bertS'
           ]


class rgb_resneXt3D64f101(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101, self).__init__()
        self.num_classes=num_classes
        self.dp = nn.Dropout(p=0.8)
        

        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-1])
        
        self.fc_action = nn.Linear(2048, num_classes)
        for param in self.features.parameters():
            param.requires_grad = True
                
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.dp(x)
        x = self.fc_action(x)
        return x
    
    
class rgb_resneXt3D64f101_224(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_224, self).__init__()
        self.num_classes=num_classes
        self.dp = nn.Dropout(p=0.8)
        

        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=224, sample_duration=64).children())[:-1])
        
        self.fc_action = nn.Linear(2048, num_classes)
        for param in self.features.parameters():
            param.requires_grad = True
                
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.dp(x)
        x = self.fc_action(x)
        return x
    

    
class rgb_resneXt3D64f101_student_mars(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_student_mars, self).__init__()
        self.num_classes=num_classes
        self.dp = nn.Dropout(p=0.8)
        

        self.features=nn.Sequential(*list(_trained_resnext101(model_path = modelPath, sample_size=112, sample_duration=64).children())[:-1])
        
        self.fc_action = nn.Linear(2048, num_classes)
        for param in self.features.parameters():
            param.requires_grad = True
                
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.dp(x)
        x = self.fc_action(x)
        return x        
    def student_forward(self, x):
        features = self.features(x)
        features = features.view(features.size(0), -1)
        x = self.dp(features)
        x = self.fc_action(x)
        return x, features
    def mars_forward(self, x):
        features = self.features(x)
        features = features.view(features.size(0), -1)
        return features
    
class rgb_resneXt3D64f101_student_MARS(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_student_MARS, self).__init__()
        self.num_classes=num_classes
        self.dp = nn.Dropout(p=0.8)
        

        self.features=nn.Sequential(*list(_trained_resnext101(model_path = modelPath, sample_size=112, sample_duration=64).children())[:-1])
        
        self.fc_action = nn.Linear(2048, num_classes)
        for param in self.features.parameters():
            param.requires_grad = True
                
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.dp(x)
        x = self.fc_action(x)
        return x        
    def student_forward(self, x):
        features = self.features(x)
        features = features.view(features.size(0), -1)
        x = self.dp(features)
        x = self.fc_action(x)
        return x, features
    def mars_forward(self, x):
        features = self.features(x)
        features = features.view(features.size(0), -1)
        return features
    
class flow_resneXt3D64f101(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(flow_resneXt3D64f101, self).__init__()
        self.num_classes=num_classes
        self.dp = nn.Dropout(p=0.7)
        

        self.features=nn.Sequential(*list(_trained_resnext101_flow(model_path_flow=modelPath, \
            sample_size=112, sample_duration=64).children())[:-1])
        
        self.fc_action = nn.Linear(2048, num_classes)
        for param in self.features.parameters():
            param.requires_grad = True
                
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.dp(x)
        x = self.fc_action(x)
        return x
    def mars_forward(self, x):
        features = self.features(x)
        features = features.view(features.size(0), -1)
        return features


class rgb_resneXt3D16f101(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D16f101, self).__init__()
        self.num_classes=num_classes
        self.dp = nn.Dropout(p=0.8)
        

        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=16).children())[:-1])
        
        self.fc_action = nn.Linear(2048, num_classes)
        for param in self.features.parameters():
            param.requires_grad = True
                
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.dp(x)
        x = self.fc_action(x)
        return x
    
class rgb_resneXt3D64f101_16fweight(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_16fweight, self).__init__()
        self.num_classes=num_classes
        self.dp = nn.Dropout(p=0.8)
        

        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-1])
        
        self.fc_action = nn.Linear(2048, num_classes)
        for param in self.features.parameters():
            param.requires_grad = True
                
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.dp(x)
        x = self.fc_action(x)
        return x

class rgb_resneXt3D64f101_bert10XX(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_bert10XX, self).__init__()
        self.hidden_size=2048
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        

        self.features1=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-3])
        self.features2=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[-3:-1])
        self.bert = BERT5(self.hidden_size,length, hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        print(sum(p.numel() for p in self.bert.parameters() if p.requires_grad))
        self.fc_action = nn.Linear(self.hidden_size, num_classes)
            
        for param in self.features1.parameters():
            param.requires_grad = False
            
        for param in self.features2.parameters():
            param.requires_grad = True
                
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features1(x)
        x = self.features2(x)
        x = x.view(x.size(0), -1)
        x = x.view(-1,self.length,self.hidden_size)
        input_vectors=x
        output , maskSample = self.bert(x)
        classificationOut = output[:,0,:]
        sequenceOut=output[:,1:,:]
        output=self.dp(classificationOut)
        x = self.fc_action(output)
        return x, input_vectors, sequenceOut, maskSample
    
    
class rgb_resneXt3D64f101_bert10XY(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_bert10XY, self).__init__()
        self.hidden_size=2048
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features1=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-3])
        self.features2=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[-3:-2])
        self.bert = BERT5(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        print(sum(p.numel() for p in self.bert.parameters() if p.requires_grad))
        self.fc_action = nn.Linear(self.hidden_size, num_classes)
            
        for param in self.features1.parameters():
            param.requires_grad = True
            
        for param in self.features2.parameters():
            param.requires_grad = True
            
        numberofparam_feature1 = sum(p.numel() for p in self.features1.parameters() if p.requires_grad)
        numberofparam_feature2 = sum(p.numel() for p in self.features2.parameters() if p.requires_grad)
        total_parameters = numberofparam_feature1 + numberofparam_feature2
        print('total parameters of the backbone architecture: %d' %(total_parameters))
                
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features1(x)
        x = self.features2(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        input_vectors=x
        output , maskSample = self.bert(x)
        classificationOut = output[:,0,:]
        sequenceOut=output[:,1:,:]
        output=self.dp(classificationOut)
        x = self.fc_action(output)
        return x, input_vectors, sequenceOut, maskSample
    
class flow_resneXt3D64f101_bert10XY(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(flow_resneXt3D64f101_bert10XY, self).__init__()
        self.hidden_size=2048
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.7)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101_flow(model_path_flow=modelPath, \
            sample_size=112, sample_duration=64).children())[:-2])
        self.bert = BERT5(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        print(sum(p.numel() for p in self.bert.parameters() if p.requires_grad))
        self.fc_action = nn.Linear(self.hidden_size, num_classes)
            
        for param in self.features.parameters():
            param.requires_grad = True

                
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        input_vectors=x
        output , maskSample = self.bert(x)
        classificationOut = output[:,0,:]
        sequenceOut=output[:,1:,:]
        output=self.dp(classificationOut)
        x = self.fc_action(output)
        return x, input_vectors, sequenceOut, maskSample
    
class rgb_resneXt3D64f101_bert10XY_nonPreTrained(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_bert10XY_nonPreTrained, self).__init__()
        self.hidden_size=2048
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features1=nn.Sequential(*list(resnext3D101(sample_size=112, sample_duration=64).children())[:-3])
        self.features2=nn.Sequential(*list(resnext3D101(sample_size=112, sample_duration=64).children())[-3:-2])
        self.bert = BERT5(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        print(sum(p.numel() for p in self.bert.parameters() if p.requires_grad))
        self.fc_action = nn.Linear(self.hidden_size, num_classes)
            
        for param in self.features1.parameters():
            param.requires_grad = True
            
        for param in self.features2.parameters():
            param.requires_grad = True
                
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features1(x)
        x = self.features2(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        input_vectors=x
        output , maskSample = self.bert(x)
        classificationOut = output[:,0,:]
        sequenceOut=output[:,1:,:]
        output=self.dp(classificationOut)
        x = self.fc_action(output)
        return x, input_vectors, sequenceOut, maskSample
    
class rgb_resneXt3D64f101_bert10XY_16fweight(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_bert10XY_16fweight, self).__init__()
        self.hidden_size=2048
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features1=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-3])
        self.features2=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[-3:-2])
        self.bert = BERT5(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        print(sum(p.numel() for p in self.bert.parameters() if p.requires_grad))
        self.fc_action = nn.Linear(self.hidden_size, num_classes)
            
        for param in self.features1.parameters():
            param.requires_grad = True
            
        for param in self.features2.parameters():
            param.requires_grad = True
                
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features1(x)
        x = self.features2(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        input_vectors=x
        output , maskSample = self.bert(x)
        classificationOut = output[:,0,:]
        sequenceOut=output[:,1:,:]
        output=self.dp(classificationOut)
        x = self.fc_action(output)
        return x, input_vectors, sequenceOut, maskSample
    
    
class rgb_resneXt3D64f101_bert10XYS(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_bert10XYS, self).__init__()
        self.hidden_size=2048
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features1=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-3])
        self.features2=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[-3:-2])
        self.bert = BERT3(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        print(sum(p.numel() for p in self.bert.parameters() if p.requires_grad))
        self.fc_action = nn.Linear(self.hidden_size, num_classes)
            
        for param in self.features1.parameters():
            param.requires_grad = True
            
        for param in self.features2.parameters():
            param.requires_grad = True
                
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features1(x)
        x = self.features2(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        input_vectors=x
        output , maskSample = self.bert(x)
        classificationOut = output[:,0,:]
        sequenceOut=output[:,1:,:]
        output=self.dp(classificationOut)
        x = self.fc_action(output)
        return x, input_vectors, sequenceOut, maskSample
    
class rgb_resneXt3D64f101_bert10XY2(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_bert10XY2, self).__init__()
        self.hidden_size=512
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                512,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(512))

        self.mapper = ResNeXtBottleneck(2048, 256, cardinality = 32, stride = 1, downsample = downsample)

        for m in self.mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()      
                
        self.bert = BERT5(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        print(sum(p.numel() for p in self.bert.parameters() if p.requires_grad))
        
        self.fc_action = nn.Linear(self.hidden_size, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.mapper(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        input_vectors=x
        norm = input_vectors.norm(p=2, dim = -1, keepdim=True)
        input_vectors = input_vectors.div(norm)
        output , maskSample = self.bert(x)
        classificationOut = output[:,0,:]
        sequenceOut=output[:,1:,:]
        norm = sequenceOut.norm(p=2, dim = -1, keepdim=True)
        sequenceOut = sequenceOut.div(norm)
        output=self.dp(classificationOut)
        x = self.fc_action(output)
        return x, input_vectors, sequenceOut, maskSample
    
    
class rgb_resneXt3D64f101_bert10S(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_bert10S, self).__init__()
        self.hidden_size=512
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                512,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(512))

        mapper = ResNeXtBottleneck(2048, 256, cardinality = 32, stride = 1, downsample = downsample)

        for m in mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()   
                
        self.features[7][2] = mapper
                
        self.bert = BERT5(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        print(sum(p.numel() for p in self.bert.parameters() if p.requires_grad))
        
        self.fc_action = nn.Linear(self.hidden_size, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        input_vectors=x
        norm = input_vectors.norm(p=2, dim = -1, keepdim=True)
        input_vectors = input_vectors.div(norm)
        output , maskSample = self.bert(x)
        classificationOut = output[:,0,:]
        sequenceOut=output[:,1:,:]
        norm = sequenceOut.norm(p=2, dim = -1, keepdim=True)
        sequenceOut = sequenceOut.div(norm)
        output=self.dp(classificationOut)
        x = self.fc_action(output)
        return x, input_vectors, sequenceOut, maskSample
    
class rgb_resneXt3D64f101_bertS(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_bertS, self).__init__()
        self.hidden_size=512
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                512,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(512))

        mapper = ResNeXtBottleneck(2048, 256, cardinality = 32, stride = 1, downsample = downsample)

        for m in mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()   
                
        self.features[7][2] = mapper
                
        self.bert = BERT(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        print(sum(p.numel() for p in self.bert.parameters() if p.requires_grad))
        
        self.fc_action = nn.Linear(self.hidden_size, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        input_vectors=x
        norm = input_vectors.norm(p=2, dim = -1, keepdim=True)
        input_vectors = input_vectors.div(norm)
        output , maskSample = self.bert(x)
        classificationOut = output[:,0,:]
        sequenceOut=output[:,1:,:]
        norm = sequenceOut.norm(p=2, dim = -1, keepdim=True)
        sequenceOut = sequenceOut.div(norm)
        output=self.dp(classificationOut)
        x = self.fc_action(output)
        return x, input_vectors, sequenceOut, maskSample
    
    
class rgb_resneXt3D64f101_bert10S_single_head(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_bert10S_single_head, self).__init__()
        self.hidden_size=512
        self.n_layers=1
        self.attn_heads=1
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                512,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(512))

        mapper = ResNeXtBottleneck(2048, 256, cardinality = 32, stride = 1, downsample = downsample)

        for m in mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()   
                
        self.features[7][2] = mapper
                
        self.bert = BERT5(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        print(sum(p.numel() for p in self.bert.parameters() if p.requires_grad))
        
        self.fc_action = nn.Linear(self.hidden_size, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        input_vectors=x
        norm = input_vectors.norm(p=2, dim = -1, keepdim=True)
        input_vectors = input_vectors.div(norm)
        output , maskSample = self.bert(x)
        classificationOut = output[:,0,:]
        sequenceOut=output[:,1:,:]
        norm = sequenceOut.norm(p=2, dim = -1, keepdim=True)
        sequenceOut = sequenceOut.div(norm)
        output=self.dp(classificationOut)
        x = self.fc_action(output)
        return x, input_vectors, sequenceOut, maskSample

class rgb_resneXt3D64f101_bert10S2(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_bert10S2, self).__init__()
        self.hidden_size=512
        self.n_layers=2
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                512,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(512))

        mapper = ResNeXtBottleneck(2048, 256, cardinality = 32, stride = 1, downsample = downsample)

        for m in mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()   
                
        self.features[7][2] = mapper
                
        self.bert = BERT5(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        print(sum(p.numel() for p in self.bert.parameters() if p.requires_grad))
        
        self.fc_action = nn.Linear(self.hidden_size, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        input_vectors=x
        norm = input_vectors.norm(p=2, dim = -1, keepdim=True)
        input_vectors = input_vectors.div(norm)
        output , maskSample = self.bert(x)
        classificationOut = output[:,0,:]
        sequenceOut=output[:,1:,:]
        norm = sequenceOut.norm(p=2, dim = -1, keepdim=True)
        sequenceOut = sequenceOut.div(norm)
        output=self.dp(classificationOut)
        x = self.fc_action(output)
        return x, input_vectors, sequenceOut, maskSample
    
class flow_resneXt3D64f101_bert10SS(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(flow_resneXt3D64f101_bert10SS, self).__init__()
        self.hidden_size=512
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101_flow(model_path_flow=modelPath, \
            sample_size=112, sample_duration=64).children())[:-2])
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                512,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(512))

        mapper = ResNeXtBottleneck(2048, 256, cardinality = 32, stride = 1, downsample = downsample)

        for m in mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()   
                
        self.features[7][2] = mapper
                
        self.bert = BERT5(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        print(sum(p.numel() for p in self.bert.parameters() if p.requires_grad))
        
        self.fc_action = nn.Linear(self.hidden_size, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        input_vectors=x
        norm = input_vectors.norm(p=2, dim = -1, keepdim=True)
        input_vectors = input_vectors.div(norm)
        output , maskSample = self.bert(x)
        classificationOut = output[:,0,:]
        sequenceOut=output[:,1:,:]
        norm = sequenceOut.norm(p=2, dim = -1, keepdim=True)
        sequenceOut = sequenceOut.div(norm)
        output=self.dp(classificationOut)
        x = self.fc_action(output)
        return x, input_vectors, sequenceOut, maskSample
    
    
class rgb_resneXt3D64f101_bert(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_bert, self).__init__()
        self.hidden_size=512
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                512,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(512))

        self.mapper = ResNeXtBottleneck(2048, 256, cardinality = 32, stride = 1, downsample = downsample)

        for m in self.mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()      
                
        self.bert = BERT(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        print(sum(p.numel() for p in self.bert.parameters() if p.requires_grad))
        
        self.fc_action = nn.Linear(self.hidden_size, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        nn.init.normal_(self.fc_action.weight, mean=0, std = 0.02)
        #torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.mapper(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        input_vectors=x
        output , maskSample = self.bert(x)
        classificationOut = output[:,0,:]
        sequenceOut=output[:,1:,:]
        output=self.dp(classificationOut)
        x = self.fc_action(output)
        return x, input_vectors, sequenceOut, maskSample
    
class rgb_resneXt3D64f101_bert2S(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_bert2S, self).__init__()
        self.hidden_size=512
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                512,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(512))

        self.mapper = ResNeXtBottleneck(2048, 256, cardinality = 32, stride = 1, downsample = downsample)

        for m in self.mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()      
                
        self.bert = BERT2(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        
        self.fc_action = nn.Linear(self.hidden_size, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.mapper(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        norm = x.norm(p=2, dim = -1, keepdim=True)
        x = x.div(norm)
        input_vectors=x
        output , maskSample = self.bert(x)
        classificationOut = output[:,0,:]
        sequenceOut=output[:,1:,:]
        output=self.dp(classificationOut)
        x = self.fc_action(output)
        return x, input_vectors, sequenceOut, maskSample
    
class flow_resneXt3D64f101_bert2S(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(flow_resneXt3D64f101_bert2S, self).__init__()
        self.hidden_size=512
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101_flow(model_path_flow=modelPath, \
            sample_size=112, sample_duration=64).children())[:-2])
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                512,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(512))

        self.mapper = ResNeXtBottleneck(2048, 256, cardinality = 32, stride = 1, downsample = downsample)

        for m in self.mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()      
                
        self.bert = BERT2(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        
        self.fc_action = nn.Linear(self.hidden_size, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.mapper(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        norm = x.norm(p=2, dim = -1, keepdim=True)
        x = x.div(norm)
        input_vectors=x
        output , maskSample = self.bert(x)
        classificationOut = output[:,0,:]
        sequenceOut=output[:,1:,:]
        output=self.dp(classificationOut)
        x = self.fc_action(output)
        return x, input_vectors, sequenceOut, maskSample
    
class flow_resneXt3D64f101_bert10S(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(flow_resneXt3D64f101_bert10S, self).__init__()
        self.hidden_size=512
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101_flow(model_path_flow=modelPath, \
            sample_size=112, sample_duration=64).children())[:-2])
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                512,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(512))

        self.mapper = ResNeXtBottleneck(2048, 256, cardinality = 32, stride = 1, downsample = downsample)

        for m in self.mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()      
                
        self.bert = BERT5(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        
        self.fc_action = nn.Linear(self.hidden_size, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.mapper(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        input_vectors=x
        norm = input_vectors.norm(p=2, dim = -1, keepdim=True)
        input_vectors = input_vectors.div(norm)
        output , maskSample = self.bert(x)
        classificationOut = output[:,0,:]
        sequenceOut=output[:,1:,:]
        norm = sequenceOut.norm(p=2, dim = -1, keepdim=True)
        sequenceOut = sequenceOut.div(norm)
        output=self.dp(classificationOut)
        x = self.fc_action(output)
        return x, input_vectors, sequenceOut, maskSample
    
    
class rgb_resneXt3D64f101_bert10S_MARS(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_bert10S_MARS, self).__init__()
        self.hidden_size=512
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                512,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(512))

        self.mapper = ResNeXtBottleneck(2048, 256, cardinality = 32, stride = 1, downsample = downsample)

        for m in self.mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()      
                
        self.bert = BERT5(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        print(sum(p.numel() for p in self.bert.parameters() if p.requires_grad))
        
        self.fc_action = nn.Linear(self.hidden_size, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.mapper(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        input_vectors=x
        norm = input_vectors.norm(p=2, dim = -1, keepdim=True)
        input_vectors = input_vectors.div(norm)
        output , maskSample = self.bert(x)
        classificationOut = output[:,0,:]
        sequenceOut=output[:,1:,:]
        norm = sequenceOut.norm(p=2, dim = -1, keepdim=True)
        sequenceOut = sequenceOut.div(norm)
        output=self.dp(classificationOut)
        x = self.fc_action(output)
        return x, input_vectors, sequenceOut, maskSample
    
    
class rgb_resneXt3D64f101_bert10S_MARS2(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_bert10S_MARS2, self).__init__()
        self.hidden_size=512
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                512,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(512))

        self.mapper = ResNeXtBottleneck(2048, 256, cardinality = 32, stride = 1, downsample = downsample)

        for m in self.mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()      
                
        self.bert = BERT5(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        print(sum(p.numel() for p in self.bert.parameters() if p.requires_grad))
        
        self.fc_action = nn.Linear(self.hidden_size, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.mapper(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        input_vectors=x
        norm = input_vectors.norm(p=2, dim = -1, keepdim=True)
        input_vectors = input_vectors.div(norm)
        output , maskSample = self.bert(x)
        classificationOut = output[:,0,:]
        sequenceOut=output[:,1:,:]
        norm = sequenceOut.norm(p=2, dim = -1, keepdim=True)
        sequenceOut = sequenceOut.div(norm)
        output=self.dp(classificationOut)
        x = self.fc_action(output)
        return x, input_vectors, sequenceOut, maskSample
    
class rgb_resneXt3D64f101_bert10S_MARS3(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_bert10S_MARS3, self).__init__()
        self.hidden_size=512
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                512,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(512))

        self.mapper = ResNeXtBottleneck(2048, 256, cardinality = 32, stride = 1, downsample = downsample)

        for m in self.mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()      
                
        self.bert = BERT5(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        
        self.bert_mars = BERT5(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        
        self.fc_action_mars = nn.Linear(self.hidden_size, num_classes)
        self.fc_action = nn.Linear(self.hidden_size, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
        torch.nn.init.xavier_uniform_(self.fc_action_mars.weight)
        self.fc_action_mars.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.mapper(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        input_vectors=x
        norm = input_vectors.norm(p=2, dim = -1, keepdim=True)
        input_vectors = input_vectors.div(norm)
        
        output_mars , maskSample = self.bert_mars(x)
        classificationOut_mars = output_mars[:,0,:]
        sequenceOut_mars = output_mars[:,1:,:]
        norm = sequenceOut_mars.norm(p=2, dim = -1, keepdim=True)
        sequenceOut_mars = sequenceOut_mars.div(norm)
        output_mars = self.dp(classificationOut_mars)
        x_mars = self.fc_action_mars(output_mars)
        
        output , maskSample = self.bert(x)
        classificationOut = output[:,0,:]
        output = self.dp(classificationOut)
        x = self.fc_action_mars(output)
        
        out = x + x_mars
        
        return out, input_vectors, sequenceOut_mars, maskSample
    
    
class rgb_resneXt3D64f101_bert10S_MARS4(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_bert10S_MARS4, self).__init__()
        self.teacher_size = 512
        self.student_self_size = 256
        self.hidden_size = self.teacher_size + self.student_self_size
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                self.hidden_size,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(self.hidden_size))

        self.mapper = ResNeXtBottleneck(2048, int(self.hidden_size / 2), cardinality = 32, stride = 1, downsample = downsample)

        for m in self.mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()      
                
        self.bert = BERT5(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        print(sum(p.numel() for p in self.bert.parameters() if p.requires_grad))
        
        self.fc_action = nn.Linear(self.hidden_size, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.mapper(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        input_vectors=x
        norm = input_vectors.norm(p=2, dim = -1, keepdim=True)
        input_vectors = input_vectors.div(norm)
        output , maskSample = self.bert(x)
        classificationOut = output[:,0,:]
        sequenceOut=output[:,1:,:self.teacher_size]
        norm = sequenceOut.norm(p=2, dim = -1, keepdim=True)
        sequenceOut = sequenceOut.div(norm)
        output=self.dp(classificationOut)
        x = self.fc_action(output)
        return x, input_vectors, sequenceOut, maskSample
    
class rgb_resneXt3D64f101_bert10S_MARS5(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_bert10S_MARS5, self).__init__()
        self.hidden_size=512
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                512,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(512))

        self.mapper = ResNeXtBottleneck(2048, 256, cardinality = 32, stride = 1, downsample = downsample)

        for m in self.mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()      
                
        self.bert_mars1 = BERT5(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        
        self.bert_mars2 = BERT5(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        
        self.fc_action_mars1 = nn.Linear(self.hidden_size, num_classes)
        self.fc_action_mars2 = nn.Linear(self.hidden_size, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action_mars1.weight)
        self.fc_action_mars1.bias.data.zero_()
        
        torch.nn.init.xavier_uniform_(self.fc_action_mars2.weight)
        self.fc_action_mars2.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.mapper(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        input_vectors=x
        norm = input_vectors.norm(p=2, dim = -1, keepdim=True)
        input_vectors = input_vectors.div(norm)
        
        output_mars1 , maskSample = self.bert_mars1(x)
        classificationOut_mars1 = output_mars1[:,0,:]
        sequenceOut_mars1 = output_mars1[:,1:,:]
        norm = sequenceOut_mars1.norm(p=2, dim = -1, keepdim=True)
        sequenceOut_mars1 = sequenceOut_mars1.div(norm)
        output_mars1 = self.dp(classificationOut_mars1)
        x_mars1 = self.fc_action_mars1(output_mars1)
        
        output_mars2 , maskSample = self.bert_mars2(x)
        classificationOut_mars2 = output_mars2[:,0,:]
        sequenceOut_mars2 = output_mars2[:,1:,:]
        norm = sequenceOut_mars2.norm(p=2, dim = -1, keepdim=True)
        sequenceOut_mars2 = sequenceOut_mars2.div(norm)
        output_mars2 = self.dp(classificationOut_mars2)
        x_mars2 = self.fc_action_mars2(output_mars2)
        
        out = x_mars1 + x_mars2
        
        sequenceOut_mars = torch.cat((sequenceOut_mars1, sequenceOut_mars2), -1)
        return out, input_vectors, sequenceOut_mars, maskSample 
    
    
class rgb_resneXt3D64f101_bert10S_MARS6(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_bert10S_MARS6, self).__init__()
        self.hidden_size=1024
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                1024,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(1024))

        self.mapper = ResNeXtBottleneck(2048, 512, cardinality = 32, stride = 1, downsample = downsample)

        for m in self.mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()      
                
        self.bert = BERT5(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        print(sum(p.numel() for p in self.bert.parameters() if p.requires_grad))
        
        self.fc_action = nn.Linear(self.hidden_size, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.mapper(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        input_vectors=x
        norm = input_vectors.norm(p=2, dim = -1, keepdim=True)
        norm = norm / 2 ** 0.5
        input_vectors = input_vectors.div(norm)
        output , maskSample = self.bert(x)
        classificationOut = output[:,0,:]
        sequenceOut=output[:,1:,:]
        norm = sequenceOut.norm(p=2, dim = -1, keepdim=True)
        sequenceOut = sequenceOut.div(norm)
        output=self.dp(classificationOut)
        x = self.fc_action(output)
        return x, input_vectors, sequenceOut, maskSample
    
    
class rgb_resneXt3D64f101_bert10S_MARS7(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_bert10S_MARS7, self).__init__()
        self.hidden_size=512
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.2)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                512,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(512))

        self.mapper = ResNeXtBottleneck(2048, 256, cardinality = 32, stride = 1, downsample = downsample)

        for m in self.mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()      
                
        self.bert_mars1 = BERT5(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        
        self.bert_mars2 = BERT5(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        
        self.fc_action_mars1 = nn.Linear(self.hidden_size, num_classes)
        self.fc_action_mars2 = nn.Linear(self.hidden_size, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action_mars1.weight)
        self.fc_action_mars1.bias.data.zero_()
        
        torch.nn.init.xavier_uniform_(self.fc_action_mars2.weight)
        self.fc_action_mars2.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.mapper(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        input_vectors=x
        norm = input_vectors.norm(p=2, dim = -1, keepdim=True)
        input_vectors = input_vectors.div(norm)
        
        output_mars1 , maskSample = self.bert_mars1(x)
        classificationOut_mars1 = output_mars1[:,0,:]
        sequenceOut_mars1 = output_mars1[:,1:,:]
        norm = sequenceOut_mars1.norm(p=2, dim = -1, keepdim=True)
        sequenceOut_mars1 = sequenceOut_mars1.div(norm)
        output_mars1 = self.dp(classificationOut_mars1)
        x_mars1 = self.fc_action_mars1(output_mars1)
        
        output_mars2 , maskSample = self.bert_mars2(x)
        classificationOut_mars2 = output_mars2[:,0,:]
        sequenceOut_mars2 = output_mars2[:,1:,:]
        norm = sequenceOut_mars2.norm(p=2, dim = -1, keepdim=True)
        sequenceOut_mars2 = sequenceOut_mars2.div(norm)
        output_mars2 = self.dp(classificationOut_mars2)
        x_mars2 = self.fc_action_mars2(output_mars2)
        
        out = x_mars1 + x_mars2
        
        sequenceOut_mars = torch.cat((sequenceOut_mars1, sequenceOut_mars2), -1)
        return out, input_vectors, sequenceOut_mars, maskSample 
    
    
class rgb_resneXt3D64f101_bert10S_mars(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_bert10S_mars, self).__init__()
        self.hidden_size=512
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                512,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(512))

        self.mapper = ResNeXtBottleneck(2048, 256, cardinality = 32, stride = 1, downsample = downsample)

        for m in self.mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()      
                
        self.bert = BERT5(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        print(sum(p.numel() for p in self.bert.parameters() if p.requires_grad))
        
        self.fc_action = nn.Linear(self.hidden_size, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.mapper(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        input_vectors=x
        norm = input_vectors.norm(p=2, dim = -1, keepdim=True)
        input_vectors = input_vectors.div(norm)
        output , maskSample = self.bert(x)
        classificationOut = output[:,0,:]
        sequenceOut=output[:,1:,:]
        norm = sequenceOut.norm(p=2, dim = -1, keepdim=True)
        sequenceOut = sequenceOut.div(norm)
        output=self.dp(classificationOut)
        x = self.fc_action(output)
        return x, input_vectors, sequenceOut, maskSample
    
class rgb_resneXt3D64f101_bert10B_MARS(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_bert10B_MARS, self).__init__()
        self.hidden_size=512
        self.n_layers=8
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                512,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(512))

        self.mapper = ResNeXtBottleneck(2048, 256, cardinality = 32, stride = 1, downsample = downsample)

        for m in self.mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()      
                
        self.bert = BERT2(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        print(sum(p.numel() for p in self.bert.parameters() if p.requires_grad))
        
        self.fc_action = nn.Linear(self.hidden_size, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.mapper(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        input_vectors=x
        norm = input_vectors.norm(p=2, dim = -1, keepdim=True)
        input_vectors = input_vectors.div(norm)
        output , maskSample = self.bert(x)
        classificationOut = output[:,0,:]
        sequenceOut=output[:,1:,:]
        norm = sequenceOut.norm(p=2, dim = -1, keepdim=True)
        sequenceOut = sequenceOut.div(norm)
        output=self.dp(classificationOut)
        x = self.fc_action(output)
        return x, input_vectors, sequenceOut, maskSample

def conv3x3x3(in_planes, out_planes, stride=1):
    # 3x3x3 convolution with padding
    return nn.Conv3d(
        in_planes,
        out_planes,
        kernel_size=3,
        stride=stride,
        padding=1,
        bias=False)


def downsample_basic_block(x, planes, stride):
    out = F.avg_pool3d(x, kernel_size=1, stride=stride)
    zero_pads = torch.Tensor(
        out.size(0), planes - out.size(1), out.size(2), out.size(3),
        out.size(4)).zero_()
    if isinstance(out.data, torch.cuda.FloatTensor):
        zero_pads = zero_pads.cuda()

    out = Variable(torch.cat([out.data, zero_pads], dim=1))

    return out


class ResNeXtBottleneck(nn.Module):
    expansion = 2

    def __init__(self, inplanes, planes, cardinality, stride=1,
                 downsample=None):
        super(ResNeXtBottleneck, self).__init__()
        mid_planes = cardinality * int(planes / 32)
        self.conv1 = nn.Conv3d(inplanes, mid_planes, kernel_size=1, bias=False)
        self.bn1 = nn.BatchNorm3d(mid_planes)
        self.conv2 = nn.Conv3d(
            mid_planes,
            mid_planes,
            kernel_size=3,
            stride=stride,
            padding=1,
            groups=cardinality,
            bias=False)
        self.bn2 = nn.BatchNorm3d(mid_planes)
        self.conv3 = nn.Conv3d(
            mid_planes, planes * self.expansion, kernel_size=1, bias=False)
        self.bn3 = nn.BatchNorm3d(planes * self.expansion)
        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample
        self.stride = stride

    def forward(self, x):
        residual = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)

        out = self.conv3(out)
        out = self.bn3(out)

        if self.downsample is not None:
            residual = self.downsample(x)

        out += residual
        out = self.relu(out)

        return out


class ResNeXt(nn.Module):

    def __init__(self,
                 block,
                 layers,
                 sample_size,
                 sample_duration,
                 shortcut_type='B',
                 cardinality=32,
                 num_classes=400):
        self.inplanes = 64
        super(ResNeXt, self).__init__()
        self.conv1 = nn.Conv3d(
            3,
            64,
            kernel_size=7,
            stride=(1, 2, 2),
            padding=(3, 3, 3),
            bias=False)
        self.bn1 = nn.BatchNorm3d(64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool3d(kernel_size=(3, 3, 3), stride=2, padding=1)
        self.layer1 = self._make_layer(block, 128, layers[0], shortcut_type,
                                       cardinality)
        self.layer2 = self._make_layer(
            block, 256, layers[1], shortcut_type, cardinality, stride=2)
        self.layer3 = self._make_layer(
            block, 512, layers[2], shortcut_type, cardinality, stride=2)
        self.layer4 = self._make_layer(
            block, 1024, layers[3], shortcut_type, cardinality, stride=2)
        last_duration = int(math.ceil(sample_duration / 16))
        last_size = int(math.ceil(sample_size / 32))
        self.avgpool = nn.AvgPool3d(
            (last_duration, last_size, last_size), stride=1)
        self.fc = nn.Linear(cardinality * 32 * block.expansion, num_classes)

        for m in self.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()

    def _make_layer(self,
                    block,
                    planes,
                    blocks,
                    shortcut_type,
                    cardinality,
                    stride=1):
        downsample = None
        if stride != 1 or self.inplanes != planes * block.expansion:
            if shortcut_type == 'A':
                downsample = partial(
                    downsample_basic_block,
                    planes=planes * block.expansion,
                    stride=stride)
            else:
                downsample = nn.Sequential(
                    nn.Conv3d(
                        self.inplanes,
                        planes * block.expansion,
                        kernel_size=1,
                        stride=stride,
                        bias=False), nn.BatchNorm3d(planes * block.expansion))

        layers = []
        layers.append(
            block(self.inplanes, planes, cardinality, stride, downsample))
        self.inplanes = planes * block.expansion
        for i in range(1, blocks):
            layers.append(block(self.inplanes, planes, cardinality))

        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.avgpool(x)

        x = x.view(x.size(0), -1)
        x = self.fc(x)

        return x


def get_fine_tuning_parameters(model, ft_begin_index):
    if ft_begin_index == 0:
        return model.parameters()

    ft_module_names = []
    for i in range(ft_begin_index, 5):
        ft_module_names.append('layer{}'.format(i))
    ft_module_names.append('fc')

    parameters = []
    for k, v in model.named_parameters():
        for ft_module in ft_module_names:
            if ft_module in k:
                parameters.append({'params': v})
                break
        else:
            parameters.append({'params': v, 'lr': 0.0})

    return parameters


def resnext3D50(**kwargs):
    """Constructs a ResNet-50 model.
    """
    model = ResNeXt(ResNeXtBottleneck, [3, 4, 6, 3], **kwargs)
    return model


def resnext3D101(**kwargs):
    """Constructs a ResNet-101 model.
    """
    model = ResNeXt(ResNeXtBottleneck, [3, 4, 23, 3], **kwargs)
    return model

def rgb_mars_resnext3D64f101(num_classes , length, modelPath=''):
    """Constructs a ResNet-101 model.
    """
    model = ResNeXt(ResNeXtBottleneck, [3, 4, 23, 3], sample_size=112, sample_duration=64, num_classes=51)
    return model

def flow_mars_resnext3D64f101(num_classes , length, modelPath=''):
    """Constructs a ResNet-101 model.
    """
    model = ResNeXt(ResNeXtBottleneck, [3, 4, 23, 3], sample_size=112, sample_duration=64, num_classes=51)
    model.conv1 = nn.Conv3d(
        2,
        64,
        kernel_size=7,
        stride=(1, 2, 2),
        padding=(3, 3, 3),
        bias=False)
    return model


def _trained_resnext101(model_path, **kwargs):
    """Constructs a ResNet-101 model.
    """
    model = ResNeXt(ResNeXtBottleneck, [3, 4, 23, 3], **kwargs)
    if model_path=='':
        return model
    params = torch.load(model_path)
    new_dict = {k[7:]: v for k, v in params['state_dict'].items()} 
    model_dict=model.state_dict() 
    model_dict.update(new_dict)
    model.load_state_dict(new_dict)
    return model

def _trained_resnext101_flow(model_path_flow, **kwargs):
    """Constructs a ResNet-101 model.
    """
    model = ResNeXt(ResNeXtBottleneck, [3, 4, 23, 3], **kwargs)
    model.conv1 = nn.Conv3d(
        2,
        64,
        kernel_size=7,
        stride=(1, 2, 2),
        padding=(3, 3, 3),
        bias=False)
    if model_path_flow=='':
        return model
    params = torch.load(model_path_flow)
    new_dict = {k[7:]: v for k, v in params['state_dict'].items()} 
    model_dict=model.state_dict() 
    model_dict.update(new_dict)
    model.load_state_dict(new_dict)
    return model

def resnext3D152(**kwargs):
    """Constructs a ResNet-101 model.
    """
    model = ResNeXt(ResNeXtBottleneck, [3, 8, 36, 3], **kwargs)
    return model




class rgb_resneXt3D64f101_pooling(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_pooling, self).__init__()
        self.hidden_size=512
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                512,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(512))

        mapper = ResNeXtBottleneck(2048, 256, cardinality = 32, stride = 1, downsample = downsample)

        for m in mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()   
                
        self.features[7][2] = mapper
           
        self.linear = nn.Linear(2048, 1550)
        self.fc_action = nn.Linear(1550, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size * 4)
        input_vectors = x
        sequenceOut = x
        maskSample = x
        x = self.dp(x)
        output = self.linear(x)
        x = self.fc_action(output)
        return x, input_vectors, sequenceOut, maskSample
    
class rgb_resneXt3D64f101_pooling2(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_pooling2, self).__init__()
        self.hidden_size=512
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                512,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(512))

        mapper = ResNeXtBottleneck(2048, 256, cardinality = 32, stride = 1, downsample = downsample)

        for m in mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()   
                
        self.features[7][2] = mapper
        
        self.relu = nn.ReLU(inplace=True)
           
        self.linear = nn.Linear(2048, 1550)
        self.fc_action = nn.Linear(1550, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size * 4)
        input_vectors = x
        sequenceOut = x
        maskSample = x
        x = self.linear(x)
        x = self.relu(x)
        x = self.dp(x)
        x = self.fc_action(x)
        return x, input_vectors, sequenceOut, maskSample
    
    
class rgb_resneXt3D64f101_pooling3(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_pooling3, self).__init__()
        self.hidden_size=512
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                512,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(512))

        mapper = ResNeXtBottleneck(2048, 256, cardinality = 32, stride = 1, downsample = downsample)

        for m in mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()   
                
        self.features[7][2] = mapper
           
        self.fc_action = nn.Linear(2048, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size * 4)
        input_vectors = x
        sequenceOut = x
        maskSample = x
        x = self.dp(x)
        x = self.fc_action(x)
        return x, input_vectors, sequenceOut, maskSample
    
class rgb_resneXt3D64f101_NLB(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_NLB, self).__init__()
        self.hidden_size=750
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                self.hidden_size,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(self.hidden_size))

        mapper = ResNeXtBottleneck(2048, int(self.hidden_size / 2), cardinality = 32, stride = 1, downsample = downsample)

        for m in mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()   
                
        self.features[7][2] = mapper
           
        self.NLB = NLBlockND(in_channels = self.hidden_size, inter_channels = self.hidden_size)
        
        self.fc_action = nn.Linear(self.hidden_size * 4, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.NLB(x)
        x = self.avgpool(x)
        x = x.view(-1,self.hidden_size * 4)
        input_vectors = x
        sequenceOut = x
        maskSample = x
        x = self.dp(x)
        x = self.fc_action(x)
        return x, input_vectors, sequenceOut, maskSample
    
    
class rgb_resneXt3D64f101_NLB2(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_NLB2, self).__init__()
        self.hidden_size=512
        self.linear_size = 1000
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                self.hidden_size,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(self.hidden_size))

        mapper = ResNeXtBottleneck(2048, int(self.hidden_size / 2), cardinality = 32, stride = 1, downsample = downsample)

        for m in mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()   
                
        self.features[7][2] = mapper
        self.relu = nn.ReLU(inplace=True)
           
        self.NLB = NLBlockND(in_channels = self.hidden_size, inter_channels = self.hidden_size)
        
        self.linear = nn.Linear(self.hidden_size * 4, self.linear_size)
        self.fc_action = nn.Linear(self.linear_size, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.NLB(x)
        x = self.avgpool(x)
        x = x.view(-1,self.hidden_size * 4)
        input_vectors = x
        sequenceOut = x
        maskSample = x
        x = self.linear(x)
        x = self.relu(x)
        x = self.dp(x)
        x = self.fc_action(x)
        return x, input_vectors, sequenceOut, maskSample
    
    
class rgb_resneXt3D64f101_NLB3(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_NLB3, self).__init__()
        self.hidden_size=512
        self.linear_size = 1000
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                self.hidden_size,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(self.hidden_size))

        mapper = ResNeXtBottleneck(2048, int(self.hidden_size / 2), cardinality = 32, stride = 1, downsample = downsample)

        for m in mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()   
                
        self.features[7][2] = mapper
           
        self.NLB = NLBlockND(in_channels = self.hidden_size, inter_channels = self.hidden_size)
        
        self.linear = nn.Linear(self.hidden_size * 4, self.linear_size)
        self.fc_action = nn.Linear(self.linear_size, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.NLB(x)
        x = self.avgpool(x)
        x = x.view(-1,self.hidden_size * 4)
        input_vectors = x
        sequenceOut = x
        maskSample = x
        x = self.dp(x)
        x = self.linear(x)
        x = self.fc_action(x)
        return x, input_vectors, sequenceOut, maskSample
    
    
class rgb_resneXt3D64f101_NLB4(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_NLB4, self).__init__()
        self.hidden_size=512
        self.linear_size = 1000
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                self.hidden_size,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(self.hidden_size))

        mapper = ResNeXtBottleneck(2048, int(self.hidden_size / 2), cardinality = 32, stride = 1, downsample = downsample)

        for m in mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()   
                
        self.features[7][2] = mapper
        self.relu = nn.ReLU(inplace=True)
           
        self.NLB = NLBlockND(in_channels = self.hidden_size, inter_channels = self.hidden_size)
        
        self.linear = nn.Linear(self.hidden_size * 4, self.linear_size)
        self.fc_action = nn.Linear(self.linear_size, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.NLB(x)
        x = self.avgpool(x)
        x = x.view(-1,self.hidden_size * 4)
        input_vectors = x
        sequenceOut = x
        maskSample = x
        x = self.dp(x)
        x = self.linear(x)
        x = self.relu(x)
        x = self.fc_action(x)
        return x, input_vectors, sequenceOut, maskSample
    
    
class rgb_resneXt3D64f101_lstm(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_lstm, self).__init__()
        self.hidden_size=460
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                self.hidden_size,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(self.hidden_size))

        mapper = ResNeXtBottleneck(2048, int(self.hidden_size / 2), cardinality = 32, stride = 1, downsample = downsample)

        for m in mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()   
                
        self.features[7][2] = mapper
           
        self.lstm=nn.LSTM(input_size=self.hidden_size, hidden_size=self.hidden_size, num_layers=1, batch_first=True,bidirectional=True)
        self.fc_action = nn.Linear(self.hidden_size * 2, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        output,_=self.lstm(x)
        x= output[:,-1,:]
        input_vectors = x
        sequenceOut = x
        maskSample = x
        x = self.dp(x)
        x = self.fc_action(x)
        return x, input_vectors, sequenceOut, maskSample
    
class rgb_resneXt3D64f101_lstm2(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_lstm2, self).__init__()
        self.hidden_size = 450
        self.input_size = 512
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                self.input_size,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(self.input_size))

        mapper = ResNeXtBottleneck(2048, int(self.input_size / 2), cardinality = 32, stride = 1, downsample = downsample)

        for m in mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()   
                
        self.features[7][2] = mapper
           
        self.lstm=nn.LSTM(input_size=self.input_size, hidden_size=self.hidden_size, num_layers=2, batch_first=True,bidirectional=False)
        self.fc_action = nn.Linear(self.hidden_size, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.input_size, 4)
        x = x.transpose(1,2)
        output,_=self.lstm(x)
        x= output[:,-1,:]
        input_vectors = x
        sequenceOut = x
        maskSample = x
        x = self.dp(x)
        x = self.fc_action(x)
        return x, input_vectors, sequenceOut, maskSample
    
class rgb_resneXt3D64f101_adamw(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_adamw, self).__init__()
        self.num_classes=num_classes
        self.dp = nn.Dropout(p=0.8)
        

        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-1])
        
        self.fc_action = nn.Linear(2048, num_classes)
        for param in self.features.parameters():
            param.requires_grad = True
                
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.dp(x)
        x = self.fc_action(x)
        return x, x, x, x
    
class rgb_resneXt3D64f101_adamw_modified(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_adamw_modified, self).__init__()
        self.num_classes=num_classes
        self.dp = nn.Dropout(p=0.8)
        self.hidden_size = 512
        

        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-1])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                self.hidden_size,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(self.hidden_size))

        mapper = ResNeXtBottleneck(2048, int(self.hidden_size / 2), cardinality = 32, stride = 1, downsample = downsample)

        for m in mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()   
                
        self.features[7][2] = mapper
        
        self.fc_action = nn.Linear(self.hidden_size, num_classes)
        for param in self.features.parameters():
            param.requires_grad = True
                
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.dp(x)
        x = self.fc_action(x)
        return x, x, x, x
    
class rgb_resneXt3D64f101_bert10SS_MARS(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_bert10SS_MARS, self).__init__()
        self.hidden_size=512
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                512,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(512))

        mapper = ResNeXtBottleneck(2048, 256, cardinality = 32, stride = 1, downsample = downsample)

        for m in mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()   
                
        self.features[7][2] = mapper
                
        self.bert = BERT5(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        print(sum(p.numel() for p in self.bert.parameters() if p.requires_grad))
        
        self.fc_action = nn.Linear(self.hidden_size, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        input_vectors=x
        norm = input_vectors.norm(p=2, dim = -1, keepdim=True)
        input_vectors = input_vectors.div(norm)
        output , maskSample = self.bert(x)
        classificationOut = output[:,0,:]
        sequenceOut=output[:,1:,:]
        norm = sequenceOut.norm(p=2, dim = -1, keepdim=True)
        sequenceOut = sequenceOut.div(norm)
        output=self.dp(classificationOut)
        x = self.fc_action(output)
        return x, input_vectors, sequenceOut, maskSample
    
    
class rgb_resneXt3D64f101_bert10SS_MARS_copy(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_bert10SS_MARS_copy, self).__init__()
        self.hidden_size=512
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                512,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(512))

        mapper = ResNeXtBottleneck(2048, 256, cardinality = 32, stride = 1, downsample = downsample)

        for m in mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()   
                
        self.features[7][2] = mapper
                
        self.bert = BERT5(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        print(sum(p.numel() for p in self.bert.parameters() if p.requires_grad))
        
        self.fc_action = nn.Linear(self.hidden_size, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        input_vectors=x
        norm = input_vectors.norm(p=2, dim = -1, keepdim=True)
        input_vectors = input_vectors.div(norm)
        output , maskSample = self.bert(x)
        classificationOut = output[:,0,:]
        sequenceOut=output[:,1:,:]
        norm = sequenceOut.norm(p=2, dim = -1, keepdim=True)
        sequenceOut = sequenceOut.div(norm)
        output=self.dp(classificationOut)
        x = self.fc_action(output)
        return x, input_vectors, sequenceOut, maskSample
    
class rgb_resneXt3D64f101_bert10SS_MARS_copy2(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_bert10SS_MARS_copy2, self).__init__()
        self.hidden_size=512
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                512,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(512))

        mapper = ResNeXtBottleneck(2048, 256, cardinality = 32, stride = 1, downsample = downsample)

        for m in mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()   
                
        self.features[7][2] = mapper
                
        self.bert = BERT5(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        print(sum(p.numel() for p in self.bert.parameters() if p.requires_grad))
        
        self.fc_action = nn.Linear(self.hidden_size, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        input_vectors=x
        norm = input_vectors.norm(p=2, dim = -1, keepdim=True)
        input_vectors = input_vectors.div(norm)
        output , maskSample = self.bert(x)
        classificationOut = output[:,0,:]
        sequenceOut=output[:,1:,:]
        norm = sequenceOut.norm(p=2, dim = -1, keepdim=True)
        sequenceOut = sequenceOut.div(norm)
        output=self.dp(classificationOut)
        x = self.fc_action(output)
        return x, input_vectors, sequenceOut, maskSample
    
class rgb_resneXt3D64f101_bert10SS_MARS_copy3(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_bert10SS_MARS_copy3, self).__init__()
        self.hidden_size=512
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                512,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(512))

        mapper = ResNeXtBottleneck(2048, 256, cardinality = 32, stride = 1, downsample = downsample)

        for m in mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()   
                
        self.features[7][2] = mapper
                
        self.bert = BERT5(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        print(sum(p.numel() for p in self.bert.parameters() if p.requires_grad))
        
        self.fc_action = nn.Linear(self.hidden_size, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        input_vectors=x
        norm = input_vectors.norm(p=2, dim = -1, keepdim=True)
        input_vectors = input_vectors.div(norm)
        output , maskSample = self.bert(x)
        classificationOut = output[:,0,:]
        sequenceOut=output[:,1:,:]
        norm = sequenceOut.norm(p=2, dim = -1, keepdim=True)
        sequenceOut = sequenceOut.div(norm)
        output=self.dp(classificationOut)
        x = self.fc_action(output)
        return x, input_vectors, sequenceOut, maskSample
    
class rgb_resneXt3D64f101_bert10SS_MARS5(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_bert10SS_MARS5, self).__init__()
        self.hidden_size=512
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                512,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(512))

        self.mapper = ResNeXtBottleneck(2048, 256, cardinality = 32, stride = 1, downsample = downsample)

        for m in self.mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()      
                
        self.features[7][2] = self.mapper
        self.bert_mars1 = BERT5(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        
        self.bert_mars2 = BERT5(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        
        self.fc_action_mars1 = nn.Linear(self.hidden_size, num_classes)
        self.fc_action_mars2 = nn.Linear(self.hidden_size, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action_mars1.weight)
        self.fc_action_mars1.bias.data.zero_()
        
        torch.nn.init.xavier_uniform_(self.fc_action_mars2.weight)
        self.fc_action_mars2.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        input_vectors=x
        norm = input_vectors.norm(p=2, dim = -1, keepdim=True)
        input_vectors = input_vectors.div(norm)
        
        output_mars1 , maskSample = self.bert_mars1(x)
        classificationOut_mars1 = output_mars1[:,0,:]
        sequenceOut_mars1 = output_mars1[:,1:,:]
        norm = sequenceOut_mars1.norm(p=2, dim = -1, keepdim=True)
        sequenceOut_mars1 = sequenceOut_mars1.div(norm)
        output_mars1 = self.dp(classificationOut_mars1)
        x_mars1 = self.fc_action_mars1(output_mars1)
        
        output_mars2 , maskSample = self.bert_mars2(x)
        classificationOut_mars2 = output_mars2[:,0,:]
        sequenceOut_mars2 = output_mars2[:,1:,:]
        norm = sequenceOut_mars2.norm(p=2, dim = -1, keepdim=True)
        sequenceOut_mars2 = sequenceOut_mars2.div(norm)
        output_mars2 = self.dp(classificationOut_mars2)
        x_mars2 = self.fc_action_mars2(output_mars2)
        
        out = x_mars1 + x_mars2
        
        sequenceOut_mars = torch.cat((sequenceOut_mars1, sequenceOut_mars2), -1)
        return out, input_vectors, sequenceOut_mars, maskSample 
    
    
class rgb_resneXt3D64f101_bert10SS_MARS6(nn.Module):
    def __init__(self, num_classes , length, modelPath=''):
        super(rgb_resneXt3D64f101_bert10SS_MARS6, self).__init__()
        self.hidden_size=1024
        self.n_layers=1
        self.attn_heads=8
        self.num_classes=num_classes
        self.length=length
        self.dp = nn.Dropout(p=0.8)
        
        self.avgpool = nn.AvgPool3d((1, 4, 4), stride=1)
        self.features=nn.Sequential(*list(_trained_resnext101(model_path=modelPath, sample_size=112, sample_duration=64).children())[:-2])
        
        downsample = nn.Sequential(
            nn.Conv3d(
                2048,
                1024,
                kernel_size=1,
                stride=1,
                bias=False), nn.BatchNorm3d(1024))

        self.mapper = ResNeXtBottleneck(2048, 512, cardinality = 32, stride = 1, downsample = downsample)

        for m in self.mapper.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight)
                #m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
            elif isinstance(m, nn.BatchNorm3d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()      
                
        self.features[7][2] = self.mapper
        self.bert = BERT5(self.hidden_size, 4 , hidden=self.hidden_size, n_layers=self.n_layers, attn_heads=self.attn_heads)
        print(sum(p.numel() for p in self.bert.parameters() if p.requires_grad))
        
        self.fc_action = nn.Linear(self.hidden_size, num_classes)
      
        for param in self.features.parameters():
            param.requires_grad = True
  
        torch.nn.init.xavier_uniform_(self.fc_action.weight)
        self.fc_action.bias.data.zero_()
        
    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), self.hidden_size, 4)
        x = x.transpose(1,2)
        input_vectors=x
        norm = input_vectors.norm(p=2, dim = -1, keepdim=True)
        norm = norm / 2 ** 0.5
        input_vectors = input_vectors.div(norm)
        output , maskSample = self.bert(x)
        classificationOut = output[:,0,:]
        sequenceOut=output[:,1:,:]
        norm = sequenceOut.norm(p=2, dim = -1, keepdim=True)
        sequenceOut = sequenceOut.div(norm)
        output=self.dp(classificationOut)
        x = self.fc_action(output)
        return x, input_vectors, sequenceOut, maskSample