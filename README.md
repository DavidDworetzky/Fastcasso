# Fastcasso
Fastcasso is a web server for diffusion and GAN based image generation. 
Fastcasso makes running stable diffusion on a web server easy and fast.
# How to Run

## Pre installation steps
1. huggingface-cli login
2. If running from CLI instead of docker, `python initdb.py`

## Running with uvicorn

1. `uvicorn main:app --reload`
2. `navigate to 127.0.0.1:8000/docs`

## Running with docker

1. `docker build -t fastcasso .`
2. `docker run -dp 8000:8000 fastcasso`

## Additional Notes

1. Default settings / pipelines are indexed against Mac M1.
