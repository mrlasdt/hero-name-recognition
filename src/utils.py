
import numpy as np
import cv2

def readlines(fp:str)->list[str]:
  with open(fp, "r") as f:
    lines = f.read().splitlines()
  return lines

def flip_image(img:np.ndarray):
    flipped = cv2.flip(img, 1)  # 1 indicates horizontal flip
    return flipped

def crop_img_to_center(img:np.ndarray, offset=0.25, center_offset=(0.1,0.1,0.1,0.1)) -> np.ndarray:
    h,w = img.shape[0], img.shape[1]
    crop_pt = int(h*(1+offset))
    img = img[:,:crop_pt] if len(img.shape)==2 else img[:,:crop_pt, :]
    h_crop,w_crop = img.shape[0], img.shape[1]
    l = int(center_offset[0]*w_crop)
    t = int(center_offset[1]*h_crop)
    r = int((1-center_offset[2])*w_crop)
    b = int((1-center_offset[3])*h_crop)
    return img[t:b,l:r] if len(img.shape)==2 else img[t:b,l:r,:]
