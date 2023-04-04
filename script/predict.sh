#bash script/predict.sh -i data/test_data/test_images -a data/test_data/test.txt -o out.txt
export PYTHONWARNINGS="ignore"

while getopts i:a:o: flag
do
    case "${flag}" in
        i) img=${OPTARG};;
        a) label_file=${OPTARG};;
        o) out_file=${OPTARG};;
    esac
done

python main.py \
    --image="$img" \
    --label_file  $label_file \
    --out_file  $out_file \
