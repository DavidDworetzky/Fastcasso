FROM python:3.8-slim

ENV FASTCASSO_HOME /opt/fastcasso
WORKDIR $FASTCASSO_HOME

RUN apt update && apt install -y \
    gcc \
    libpq-dev \
    make \
    curl \
    wget
RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh 
RUN conda --version
COPY environment.yml .
RUN conda env create -f environment.yml && conda env activate stablediffusion

COPY . .

VOLUME /graphql

EXPOSE 5000
EXPOSE 5678
EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]