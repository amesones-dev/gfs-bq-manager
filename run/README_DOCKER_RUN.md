## Local environment build of a specific feature branch
* Repo:  [gfs-bq-manager](https://github.com/amesones-dev/gfs-bq-manager.git).  
* Branch to build: [main](https://github.com/amesones-dev/gfs-bq-manager/tree/main)
* [Dockerfile](https://github.com/amesones-dev/gfs-bq-manager/blob/main/run/Dockerfile)  
* Running the application with  Flask: [start.py](https://github.com/amesones-dev/gfs-bq-manager/blob/main/src/start.py)

**Dockerfile**
```Dockerfile
# Python image to use.
FROM python:3.10-alpine
# Set the working directory to /app
WORKDIR /app
# copy the requirements file used for dependencies
COPY requirements.txt .
# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
# Copy the rest of the working directory contents into the container at /app
COPY . .

# Run start.py when the container launches
ENTRYPOINT ["python", "start.py"]
```
**Startup script run by docker image**
```python
# start.py
import os
from flask import Flask

from app import create_app
app = create_app()

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(host='0.0.0.0', port=int(server_port))
```

### Clone repo and checkout specific branch
**Instructions**
```shell
# Local build
REPO='https://github.com/amesones-dev/gfs-bq-manager.git'
REPO_NAME='gfs-bq-manager'
git clone ${REPO}
cd ${REPO_NAME}

# Select branch. Ideally use a specific convention for branch naming
export FEATURE_BRANCH="main"
# Check that the branch exists
git branch -a |grep ${FEATURE_BRANCH}

git checkout ${FEATURE_BRANCH}
# Output
    branch 'main' set up to track 'origin/main'.
    Switched to a new branch 'main'
````    

```shell
# Identify your build
# Usually automated CI systems provide UUID for build IDs and maintains a Build ID database
export BUILD_ID=$(python -c "import uuid;print(uuid.uuid4())")

# Use a meaningful local docker image tag for the build
# Automated CI systems can generate a docker image tag for you
export RID="${RANDOM}-$(date +%s)" 
export LOCAL_DOCKER_IMG_TAG="${REPO_NAME}-${FEATURE_BRANCH}-${RID}"

```
```shell
# Running code integrated unittests
export TID=$(python -c "import uuid;print(uuid.uuid4())")
# Tests named based on build docker image
export LOCAL_DOCKER_IMG_TAG_TEST="test-${LOCAL_DOCKER_IMG_TAG}"
docker build . -f ./run/Dockerfile-tests   -t ${LOCAL_DOCKER_IMG_TAG_TEST}  --no-cache --progress=plain  2>&1 | tee ${BUILD_ID}.log


# You may want to use a different set of environment variables to run tests
# Alternatively, code built-in tests can use a specific configuration defined inline.
export TEST_BQ_SA_KEY_JSON_FILE='/etc/secrets/sa_key_bq.json'
export FLASK_SECRET_KEY=$(openssl rand -base64 128) 

# Known local path containing  SA key sa_key_bq.json for testing
export LOCAL_SA_KEY_PATH='/secure_location'
docker run -e TEST_BQ_SA_KEY_JSON_FILE -e FLASK_SECRET_KEY -v "${LOCAL_SA_KEY_PATH}":/etc/secrets  ${LOCAL_DOCKER_IMG_TAG_TEST} 2>&1|tee ${TEST_ID}-result.log
grep 'OK' ""${TEST_ID}-result.log"" 

```

#### Build
```shell

# Launch build process with docker
# The build is done with your local environment docker engine
# docker build ./src -f ./run/Dockerfile -t ${LOCAL_DOCKER_IMG_TAG}
# With logs captured to file 
docker build . -f ./run/Dockerfile -t ${LOCAL_DOCKER_IMG_TAG} --no-cache --progress=plain  2>&1 | tee ${BUILD_ID}.log
# CI systems usually send builds to automated build engine APIs
```

#### Run the newly built docker image
* Set container port for running application
```shell
# Default container port is 8080 if PORT not specified
export PORT=8081
export BQ_SA_KEY_JSON_FILE='/etc/secrets/sa_key_bq.json'
export FLASK_SECRET_KEY=$(openssl rand -base64 128) 

# Known local path containing SA key sa_key_bq.json
export LOCAL_SA_KEY_PATH='/secure_location'

# Set environment with -e
# Publish app port with -p 
# Mount LOCAL_SA_KEY_PATH to /etc/secrets in running container
docker run -e PORT -e BQ_SA_KEY_JSON_FILE -e FLASK_SECRET_KEY -p ${PORT}:${PORT}  -v "${LOCAL_SA_KEY_PATH}":/etc/secrets  ${LOCAL_DOCKER_IMG_TAG}
```


*Basic endpoint testing (Smoke Test)*
```shell
# Basic app endpoints tests
# Main url
curl --head  localhost:8081
# Output
  HTTP/1.1 200 OK
  Content-Type: text/html; charset=utf-8
  ...
  
# The app implements a /healthcheck endpoint that can be used for liveness and readiness probes
# Output set by app design
curl -i localhost:8081/healthcheck
  HTTP/1.1 200 OK
  ...
  Content-Type: application/json

  {"status":"OK"}

# Test any app endpoints as needed
export ENDPOINT='index'
curl -I  localhost:8081/${ENDPOINT}
# Output 
  HTTP/1.1 200 OK
  ...
 
curl -I -s  localhost:8081/${ENDPOINT} --output http-test-${ENDPOINT}.log
grep   'HTTP' http-test-${ENDPOINT}.log
# Output
  HTTP/1.1 200 OK

# Non existent endpoint
export ENDPOINT=app_does_not_implement
curl -I -s  localhost:8081/${ENDPOINT} --output http-test-${ENDPOINT}.log 
grep   'HTTP' http-test-${ENDPOINT}.log
# Output
  HTTP/1.1 404 NOT FOUND
   
```
