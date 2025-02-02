#!/bin/bash

DOCKER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd $DOCKER_DIR

DOCKER_UNAME=docker-$(id -un)
DOCKER_NAME=dev-$(id -un)

docker build . --rm \
    --build-arg UID=$(id -u) \
    --build-arg GID=$(id -g) \
    --build-arg UNAME=$DOCKER_UNAME \
    --tag $DOCKER_NAME \
    --file Dockerfile
