#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <workspace-dir>"
    exit 1
fi

DOCKER_UNAME=docker-$(id -un)
DOCKER_NAME=dev-$(id -un)

docker run -it \
  --name $DOCKER_NAME \
  -e TERM=xterm-256color \
  -u $(id -u):$(id -g) \
  -v $1:/workspace \
  --ipc=host \
  --network host \
  --shm-size=512g \
  $DOCKER_NAME bash -c "python3 -c \"\$(curl -fsSL https://raw.githubusercontent.com/Fitree/dev-env-setup/refs/heads/main/scripts/autosetup.py)\" && zsh"
