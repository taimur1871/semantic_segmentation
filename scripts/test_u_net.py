# -*- coding: utf-8 -*-
"""test U-net.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Vnf8u7UvioJ7DrJFZ5Jrc_wlqC9I5lCq
"""

# import modules
import numpy as np 
import os
import skimage.io as io
import skimage.transform as trans
import scipy.misc as sc

import numpy as np
from tensorflow.keras.models import *
from tensorflow.keras.layers import *
from tensorflow.keras.optimizers import *
from tensorflow.keras.callbacks import ModelCheckpoint, LearningRateScheduler
from tensorflow.keras import backend as keras

import tensorflow as tf

import matplotlib.pyplot as plt
from PIL import Image, ImageEnhance

# save results as image
def saveResult(img_path,save_path,npyfile,flag_multi_class = False,num_class = 2):
    files=os.listdir(img_path)
    #print(len(img_path))
    #print(len(npyfile))
    
    for i,item in enumerate(npyfile):
        img = labelVisualize(num_class,COLOR_DICT,item) if flag_multi_class else item[:,:,0]
        #img1=np.array(((img - np.min(img))/np.ptp(img))>0.6).astype(float)
        img[img>0.1]=1
        img[img<=0.1]=0
        io.imsave(os.path.join(save_path, files[i]+'_predict.png'),img)

# get model path
model_path = '/content/drive/MyDrive/4BAI/Week 7/unet_2.h5'

# get image folder path
pic_folder = '/content/drive/MyDrive/Edge Detection Examples/Pictures'

# save folder
save_folder = '/content/drive/MyDrive/bit_semantic_segmentation'

#Define Additional loss functions for Task 2
def dice_coef(y_true, y_pred, smooth=1):
    intersection = keras.sum(y_true * y_pred, axis=[1,2,3])
    union = keras.sum(y_true, axis=[1,2,3]) + keras.sum(y_pred, axis=[1,2,3])
    return keras.mean( (2. * intersection + smooth) / (union + smooth), axis=0)

def dice_coef_loss(y_true, y_pred):
    return -dice_coef(y_true, y_pred)

model = tf.keras.models.load_model(model_path, custom_objects={'dice_coef_loss':dice_coef_loss, 'dice_coef':dice_coef})

# preprocess images
img = Image.open(os.path.join(pic_folder, '16.jpg'))
img = img.resize((256,256))
img = np.array(img)
img.shape

img_test = np.expand_dims(img, axis=0)

temp = model.predict(img_test[:,:,:,1])

saveResult(pic_folder, save_folder, temp)

