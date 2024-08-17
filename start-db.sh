#!/bin/bash

podman run -d --rm --name feedbackdb \
  -e POSTGRESQL_USER=feedbackuser \
  -e POSTGRESQL_PASSWORD=feedbackpassword \
  -e POSTGRESQL_ADMIN_PASSWORD=adminpassword \
  -e POSTGRESQL_DATABASE=feedback \
  -p 5432:5432 \
  registry.redhat.io/rhel9/postgresql-15:1-74
