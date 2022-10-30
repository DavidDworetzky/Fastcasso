# Fastcasso
Fastcasso is a project intended to make image gen, image to image, and art generation available in a neat fastapi package
# How to Run

## Running with uvicorn

1. `uvicorn main:app --reload`
2. `navigate to 127.0.0.1:8000/docs`

## Running with docker

1. `docker build -t fastcasso .`
2. `docker run -dp 8000:8000 fastcasso`

## Additional Notes

1. Default settings / pipelines are indexed against Mac M1.