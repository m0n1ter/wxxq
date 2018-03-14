# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 16:04:29 2017

@author: jjxyyjs
"""

import tensorflow as tf 
import numpy as np 
import random
import math
from collections import deque
import matplotlib.pyplot as plt 
import pandas as pd

data=pd.read_csv('index_feature.csv')
class BrainDQN(object):
    
    def candlestickChart(data, visiableSzie=140, height=200, compact=False):
        """
        根据K线数据生成K线图并返回，每幅图140根可见K线
        参数：
        data, DataFrame的交易品种报价数据（open, high, low, close）
        compact, K线图是否为紧凑图（即K线实体只显示一半）
        返回值：
        chart, K线图的图像
        """
        if data.index.size>visiableSzie: print('警告：data中K线根数超出140根可见K线，多出K线将不可见')
        #BarWidth = 2 if compact else 3                                          # Bar的宽度
        BarWidth = 4 if compact else 5                                          # Bar的宽度
        datapace = 1                                                            # Bar之间间隔
        
        ChartHeight = height                                                       # K线图高度
        ChartWidth = visiableSzie * (BarWidth + datapace)                                # K线图宽度，每幅图140根可见K线
        chart = np.zeros([ChartHeight, ChartWidth,3], np.uint8) + 255          # K线图
    
        dmax,dmin=data['MACD'].max(),data['MACD'].min()                # 计算最大值、最小值
        k=list(data.index)
        for i in k:
            x = (BarWidth + datapace) * i + 1                                # x为K线影线的X轴坐标值(1为Bar之间间隔)
            #color = (0,0,255) if data.ix[i,'close']>=data.ix[i,'open'] else (0,0,0)
            M=data.MACD                   
            M=round(100 * (dmax-M) / (dmax - dmin)).astype(int)
            K=round(100 * (dmax) / (dmax - dmin)).astype(int)
            if i==k[0]:
                if M[i]>K:
                    cv2.line(chart, (x,M[i]),(x,M[i]), (0,0,255))
                else:
                    cv2.line(chart, (x,M[i]),(x,M[i]), (0,0,0))
            else:
                y=  (BarWidth + datapace)*(i-1)+1  
                if M[i]>K:                
                    cv2.line(chart, (y,M[i-1]),(x,M[i]), (0,0,255))  #红色表示MACD原数据为负
                else:
                    cv2.line(chart, (y,M[i-1]),(x,M[i]), (0,0,0))      #灰色表示MACD原数据为正
        return chart

    
    
    def createQNetwork(self):
        # network weights
        W_conv1 = self.weight_variable([8,8,3,32])
        b_conv1 = self.bias_variable([32])

        W_conv2 = self.weight_variable([4,4,32,64])
        b_conv2 = self.bias_variable([64])

        W_conv3 = self.weight_variable([3,3,64,64])
        b_conv3 = self.bias_variable([64])

        W_fc1 = self.weight_variable([1600,512])
        b_fc1 = self.bias_variable([512])

        W_fc2 = self.weight_variable([512,self.actions])
        b_fc2 = self.bias_variable([self.actions])

        # input layer

        stateInput = tf.placeholder("float",[None,Chart_Size,Chart_Size,3])

        # hidden layers
        h_conv1 = tf.nn.relu(self.conv2d(stateInput,W_conv1,3) + b_conv1)
        h_pool1 = self.max_pool_2x2(h_conv1)

        h_conv2 = tf.nn.relu(self.conv2d(h_pool1,W_conv2,2) + b_conv2)
        h_pool2 = self.max_pool_2x2(h_conv2)
        
        h_conv3 = tf.nn.relu(self.conv2d(h_pool2,W_conv3,1) + b_conv3)

        h_conv3_flat = tf.reshape(h_conv3,[-1,1600])
        h_fc1 = tf.nn.relu(tf.matmul(h_conv3_flat,W_fc1) + b_fc1)

        # Q Value layer
        QValue = tf.matmul(h_fc1,W_fc2) + b_fc2

        return stateInput,QValue,W_conv1,b_conv1,W_conv2,b_conv2,W_conv3,b_conv3,W_fc1,b_fc1,W_fc2,b_fc2
    


    def weight_variable(self,shape):
        initial = tf.truncated_normal(shape, stddev = 0.01)
        return tf.Variable(initial)

    def bias_variable(self,shape):
        initial = tf.constant(0.01, shape = shape)
        return tf.Variable(initial)

    def conv2d(self,x, W, stride):
        return tf.nn.conv2d(x, W, strides = [1, stride, stride, 1], padding = "SAME")

    def max_pool_2x2(self,x):
        return tf.nn.max_pool(x, ksize = [1, 2, 2, 1], strides = [1, 2, 2, 1], padding = "SAME")


action=BrainDQN()
action.candlestickChart()
        
