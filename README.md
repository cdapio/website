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

## Update for new CDAP version

To update website for new CDAP release version run the `python3` script present at `scripts\content\add_release_content.py`.

This script prompts for 2 inputs:
1. CDAP version in the format `6.X.Y`. Eg. `6.8.0` or `6.7.3`
2. Release notes link. Eg. `https://cdap.atlassian.net/wiki/spaces/DOCS/pages/1872232449/CDAP+Release+6.8.1`

Here is the output from a sample run for `6.8.1` release.

```
$ python3 add_release_content.py 
Adding content for new CDAP version...


Enter the CDAP version (Eg. 6.8.0, 6.7.3):
6.8.1

[1/3] Generating get-started card files...

Enter the CDAP release notes link:
https://cdap.atlassian.net/wiki/spaces/DOCS/pages/1872232449/CDAP+Release+6.8.1
Reading template from: "./templates/docker-template.md" to generate file: "../../content/en/get-started/cards/docker-681.md"
Reading template from: "./templates/linux-mac-template.md" to generate file: "../../content/en/get-started/cards/linux-mac-681.md"
Reading template from: "./templates/vm-template.md" to generate file: "../../content/en/get-started/cards/vm-681.md"

[2/3] Updating get-started json data...
Updating data file ../../data/en/get_started.json

[3/3] Updating news json data...
Updating news json file ../../data/en/news.json
```
