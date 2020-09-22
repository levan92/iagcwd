import cv2
import glob
import argparse
import numpy as np
from matplotlib import pyplot as plt
from scipy.linalg import fractional_matrix_power

def image_agcwd(img, a=0.25, truncated_cdf=False):
    # h,w = img.shape[:2]
    hist,_ = np.histogram(img.flatten(),256,[0,256])
    # hist,bins = np.histogram(img.flatten(),256,[0,256])
    # cdf = hist.cumsum()
    # cdf_normalized = cdf / cdf.max()
    prob_normalized = hist / hist.sum()

    unique_intensity = np.unique(img)
    # intensity_max = unique_intensity.max()
    # intensity_min = unique_intensity.min()
    prob_min = prob_normalized.min()
    prob_max = prob_normalized.max()
    
    pn_temp = (prob_normalized - prob_min) / (prob_max - prob_min)
    pn_temp[pn_temp>0] = prob_max * (pn_temp[pn_temp>0]**a)
    pn_temp[pn_temp<0] = prob_max * (-((-pn_temp[pn_temp<0])**a))
    prob_normalized_wd = pn_temp / pn_temp.sum() # normalize to [0,1]
    cdf_prob_normalized_wd = prob_normalized_wd.cumsum()
    
    if truncated_cdf: 
        inverse_cdf = np.maximum(0.5,1 - cdf_prob_normalized_wd)
    else:
        inverse_cdf = 1 - cdf_prob_normalized_wd
    
    img_new = img.copy()
    for i in unique_intensity:
        img_new[img==i] = np.round(255 * (i / 255)**inverse_cdf[i])
   
    return img_new

class AdaptiveGamma(object):
    def __init__(self, thresh=0.3, exp_in = 112, agcwd_alpha_bright=0.25, agcwd_alpha_dimmed=0.75):
        # Determine whether image is bright or dimmed
        self.threshold = thresh
        # Expected global average intensity
        self.exp_in = exp_in
        self.agcwd_alpha_bright = agcwd_alpha_bright
        self.agcwd_alpha_dimmed = agcwd_alpha_dimmed

    def update(self, thresh=None, exp_in = None, agcwd_alpha_bright=None, agcwd_alpha_dimmed=None):
        if thresh:
            # Determine whether image is bright or dimmed
            self.threshold = thresh
            print(f'[AdaptiveGamma] Threshold updated to {self.threshold}.')
        if exp_in:
            # Expected global average intensity
            self.exp_in = exp_in
            print(f'[AdaptiveGamma] Expected Avrg Intensity updated to {self.exp_in}.')
        if agcwd_alpha_bright:
            self.agcwd_alpha_bright = agcwd_alpha_bright
            print(f'[AdaptiveGamma] Alpha (bright) updated to {self.agcwd_alpha_bright}.')
        if agcwd_alpha_dimmed:
            self.agcwd_alpha_dimmed = agcwd_alpha_dimmed
            print(f'[AdaptiveGamma] Alpha (dimmed) updated to {self.agcwd_alpha_dimmed}.')

    def _process_bright(self, img):
        img_negative = 255 - img
        agcwd = image_agcwd(img_negative, a=self.agcwd_alpha_bright, truncated_cdf=False)
        reversed = 255 - agcwd
        return reversed

    def _process_dimmed(self, img):
        agcwd = image_agcwd(img, a=self.agcwd_alpha_dimmed, truncated_cdf=True)
        return agcwd

    def adjust(self, img):
        # Extract intensity component of the image
        YCrCb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
        Y = YCrCb[:,:,0]
        M,N = img.shape[:2]
        mean_in = np.sum(Y/(M*N)) 
        t = (mean_in - self.exp_in)/ self.exp_in
        
        # Process image for gamma correction
        if t < -self.threshold: # Dimmed Image
            print ("Dim Image")
            result = self._process_dimmed(Y)
            YCrCb[:,:,0] = result
            img_output = cv2.cvtColor(YCrCb,cv2.COLOR_YCrCb2BGR)
        elif t > self.threshold:
            print ("Bright Image") # Bright Image
            result = self._process_bright(Y)
            YCrCb[:,:,0] = result
            img_output = cv2.cvtColor(YCrCb,cv2.COLOR_YCrCb2BGR)
        else:
            print("Not adjusted")
            img_output = img

        return img_output