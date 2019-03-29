# CDAP website

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
