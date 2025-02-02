#!/bin/bash

DOCKER_UNAME=docker-$(id -un)
DOCKER_NAME=dev-$(id -un)

docker build . --build-arg UID=$(id -u) --build-arg GID=$(id -g) --build-arg UNAME=$DOCKER_UNAME --build-arg --rm -t $DOCKER_NAME -f Dockerfile
