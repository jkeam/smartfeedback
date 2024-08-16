#!/bin/bash

podman run -d --rm --name adminer -p 8080:8080 -e ADMINER_DEFAULT_SERVER=localhost -e ADMINER_DESIGN=nette -i docker.io/adminer:4.7.9
