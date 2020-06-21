# Scrapy Project for The Ringer

[The Ringer](https://theringer.com) is a popular media site focused on
sports and pop culture. This project exists to scrape content from the
site for use in machine learning and topic modeling. Many thanks to its
journalists for the content!

## The project: theringer

The [Scrapy](https://scrapy.org) project is a simple one, with a single
spider. The project was created by running:

```powershell
\> scrapy startproject theringer
```

Note, the directory created by this command *is* the repository root.

## The conda environment

The environment for running scrapy can be created using the included
`package-list.txt` file:

```powershell
\> conda create -name ringer --file package-list.txt
```

## Spiders

The only spider in the project is `ArticlesSpider`. It crawls content
from `https://www.theringer.com/archives/`, starting from the present
year and month and working backwards until the beginning of the
archive's history, December of 2015.

## Running

The repository includes a `launch.json` file for VS Code users. For
others, the spider can be run as follows:

```powershell
\> scrapy crawl articles -o articles.json
```

Output is JSON formatted. Different filenames and locations can be
used for capture; `articles.json` is suggested as the repository is
configured to ignore this file.