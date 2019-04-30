#! /bin/bash

#  Copyright © 2019 CDAP
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# https://stackoverflow.com/questions/34405047/how-do-you-merge-into-another-branch-using-travis-with-git-commands

#
# Before running this script you need to specify 2 env variables through Travis UI
# - GITHUB_TOKEN - token that has `repo` permissions
# - MASTER_BRANCH - source branch. Pull request will be created against this branch
# Optional variables
# - COMMIT_MSG - commit message text
# - FILE_TO_CHECK - file to check changes. By default it is path to plugins_list.json

FILE_TO_CHECK=${FILE_TO_CHECK:-$TRAVIS_BUILD_DIR/data/en/plugins_list.json}
PULL_REQUEST_NAME=${PULL_REQUEST_NAME:-"Add new plugins"}
COMMIT_MSG=${COMMIT_MSG:-"Update plugins list"}

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

build_head=""

validate() {
  deps_failed=false
  if [ -z "$GITHUB_TOKEN" ]; then
    echo "You need to specify GITHUB_TOKEN env variable"
    deps_failed=true
  fi
  if [ -z "$MASTER_BRANCH" ]; then
    echo "You need to specify MASTER_BRANCH env variable"
  fi
  if [[ ! "$deps_failed" = false ]]; then
    exit 1
  fi
}

setup_git() {
  git config --global user.email "travis@travis-ci.org"
  git config --global user.name "Travis CI"
}

setup_git_branches() {
    # Keep track of where Travis put us.
    # We are on a detached head, and we need to be able to go back to it.
    build_head=$(git rev-parse HEAD)

    # Fetch all the remote branches. Travis clones with `--depth`, which
    # implies `--single-branch`, so we need to overwrite remote.origin.fetch to
    # do that.
    git config --replace-all remote.origin.fetch +refs/heads/*:refs/remotes/origin/*
    git fetch origin $MASTER_BRANCH

    echo "checkout master branch"
    git checkout -qf $MASTER_BRANCH
}

make_pr() {
  branch_name=plugins-pr-$TRAVIS_BUILD_NUMBER
  echo "check if current build is a pull request build"
  if [ "$TRAVIS_PULL_REQUEST" != "false" ]; then
    echo "this build is already a pull request one"
    exit 0
  fi

  echo "check if current branch is master"
  if [ "$TRAVIS_BRANCH" == "$MASTER_BRANCH" ]; then
    echo "skipping pull request from master to master"
    exit 0
  fi

  echo "create new branch"
  git checkout -b $branch_name

  echo "commit new changes"
  git add $FILE_TO_CHECK
  git commit -m "$COMMIT_MSG"

  git remote add origin-plugins https://${GITHUB_TOKEN}@github.com/dbuzhorkaa/website.git > /dev/null 2>&1
  git push --quiet --set-upstream origin-plugins $branch_name

  echo "open pull request"
  hub pull-request -m "$PULL_REQUEST_NAME" --base=$MASTER_BRANCH
}

generate_plugins() {
  /bin/bash $DIR/build-plugins-list.sh
}

check_and_create_pr() {
  diff=$(git diff HEAD~1 -- "$FILE_TO_CHECK")

  if [ -z "$diff" ]; then
    echo "$FILE_TO_CHECK file was not changed"
  else
    echo "$FILE_TO_CHECK file was updated, making pull request"
    make_pr
  fi
}


validate
setup_git
setup_git_branches
generate_plugins
check_and_create_pr
