import numpy as np
import cv2
from pathlib import Path
from tqdm import tqdm
import os
from sklearn.metrics import classification_report, confusion_matrix
from .utils import readlines
from .config.sift import cfg_sift
from .config import global_var as cfg_global
class Predictor:
    cfg = cfg_sift
    sift_feature_extractor = cv2.xfeatures2d.SIFT_create()

    @staticmethod
    def crop_img(img:np.ndarray, offset=0.25, center_offset=(0.2,0.15,0.15,0.1)) -> np.ndarray:
        h,w = img.shape[0], img.shape[1]
        crop_pt = int(h*(1+offset))
        img = img[:,:crop_pt] if len(img.shape)==2 else img[:,:crop_pt, :]
        h_crop,w_crop = img.shape[0], img.shape[1]
        l = int(center_offset[0]*w_crop)
        t = int(center_offset[1]*h_crop)
        r = int((1-center_offset[2])*w_crop)
        b = int((1-center_offset[3])*h_crop)
        return img[t:b,l:r] if len(img.shape)==2 else img[t:b,l:r,:]

    @staticmethod
    def preprocess_img(img:np.ndarray) -> np.ndarray:
        img_ = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # To gray image
        img_ = cv2.medianBlur(img_, Predictor.cfg["preprocess"]["blur_kernel"], 0) # lọc nhiễu bằng median blur
        return img_

    @staticmethod
    def get_matching_score(img1:np.ndarray, img2:np.ndarray) -> float:
        alg_ = Predictor.cfg["sift"]["algo"]
        trees_ = Predictor.cfg["sift"]["trees"]
        check_ = Predictor.cfg["sift"]["check"]
        k_ = Predictor.cfg["sift"]["k"]
        thres_good_ = Predictor.cfg["sift"]["thres_good"]
        img1_ = Predictor.preprocess_img(img1)
        img2_ = Predictor.preprocess_img(img2)

        # tìm điểm đặc trưng và tính sift cho từng ảnh
        kp1, des1 = Predictor.sift_feature_extractor.detectAndCompute(img1_,None)
        kp2, des2 = Predictor.sift_feature_extractor.detectAndCompute(img2_,None)  
        ## tìm các cặp đặc trưng tương đồng giữa 2 ảnh. Có thể sử dụng phương pháp vét cạn BRUTE_FORCE matching hoặc FLANN hỗ trợ so khớp nhanh hơn
        index_params = dict(algorithm = alg_, trees = trees_) #thuật toán KDTREE -> chia ảnh ra từng vùng nhỏ, match từng vùng (từng tree) với nhau
        search_params = dict(checks=check_)  
        flann = cv2.FlannBasedMatcher(index_params,search_params)  
        matches2 = flann.knnMatch(des1,des2,k=k_) # trả về k=2 features gần nhất từ tập (des1,des2)
        good = []
        for m,n in matches2:
            if m.distance < thres_good_*n.distance: # chỉ giữ lại những ghép cặp ổn định (m.distance: khoảng cách gần nhất, n.distance: khoảng cách gần thứ 2)
                good.append(m)
        return len(good)
    @staticmethod
    def get_topk_template(img_path:str) ->tuple[str,int]:
        ptemplate_dir = Path(Predictor.cfg["template"]["template_dir"])
        img = cv2.imread(img_path)
        img = Predictor.crop_img(img)
        res = []
        for template_path in ptemplate_dir.iterdir():
            template_correct_path = os.path.join(Predictor.cfg["template"]["template_correct_dir"], template_path.name)
            template_img = cv2.imread(str(template_path)) if not os.path.exists(template_correct_path) else cv2.imread(template_correct_path)
            score = Predictor.get_matching_score(img, template_img)
            res.append((score, template_path.stem))
        res = sorted(res, key=lambda x: x[0], reverse=True)
        return res[:Predictor.cfg["template"]["topk"]]

    @staticmethod
    def predict(img_path:str):
        topk = Predictor.get_topk_template(img_path)
        # print(topk)
        return topk[0][1]

    @staticmethod
    def eval(test_dir, test_file, wrong_label_paths=[]):
        test_data = [test_line.split("\t") for test_line in readlines(test_file)] #test_img, label
        preds, gts = [], []
        for test_img, label in tqdm(test_data):
            
            #   if label!="Lux":
            #     continue
            test_img_path = os.path.join(test_dir, test_img)
            if test_img_path in wrong_label_paths:
                continue
            pred = Predictor.predict(test_img_path)
            preds.append(pred)
            gts.append(label)
        return preds, gts

    @staticmethod
    def report(gts, preds, labels_=None):
        print(classification_report(gts, preds, labels=labels_))
        print(confusion_matrix(preds, gts, labels=labels_))
