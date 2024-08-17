#!/bin/bash

podman run -d --rm --name feedbackredis \
  -p 6379:6379 \
  registry.redhat.io/rhel9/redis-7:1-27
