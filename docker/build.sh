# A build script for the Dockerfile
#
# This script performs the following actions:
#
# - perform the build
# - run automated smoke tests, to check if the image is not totally broken
# - push the generated image to the registry
#
# Built images are given duplicate tags:
#
# - one for the current git branch
# - the current git commit

set -e

IMAGE_NAME=saeoss

GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD | tr / -)
GIT_COMMIT=$(git rev-parse --short HEAD)

# use branch+commit for tagging
sudo docker image build \
    --no-cache \
    -t "$IMAGE_NAME:$GIT_BRANCH" \
    -t "$IMAGE_NAME:$GIT_COMMIT" \
    --label git-commit=$GIT_COMMIT \
    --label git-branch=$GIT_BRANCH \
    --build-arg "BUILDKIT_INLINE_CACHE=1" \
    --build-arg "GIT_COMMIT=$GIT_COMMIT" \
    ..

# run smoke tests
# python3 smoketest.py $IMAGE_NAME:$GIT_BRANCH

# push to docker registry
#docker push "$IMAGE_NAME:GIT_BRANCH"
#docker push "$IMAGE_NAME:GIT_COMMIT"
