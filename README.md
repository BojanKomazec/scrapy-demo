# scrapy-demo
Scrapy framework demo project

# Why Scrapy?

Libraris like Requests and BeautifulSoup can extract data from HTML web pages but are not suitable for complex projects. They can be used for simple tasks like scraping a single HTML page but are not suitable for e.g. scraping hundreds of web pages simultanuosly.

On my machine, Scrapy benchmark showed it can scrape 2940 pages per minute (this depends on CPU, available RAM etc...):

```
$ scrapy bench
...
2020-04-25 23:57:12 [scrapy.extensions.logstats] INFO: Crawled 646 pages (at 2940 pages/min), scraped 0 items (at 0 items/min)
...
```

# Scrapy Architecture

* Spiders
* Pipelines
* Middleware
* Engine
* Scheduler


## Spiders

This is where we define what we want to extract from a web page.

It is responsible for scraping the content from a web page (web response).

There are different types/classes of spiders:
* scrapy.Spider
* CrawlSpider
* XMLFeedSpider - for scraping XML files
* CSVFeedSpider - for scraping comma-separated values files
* SitemapSpider - for scraping sitemaps

Within a project we usually create one or more spiders.

## Pipelines

Used for processing extracted data. E.g.:
* Cleaning the data
* Removing duplication
* Storing data in external database

## Middleware

Deals with web requests and responses. E.g.:
* Injecting custom headers
* Proxying

## Engine

Coordinates all other components

## Scheduler

Preserves the order of operations. Implemented as queue (FIFO).

## How do they work together?

Spider sends request to Engine.

Engine transmits it to Scheduler.

If there was some request sent earlier, this one would be served first.

Scheduler sends request to be served back to Engine.

Engine sends request to Middleware (Downloader Middleware, responsible for getting response from the target website).

Middleware sends response to the Engine.

Engine then sends response to Spider (Spider Middleware which is responsible for extracting data).

Extracted data is then sent to Engine which forwards it to Pipeline which processes data.

# robots.txt

Most of websites contain a file `robots.txt` in root directory.

It gives instructions to spiders whether they can crawl/scrape the website and if yes, then which content (pages).

It contains a set of grouped instructions. Each group contains 3 properties:
* `User-Agent`: name of the agent; represents the identity of the spider
* `Allow`: specifies path (web page) that can be crawled/scraped
* `Disallow`: specifies path (web page) that must NOT be crawled/scraped

Example of `robtots.txt` for website which allows scraping any page:
```
User-Agent: *
Disallow:
Allow: /
```

# How to install Scrapy

Scrapy should be installed in virtual environment in order not to mess up globally installed packages:

```
$ virtualenv --python=python3.6 venv
$ source venv/bin/activate
(venv) $ pip install scrapy
```

# Scrapy CLI

```
$ scrapy
Scrapy 2.1.0 - no active project

Usage:
  scrapy <command> [options] [args]

Available commands:
  bench         Run quick benchmark test
  fetch         Fetch a URL using the Scrapy downloader
  genspider     Generate new spider using pre-defined templates
  runspider     Run a self-contained spider (without creating a project)
  settings      Get settings values
  shell         Interactive scraping console
  startproject  Create new project
  version       Print Scrapy version
  view          Open URL in browser, as seen by Scrapy

  [ more ]      More commands available when run from project directory

Use "scrapy <command> -h" to see more info about a command
```

To run a benchmark:
```
$ scrapy bench
```

To fetch HTML of a web page:
```
$ scrapy fetch https://www.google.com
```

shell is used to perform some experiments on web sites we want to scrape, before writing a spider.


# How to create a project?

In this repo, project (and directory) `worldometers` was created with:

```
(venv) $ scrapy startproject worldometers
New Scrapy project 'worldometers', using template directory '/home/xxx/dev/github/scrapy-demo/venv/lib/python3.6/site-packages/scrapy/templates/project', created in:
    /home/xxx/dev/github/scrapy-demo/worldometers

You can start your first spider with:
    cd worldometers
    scrapy genspider example example.com
```


