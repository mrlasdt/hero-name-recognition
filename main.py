import argparse
from src.predictor import Predictor
from src.config.global_var import HERO_NAMES_PATH
from src.utils import readlines

WRONG_LABEL_FILES = [
    "data/test_data/test_images/Graves_1398331007194492_round4_Jarvan-IV_04-26-2021.mp4_10_0.jpg", #Jarvan
    "data/test_data/test_images/Graves_1398331007194492_round4_Jarvan-IV_04-26-2021.mp4_38_6.jpg", #Jarvan
    "data/test_data/test_images/Jinx_1398331007194492_round1_Master-Yi_04-26-2021.mp4_28_0.jpg",
    "data/test_data/test_images/Jinx_142330807963265_round5_Vayne_06-14-2021.mp4_153_6.jpg",
    "data/test_data/test_images/Jinx_1447615885600445_round7_Nami_06-04-2021.mp4_36_2.jpg",
    "data/test_data/test_images/Jinx_4161501510579966_round2_Fiora_06-10-2021.mp4_23_1.jpg",
    "data/test_data/test_images/Jinx_570649517229749_round3_Braum_04-22-2021.mp4_37_3.jpg",
]

def get_args():
    parser = argparse.ArgumentParser()
    # parser image
    parser.add_argument("--image_dir", type=str, required=True, help="path to input image/directory")
    parser.add_argument("--label_file", type=str, required=True, help="path to label file")
    parser.add_argument("--out_file", type=str, required=False, help="path to label file", default="out.txt")
    opt = parser.parse_args()
    return opt

def get_test_labels(test_label_file:str) -> list[str]:
    test_data = [test_line.split("\t") for test_line in readlines(test_label_file)] #test_img, label
    test_labels = [t[1] for t in test_data]
    return list(set(test_labels))

def write_to_file(fp:str, preds:list, gts:list) -> None:
    print("[INFO]: Saving to", fp)
    f = open(fp, "w")
    for pred, gt in zip (preds, gts):
        f.write(f"{pred}\t{gt}\n")
    f.close()

def main()->None:
    opt = get_args()
    test_labels = get_test_labels(opt.label_file)
    preds, gts = Predictor.eval(opt.image_dir, opt.label_file, wrong_label_paths=WRONG_LABEL_FILES)
    Predictor.report(gts, preds, labels_=test_labels)
    write_to_file(opt.out_file, preds, gts)

if __name__ == "__main__":
    main()