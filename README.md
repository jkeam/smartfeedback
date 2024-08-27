# Smart Feedback

Smart Feedback App

## OpenShift

### Kustomize

#### Granite

1. Copy `.env.ai.template` to `./openshift/ai/.env`
2. Fill in `./openshift/ai/.env` with real values
3. Deploy

    ```shell
    oc apply -k ./openshift/ai
    ```

#### App

1. Copy `.env.template` to `./openshift/app/.env`
2. Fill in `./openshift/app/.env` with real values
3. Deploy

    ```shell
    # create proj
    oc new-project feedback

    # create db
    oc new-app --name=feedback-db \
    --image=registry.redhat.io/rhel9/postgresql-15:1-74 \
    --env POSTGRESQL_ADMIN_PASSWORD=adminpassword\
    --env POSTGRESQL_PASSWORD=feedbackpassword \
    --env POSTGRESQL_USER=feedbackuser \
    --env POSTGRESQL_DATABASE=feedback \
    --labels 'app=feedback-db' \
    --namespace feedback

    # create redis
    oc new-app --name=feedback-redis \
    --image=registry.redhat.io/rhel9/redis-7:1-27 \
    --labels 'app=feedback-redis' \
    --namespace feedback

    # deploy app
    oc apply -k ./openshift/app
    ```

### Pipeline

#### Setup

Create project.

```shell
oc new-project feedback
```

Standup database.

```shell
oc new-app --name=feedback-db \
  --image=registry.redhat.io/rhel9/postgresql-15:1-74 \
  --env POSTGRESQL_ADMIN_PASSWORD=adminpassword\
  --env POSTGRESQL_PASSWORD=feedbackpassword \
  --env POSTGRESQL_USER=feedbackuser \
  --env POSTGRESQL_DATABASE=feedback \
  --labels 'app=feedback-db' \
  --namespace feedback
```

Standup redis.

```shell
oc new-app --name=feedback-redis \
  --image=registry.redhat.io/rhel9/redis-7:1-27 \
  --labels 'app=feedback-redis' \
  --namespace feedback
```

Create pipeline.

```shell
oc apply -f ./openshift/pipeline/tasks.yaml --namespace feedback
oc apply -f ./openshift/pipeline/pipeline.yaml --namespace feedback
```

#### Triggering

```shell
oc create -f ./openshift/pipeline/pipelinerun.yaml --namespace feedback
```

## Local

### Prerequisite

1. Python 3.12

### Environment

1. Clone this repo
2. `python3.12 -m venv venv && source ./venv/bin/activate`
3. `pip install -r ./requirements.txt`
4. `cp ./.env.template ./.env`
5. Update values in `./.env`

### Application

1. Migrate db

    ```shell
    python ./manage.py migrate
    ```

2. Create superuser

    ```shell
    DJANGO_SUPERUSER_PASSWORD=password1 python ./manage.py createsuperuser --username admin --email admin@example.com --noinput
    ```

## Docs

1. [Django Packages](https://djangopackages.org)
2. [Class-Based View Docs](https://ccbv.co.uk/)
3. [Django Docs](https://docs.djangoproject.com/en/5.0/)
