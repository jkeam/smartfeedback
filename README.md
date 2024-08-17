# Smart Feedback

Smart Feedback App

## OpenShift

### Pipeline

#### Setup

```shell
oc new-project feedback
oc apply -f ./openshift/pipeline/tasks.yaml
oc apply -f ./openshift/pipeline/pipeline.yaml
```

#### Triggering

```shell
oc create -f ./openshift/pipeline/pipelinerun.yaml
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
