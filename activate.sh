ECHO "ACTIVATING ENVIRONMENT!!!"
conda activate fastcasso
mkdir -p output

uvicorn main:app --reload