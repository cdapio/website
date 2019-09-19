# CDAP website

[![Build Status](https://travis-ci.org/cdapio/website.svg?branch=develop)](https://travis-ci.org/cdapio/website)


This site is built using [hugo](https://gohugo.io).
Follow [instruction](https://gohugo.io/getting-started/installing/) to install hugo.

## Up And Running

```bash
git clone --recurse-submodules https://github.com/cdapio/website.git
cd website
hugo server
```

Open `http://localhost:1313` in your browser, change some file and site will rebuild automatically.

## Build

Install [node.js](https://nodejs.org/en/download/).

```bash
npm install
hugo --gc --minify
```


## Plugins Generation CI

Plugins generation goes through Travis CI pipeline using a [dedicated branch](https://github.com/cdapio/website/tree/master-build-plugins).

There are few steps to make it work:

* Generate Github API token with repo read/write permission in order to create a pull request
* Set this token in `GITHUB_TOKEN` env variable in Travis CI
* Set `target` branch name in `MASTER_BRANCH` env variable in Travis CI. Pull request will be created against this branch

Now you can generate plugins by triggering the build manually using Travis UI.