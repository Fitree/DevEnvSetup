#!/bin/bash

# Container user configuration
DOCKER_UNAME="docker-$(id -un)"

# Container name and tag
DOCKER_NAME="dev-ubt2204-cu124-py310"

# Container user IDs
DOCKER_UID="$(id -u)"
DOCKER_GID="$(id -g)" 