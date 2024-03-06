#! /bin/sh

DATA=$1
PORT=$2
TAG=icodegen

docker run --gpus all -d -p $PORT:8888 --user root \
	-e NB_GROUP=grad -e NB_UID=$(id -u) -e NB_GID=$(id -g) \
	-e JUPYTER_ENABLE_LAB=yes -v "$PWD":/home/jovyan/work \
	-v "$DATA":/home/jovyan/data --name $(whoami)-$TAG \
	semerulab/datascience:dev-cuda110
