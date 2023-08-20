## Local environment build of a specific feature branch
* Repo:  [gfs-bq-manager](https://github.com/amesones-dev/gfs-bq-manager.git).  
* Branch to build: [packaging](https://github.com/amesones-dev/gfs-bq-manager/tree/main)

### Clone repo and checkout specific branch
**Instructions**
```shell
# Local build
REPO='https://github.com/amesones-dev/gfs-bq-manager.git'
REPO_NAME='gfs-bq-manager'
git clone ${REPO}
cd ${REPO_NAME}

# Select branch. Ideally use a specific convention for branch naming
export FEATURE_BRANCH="packaging"
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
export TEST_ID=$(python -c "import uuid;print(uuid.uuid4())")
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
