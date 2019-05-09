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

SANDBOX_VERSION=${SANDBOX_VERSION:-5.1.2}
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
DOWNLOADS_DIR=$DIR/tmp
SANDBOX_ZIP="cdap-sandbox-$SANDBOX_VERSION.zip"
SANDBOX_ZIP_PATH=$DOWNLOADS_DIR/$SANDBOX_ZIP
SANDBOX_DIR=$DOWNLOADS_DIR/cdap-sandbox
SANDBOX_EXTRACTED_DIR=$SANDBOX_DIR/cdap-sandbox-$SANDBOX_VERSION
MARKETPLACE_DIR=$DOWNLOADS_DIR/cdap-marketplace
IGNORE_PLUGINS_FILE=$DIR/generate-plugins/.pluginsignore
PLUGINS_FILE=$DIR/../data/en/plugins_list.json
DEPS_FAILED=false
DEPS=(python git unzip wget)

_check_deps () {
  if [[ ! $(git lfs) ]]; then
    echo "You need to install 'git lfs'"
    DEPS_FAILED=true
  fi
  for dep in "${DEPS[@]}"; do
    if ! type $dep &> /dev/null; then
      echo "You need to install '$dep'"
      DEPS_FAILED=true
    fi
  done
  if [[ ! "$DEPS_FAILED" = false ]]; then
    exit 1
  fi
}

setup () {
  mkdir -p $DOWNLOADS_DIR
  _check_deps
}

log () {
  echo -e "$@"
}

download_sandbox () {
  if [[ ! -d "$SANDBOX_EXTRACTED_DIR" ]]; then
    log "Sandbox not found. Downloading..."
    if [[ -f "$SANDBOX_ZIP_PATH" ]]; then
      log "Sandbox archive found. Skip download"
    else
      wget -q https://downloads.cask.co/cdap-sandbox/cdap-sandbox-$SANDBOX_VERSION.zip -O $DOWNLOADS_DIR/$SANDBOX_ZIP
    fi
    log "Unzip sandbox"
    unzip -qq $SANDBOX_ZIP_PATH -d $SANDBOX_DIR
  else
    log "Sandbox found. Skip"
  fi
}

download_marketplace () {
  if [[ ! -d "$MARKETPLACE_DIR" ]]; then
    log "Clonning cdap-marketplace"
    git lfs clone https://github.com/cdapio/cask-marketplace.git $MARKETPLACE_DIR
  else
    log "Marketplace found. Skip"
  fi
}

generate_plugins () {
  log "Generating plugins list"
  python $DIR/generate-plugins/main.py $SANDBOX_EXTRACTED_DIR $MARKETPLACE_DIR -o $PLUGINS_FILE -i $IGNORE_PLUGINS_FILE
}

setup
download_sandbox
download_marketplace
generate_plugins
