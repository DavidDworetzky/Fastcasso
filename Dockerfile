FROM python:3.8-slim

ENV FASTCASSO_HOME /opt/fastcasso
WORKDIR $FASTCASSO_HOME

RUN apt update && apt install -y \
    gcc \
    libpq-dev \
    make \
    curl

COPY environment.yml .
COPY Pipfile.lock .
RUN conda env create -f environment.yml && conda env activate stablediffusion

COPY . .

VOLUME /graphql

EXPOSE 5000
EXPOSE 5678
ENTRYPOINT ["./entrypoint.sh"]