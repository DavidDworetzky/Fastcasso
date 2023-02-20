# Fastcasso
Fastcasso is a web server and UI for diffusion based image generation
Fastcasso makes running stable diffusion on a web server easy and fast.
Fastcasso will also support other types of image generation / fine tune / asset generation in the future.

# How to Run

## Pre installation steps
1. huggingface-cli login
2. If running from CLI instead of docker, `python initdb.py`
3. Set .env values
- POSTGRES_PWD
- DEVICE_TYPE (generally cuda or mps)
4. Create appropriate conda environment depending for either windows or mac.

## Running with uvicorn or bootstrap.py

1. `uvicorn main:app --reload`
2. `navigate to 127.0.0.1:8000/docs`
3.  Can also run `python bootstrap.py`

## Running with docker

1. `docker build -t fastcasso .`
2. `docker run -dp 8000:8000 fastcasso`

## Additional Notes and Features

1. Default settings / pipelines are tested against CUDA device types on windows.
2. Mac also supported, simply swap out for MPS device type.
3. Some Hardcoded presets include stable diffusion 1.4, 1.5, 2.0 and 2.1 with certain fine tunes. 512 and 768 resolution on certain diffuser pipelines.
4. Supports search on generated images.
5. Supports custom presets. (used for specifying parameters, keywords, negative keywords.)
6. UI for testing / exploration.

## Feature Roadmap

1. Fastcasso will support the following features in the future (view issues for exact list):
- Textual embeddings.
- Custom Model Training.
- Queued Jobs.
- In and Out painting.
