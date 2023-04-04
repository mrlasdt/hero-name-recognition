from . import global_var
cfg_sift = {
    "preprocess": {
        "blur_kernel" : 3,
    },
    "sift": {
        "algo" : 0,
        "trees": 3,
        "check": 3,
        "k": 2, #fixed, do not change
        "thres_good": 0.75,
    },
    "template": {
        "template_dir": global_var.TEMPLATE_DIR,
        "template_correct_dir": global_var.TEMPLATE_CORRECT_DIR,
        "topk": 3,
    }
}