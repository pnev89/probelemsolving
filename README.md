# Testing projec 

This is just a simple example

## Precommit Hooks

We use [pre-commit](https://pre-commit.com/) to enforce e.g. code formatting,
linting and type checking prior to committing to the repository.
The `.pre-commit-config.yaml` in the repository includes all of the requirements.
The required packages must be declared on `pyproject.toml`.

Prior to your first commit you need to run

```zsh
pre-commit install
```

If you want to manually run it on all files without a commit

```zsh
pre-commit run --all-files
```

### Setup environment

#### Poetry virtual env

In order to setup the environment you need to
[download poetry](https://python-poetry.org/docs/) and install it using

```zsh
poetry install
```

After that you need to start the environment. For that you should use:

```zsh
poetry shell
```

## How to setup the Mysql server

- Install docker on your computer

- Build docker image:

    ```bash
    docker build -t mysql_db -f database/Dockerfile .
    ```

- Run mysql docker image
    
    ```bash
    docker run mysql_db
    ```

- Connect the mySql server from within the container 
(enter password provided with the command above)

    ```bash
    bash-3.2$ docker exec -it [CONTAINER_ID] /bin/bash
    ```
- To setup mysql do:

    ```bash
    cd docker-entrypoint-initdb.d/  
    ```

    ```bash
    mysql -proot
    ```

- The database [classicmodels](database/mysqlsampledatabase.sql) is already created




## How to run API

To dockerize the `FastAPI` app is necessary to run the following steps:

- Install docker on your computer

- Build docker image:

    ```bash
    docker build -f api/Dockerfile .
    ```

- Run docker container:

    ```bash
    docker run -p 3306:3306 IMAGE_ID
    ```







- Declare databricks environmental variables in a .env file.

```bash
    DATABRICKS_SERVER_HOSTNAME=dbc-5fd9856c-37d3.cloud.databricks.com
    DATABRICKS_HTTP_PATH=sql/protocolv1/o/2943926958937924/1118-101136-z3jws8ur
```

Ask Data Team to provide a `DATABRICKS_TOKEN` for you.

- Run docker container:

    ```bash
    docker run --env-file .env -p 8000:8000 IMAGE_ID
    ```

The `.env` file must have the databricks credentials.

If you will not use docker, and after you declare the environmental variables,
you can just type:

```bash
uvicorn recsys_engine.api.recommender_system.main:app --host [HOST] --port [PORT]
```

If localhost, the Host is 0.0.0.0 or 127.0.0.1 and the port can be 8080

- Execute POST request like:

```bash
curl -X 'POST' \
  'http://0.0.0.0:8000/engages/simple_request/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"teams": ["bdr", "sales"], "country": ["United States", "United Kingdom"]}'
```

### Load Test API

To test the API we are using [Locust](https://locust.io/).
You can use the following command to launch it:

```bash
locust -f PATH_TO_LOAD_TESTS_FOLDER --host [API_HOST]:[API_PORT]
--exclude-tags [TAGS_TO_EXCLUDE] --class-picker
```

## Precommit Hooks

We use [pre-commit](https://pre-commit.com/) to enforce e.g. code formatting,
linting and type checking prior to committing to the repository.
The `.pre-commit-config.yaml` in the repository includes all of the requirements.
The required packages must be declared on `pyproject.toml`.

Prior to your first commit you need to run

```zsh
pre-commit install
```

If you want to manually run it on all files without a commit

```zsh
pre-commit run --all-files
```

### Setup environment

#### Poetry virtual env

In order to setup the environment you need to
[download poetry](https://python-poetry.org/docs/) and install it using

```zsh
poetry install
```

After that you need to start the environment. For that you should use:

```zsh
poetry shell
```

To install an optional dependencies you can run:

```zsh
poetry install --extras <package>
```

To install all the optional dependencies run:

```zsh
poetry install --extras all
```

##### Private repositories

This repository has a private package dependency: `reachdesk-ds-prod`.
We have two options to install this package, directly from git or
through aws codeartifact. We choose the code artifact since this doesn't
need to handle git hub credentials and can communicate directly in the
AWS Databricks environment via IAM role.

In the `pyproject.toml` the `reachdesk-ds-prod` package is tagged as `extra`.
The reason for this is that when using `dbx` to run the `data-platform` jobs
if this action was not set it will try to install the package on the target cluster.
Since is necessary to provide a code artifact token in order to poetry have
the authorization to access the codeartifact, the code launch
(`dbx execute` or `dbx launch`) breaks because it cannot do the
`aws codeartifact login` specified on the cluster `init_script`:
 `packages/upload_init_scripts.py`. Within the `extras` the
`poetry build` excludes this package from the installation/wheel generation.
More details will be described about how to install this in the Databricks runtime.

To install this package for use locally via `databricks-connect` you can perform
the following action:

```zsh
export POETRY_HTTP_BASIC_CODEARTIFACT_USERNAME=aws
export POETRY_HTTP_BASIC_CODEARTIFACT_PASSWORD=$(aws codeartifact \
    get-authorization-token \
    --domain reachdesk \
    --domain-owner 517025229481 \
    --query authorizationToken \
    --output text)
```

to export the necessary variables and

```zsh
poetry install --extras recsys
```

to install the required packages

With this the package will be installed on the poetry environment.

###### Package troubleshooting

If you faced errors regarding the `reachdesk-ds-prod` hash execute
the following commands:

- Clean poetry artifact storage:

    ``` zsh
    rm -r ~/Library/Caches/pypoetry/artifacts
    ```

- Clear poetry cache

    ``` zsh
    poetry cache clear --all .
    ```

- Remove `poetry.lock`
- Reinstall environment
