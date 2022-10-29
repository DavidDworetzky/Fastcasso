#!/bin/sh
set -e

mkdir output

if [ ! -z "$DEBUG" ]; then
  uvicorn main:app --reload
else
  uvicorn main:app --reload
fi