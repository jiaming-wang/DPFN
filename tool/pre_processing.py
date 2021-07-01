#!/usr/bin/env python
# coding=utf-8
'''
@Author: wjm
@Date: 2020-06-13 20:12:23
LastEditTime: 2020-12-07 10:35:46
@Description: PAN下采样以及图像分块
'''
import numpy as np 
import glob, os, h5py
import os
import cv2
from scipy import misc
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

class image_to_patch:
    
    def __init__(self, patch_size, scale, ms_path, ms_image_path, pan_path, pan_image_path):

        self.stride = patch_size
        self.scale = scale
        self.ms_path = ms_path
        self.ms_image_path = ms_image_path
        self.pan_path = pan_path
        self.pan_image_path = pan_image_path
        
        if not os.path.exists(ms_image_path):
            os.mkdir(ms_image_path)
        if not os.path.exists(pan_image_path):
            os.mkdir(pan_image_path)

    def to_patch(self):
        
        n_ms = 1
        n_pan = 1
        
        for i in range(1,2):
            ms_path = self.ms_path + str(i) + '.tif'
            pan_path = self.pan_path + str(i) + '.tif'
            
            #read MS image, CMYK space
            img_ms = self.imread(ms_path)
            img_ms = self.modcrop(img_ms, self.scale)
            
            #read PAN image, Gray space
            img_pan = self.imread(pan_path)
            img_pan = self.modcrop(img_pan, self.scale)
            
            # high, width
            h, w  = img_ms.size

            # MS image
            for x in range(0, h - self.stride, self.stride):
                for y in range(0, w - self.stride, self.stride):
                    box = [x, y, x + self.stride, y + self.stride]
                    sub_img_label = img_ms.crop(box)
                    sub_img_label.save(os.path.join(self.ms_image_path, str(n_ms)+'.tif'))
                    n_ms = n_ms + 1
            
            # PAN image
            for x in range(0, h - self.stride, self.stride):
                for y in range(0, w - self.stride, self.stride):
                    box = [x, y, x + self.stride, y + self.stride]
                    sub_img_label = img_pan.crop(box)
                    sub_img_label.save(os.path.join(self.pan_image_path, str(n_pan)+'.tif'))
                    n_pan = n_pan + 1

    def imread(self, path):
        img = Image.open(path)
        return img

    def modcrop(self, img, scale =3):
        h, w = img.size
        h = (h // scale) * scale
        w = (w // scale) * scale
        box=(0,0,h,w)
        img = img.crop(box)
        return img  

class downsample:
    
    def __init__(self, pan_pach, scale, d_pan_path):
        image = Image.open(pan_pach).convert('L')
        d_image = image.resize((int(image.size[0]/scale),int(image.size[1]/scale)), Image.BICUBIC) 
        d_image.save(d_pan_path)
         
    
if __name__ == '__main__':
    image_size = 256
    scale = 4
    ms_pach = r'/Users/wjmecho/Desktop/Non-pan/数据/gf2/dataset/modcrop/ms/'
    ms_image_path = r'./ms'
    pan_pach = r'/Users/wjmecho/Desktop/Non-pan/数据/gf2/dataset/modcrop/pan/'
    pan_image_path = r'./pan'
    
    # downsample pan image
    # pan_path = '/Users/wjmecho/Desktop/Non-pan/数据/gf2/dataset/pan/'
    # pans_path = '/Users/wjmecho/Desktop/Non-pan/数据/gf2/dataset/pan1/'
    # for i in range(1,2):
    #     img_pan = os.path.join(pan_path, str(i)+'.tif')
    #     img_pans = os.path.join(pans_path, str(i)+'.tif')
    #     downsample(img_pan, scale, img_pans)

    # image to patch
    task = image_to_patch(image_size, scale, ms_pach, ms_image_path, pan_pach, pan_image_path)
    task.to_patch()
