#!/bin/bash

DOCKER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd $DOCKER_DIR

# Source container configuration
source ./container_config.sh

docker build . --rm \
    --build-arg UID=$DOCKER_UID \
    --build-arg GID=$DOCKER_GID \
    --build-arg UNAME=$DOCKER_UNAME \
    --tag $DOCKER_NAME \
    --file Dockerfile
