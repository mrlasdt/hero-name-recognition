from typing import Callable
import wget
import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm
import cv2
from pathlib import Path
from typing import Callable
from functools import partial
import shutil
from config import global_var as cfg
from utils import readlines, crop_img_to_center, flip_image
def download_template(hero_names:list[str], template_dir=cfg.TEMPLATE_DIR, img_ext=".png", template_size=cfg.IMG_SIZE, url = "https://leagueoflegends.fandom.com/wiki") -> None:
    '''
    @param hero_names: list of hero names to download template
    '''
    if not os.path.exists(template_dir):
        os.makedirs(template_dir)
    rp = requests.get(url)
    srp = BeautifulSoup(rp.content, "lxml")
    for img_tag in tqdm(srp.find("ol", {"class":"champion_roster"}).find_all("img")):
        img_url = img_tag.get('data-src')
        img_name = img_tag.get("alt") + img_ext
        img_path = os.path.join(template_dir, img_name)
        if os.path.exists(img_path) or img_tag.get("alt") not in hero_names:
            continue
        scale = template_size/16
        while True:
            try:
                wget.download(img_url.replace("/46?", f"/{int(16*scale)}?"), out=img_path)
            except:
                scale+=1
            break
        if scale!=template_size/16:
            img = cv2.imread(img_path)
            img = cv2.resize(img, (template_size, template_size))
            cv2.imwrite(img, img_path)

def correct_template_single(template_path:str, template_size:tuple[int,int], correct_dir:str, correct_func:Callable) -> None:
    img_template = cv2.imread(template_path)
    img_template = correct_func(img_template)
    img_template = cv2.resize(img_template, template_size)
    file_name = os.path.basename(template_path).split("_")[0]
    if not file_name.endswith(".png"):
        file_name = file_name  + ".png" 
    if file_name =="Jarvan.png":
        file_name = "Jarvan_IV.png"
    elif file_name == "Dr.png":
        file_name = "Dr._Mundo.png"
    elif file_name == "Miss.png":
        file_name = "Miss_Fortune.png"
    elif file_name == "Master.png":
        file_name = "Master_Yi.png"
    elif file_name == "Lee.png":
        file_name = "Lee_Sin.png"
    save_path = os.path.join(correct_dir,file_name)
    print(save_path)
    cv2.imwrite(save_path, img_template)
    pass
