#!/bin/bash

DOCKER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd $DOCKER_DIR

# Source container configuration
source ./container_config.sh

if [ -z "$1" ]; then
    echo "Usage: $0 <workspace-dir> [container-name]"
    exit 1
fi

WORKSPACE_DIR=$1
if [ -z "$2" ]; then
    echo "No container name provided. Using default: $DOCKER_NAME"
    CONTAINER_NAME="$DOCKER_NAME"
else
    CONTAINER_NAME=$2
fi

SSH_DIR="$HOME/.ssh"
if [ -d "$SSH_DIR" ]; then
    MOUNT_SSH="-v $SSH_DIR:/home/$DOCKER_UNAME/.ssh"
else
    echo "$SSH_DIR will not be mounted. It does not exist."
    MOUNT_SSH=""
fi

docker run -it \
    --name $CONTAINER_NAME \
    -e TERM=xterm-256color \
    -u $DOCKER_UID:$DOCKER_GID \
    -v $WORKSPACE_DIR:/workspace \
    --ipc=host \
    --network host \
    --shm-size=512g \
    $MOUNT_SSH \
    $DOCKER_NAME bash -c "python3 -c \"\$(curl -fsSL https://raw.githubusercontent.com/Fitree/dev-env-setup/refs/heads/main/scripts/autosetup.py)\" && zsh"
