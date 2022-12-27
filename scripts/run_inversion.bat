set MODEL_NAME="runwayml/stable-diffusion-v1-5"
set DATA_DIR="path-to-dir-containing-images"
set TOKEN_NAME="<dog-remy>"

accelerate launch textual_inversion.py ^
--pretrained_model_name_or_path=$MODEL_NAME ^
--train_data_dir=$DATA_DIR ^
--learnable_property="object" ^
--placeholder_token="<dog-remy>" --initializer_token="dog" ^
--resolution=512 ^
--train_batch_size=1 ^
--gradient_accumulation_steps=4 ^
--max_train_steps=3000 ^
--learning_rate=5.0e-04 --scale_lr ^
--lr_scheduler="constant" ^
--lr_warmup_steps=0 ^
--output_dir="textual_inversion_dog"