def correct_template(template_correct_dir)->None:
    default_template_size = (cfg.IMG_SIZE, cfg.IMG_SIZE)
    ptemplate_correct_dir = Path(template_correct_dir)
    ptemplate_correct_dir.mkdir(exist_ok=True)
    correct_template_single("data/template/Jhin.png", default_template_size, template_correct_dir, flip_image)
    correct_template_single(f"{cfg.TEST_IMAGE_DIR}/Ezreal_-c47DWO9iuQ_round1_Ezreal_05-27-2021.mp4_10_2.jpg", default_template_size, template_correct_dir, partial(crop_img_to_center, center_offset=(0.18,0.16,0.21,0.09)))
    correct_template_single(f"{cfg.TEST_IMAGE_DIR}/Jarvan_920174251860258_round6_Jhin_05-22-2021.mp4_36_1.jpg", default_template_size, template_correct_dir, partial(crop_img_to_center, center_offset=(0.2,0.19,0.23,0.11)))
    correct_template_single(f"{cfg.TEST_IMAGE_DIR}/Evelynn_9Aa4KRvaLFA_round1_Tryndamere_05-19-2021.mp4_37_0.jpg", default_template_size, template_correct_dir, partial(crop_img_to_center, center_offset=(0.22,0.17,0.2,0.11)))
    correct_template_single(f"{cfg.TEST_IMAGE_DIR}/Katarina_167856652018987_round3_Annie_06-10-2021.mp4_18_7.jpg", default_template_size, template_correct_dir, partial(crop_img_to_center, center_offset=(0.23,0.17,0.18,0.11)))
    correct_template_single(f"{cfg.TEST_IMAGE_DIR}/Jinx_3165192393581135_round2_Orianna_04-20-2021.mp4_25_2.jpg", default_template_size, template_correct_dir, partial(crop_img_to_center, center_offset=(0.23,0.17,0.18,0.11)))
    correct_template_single(f"{cfg.TEST_IMAGE_DIR}/Camille_9Aa4KRvaLFA_round5_Ziggs_05-19-2021.mp4_74_1.jpg", default_template_size, template_correct_dir, partial(crop_img_to_center, center_offset=(0.23,0.17,0.18,0.11)))
    correct_template_single(f"{cfg.TEST_IMAGE_DIR}/KaiSa_9Aa4KRvaLFA_round1_Tryndamere_05-19-2021.mp4_91_1.jpg", default_template_size, template_correct_dir, partial(crop_img_to_center, center_offset=(0.28,0.17,0.12,0.11)))
    correct_template_single(f"{cfg.TEST_IMAGE_DIR}/Dr_630613568339321_round1_Dr.-Mundo_06-04-2021.mp4_32_3.jpg", default_template_size, template_correct_dir, partial(crop_img_to_center, center_offset=(0.18,0.13,0.22,0.09)))
    correct_template_single(f"{cfg.TEST_IMAGE_DIR}/Kennen_142330807963265_round5_Vayne_06-14-2021.mp4_25_0.jpg", default_template_size, template_correct_dir, partial(crop_img_to_center, center_offset=(0.16,0.16,0.28,0.1)))
    correct_template_single(f"{cfg.TEST_IMAGE_DIR}/Annie_2996176217280056_round1_Akali_06-11-2021.mp4_110_3.jpg", default_template_size, template_correct_dir, partial(crop_img_to_center, center_offset=(0.25,0.21,0.2,0.1)))
    correct_template_single(f"{cfg.TEST_IMAGE_DIR}/Miss_232154245077306_round1_Lee-Sin_06-14-2021.mp4_23_6.jpg", default_template_size, template_correct_dir, partial(crop_img_to_center, center_offset=(0.23,0.01,0.01,0.0)))
    correct_template_single(f"{cfg.TEST_IMAGE_DIR}/Leona_278220660753197_round2_Olaf_06-02-2021.mp4_10_2.jpg", default_template_size, template_correct_dir, partial(crop_img_to_center, center_offset=(0.18,0.18,0.24,0.13)))
    correct_template_single(f"{cfg.TEST_IMAGE_DIR}/Jax_3894451770602604_round2_Janna_04-27-2021.mp4_62_2.jpg", default_template_size, template_correct_dir, partial(crop_img_to_center, center_offset=(0.24,0.17,0.18,0.11)))
    correct_template_single(f"{cfg.TEST_IMAGE_DIR}/Master_142330807963265_round2_Amumu_06-14-2021.mp4_12_3.jpg", default_template_size, template_correct_dir, partial(crop_img_to_center, center_offset=(0.18,0.17,0.28,0.11)))
    correct_template_single(f"{cfg.TEST_IMAGE_DIR}/Akali_496418424743603_round3_Vayne_06-02-2021.mp4_81_2.jpg", default_template_size, template_correct_dir, partial(crop_img_to_center, center_offset=(0.24,0.17,0.23,0.11)))
    correct_template_single(f"{cfg.TEST_IMAGE_DIR}/Lulu_188828656421928_round1_Kai'Sa_05-19-2021.mp4_10_1.jpg", default_template_size, template_correct_dir, partial(crop_img_to_center, center_offset=(0.18,0.17,0.23,0.11)))
    correct_template_single(f"{cfg.TEST_IMAGE_DIR}/Lee_7KOuGlmIhbk_round22_Fiora_06-07-2021.mp4_29_0.jpg", default_template_size, template_correct_dir, partial(crop_img_to_center, center_offset=(0.14,0.17,0.28,0.11)))
    correct_template_single(f"{cfg.TEST_IMAGE_DIR}/Lee_7KOuGlmIhbk_round22_Fiora_06-07-2021.mp4_29_0.jpg", default_template_size, template_correct_dir, partial(crop_img_to_center, center_offset=(0.14,0.17,0.28,0.11)))
    correct_template_single(f"{cfg.TEST_IMAGE_DIR}/Alistar_123853103101643_round4_Alistar_06-05-2021.mp4_11_1.jpg", default_template_size, template_correct_dir, partial(crop_img_to_center, center_offset=(0.14,0.17,0.28,0.11)))
    correct_template_single(f"{cfg.TEST_IMAGE_DIR}/Diana_-c47DWO9iuQ_round1_Ezreal_05-27-2021.mp4_112_2.jpg", default_template_size, template_correct_dir, partial(crop_img_to_center, center_offset=(0.14,0.17,0.28,0.11)))

def sync_template()->None:
    shutil.copy2(f"{cfg.TEMPLATE_CORRECT_DIR}/Jarvan_IV.png",  f"{cfg.TEMPLATE_DIR}/Jarvan_IV.png")
    shutil.copy2(f"{cfg.TEMPLATE_CORRECT_DIR}/Master_Yi.png",  f"{cfg.TEMPLATE_DIR}/Master_Yi.png")
    shutil.copy2(f"{cfg.TEMPLATE_CORRECT_DIR}/Miss_Fortune.png",  f"{cfg.TEMPLATE_DIR}/Miss_Fortune.png")
    shutil.copy2(f"{cfg.TEMPLATE_CORRECT_DIR}/Lee_Sin.png",  f"{cfg.TEMPLATE_DIR}/Lee_Sin.png")
    shutil.copy2(f"{cfg.TEMPLATE_CORRECT_DIR}/Dr._Mundo.png", f"{cfg.TEMPLATE_DIR}/Dr._Mundo.png")
    shutil.copy2(f"{cfg.TEMPLATE_CORRECT_DIR}/KaiSa.png",  f"{cfg.TEMPLATE_DIR}/KaiSa.png")



def data_preparation()-> None:
    hero_names = readlines(cfg.HERO_NAMES_PATH)
    download_template(hero_names)
    correct_template(cfg.TEMPLATE_CORRECT_DIR)
    sync_template()

if __name__ =="__main__":
    data_preparation()