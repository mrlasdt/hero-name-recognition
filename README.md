# Hero name recognition
## Installation
```
conda create -n <env_name> python=3.9
conda activate <env_name>
pip install -r requirements.txt

```
## Preparation
```
bash script/download_data.sh
bash script/prepare_template.sh
```

## Usage
Evaluation on test dataset:
```
bash script/predict.sh -i data/test_data/test_images -a data/test_data/test.txt
```

Evaluation on private dataset:
```
bash script/predict.sh -i <path to images folder>  -a <path to label file>
```