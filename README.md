# scrapy-demo
Scrapy framework demo project

# Why Scrapy?

Libraries like Requests and BeautifulSoup can extract data from HTML web pages but are not suitable for complex projects. They can be used for simple tasks like scraping a single HTML page but are not suitable for e.g. scraping hundreds of web pages simultanuosly.

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

There are two types of middleware:
* Downloader Middleware - responsible for sending request and getting response from the target website
* Spider Middleware - responsible for extracting data from response

## Engine

Coordinates all other components

## Scheduler

Preserves the order of operations. Implemented as queue (FIFO).

## How do they work together?

Spider sends request to Engine.

Engine transmits it to Scheduler. If there was some request sent earlier, this one would be served first. Scheduler sends request to be served back to Engine.

Engine sends request to Middleware (Downloader Middleware, responsible for getting response from the target website). Middleware sends response to the Engine.

Engine then sends response to Spider (Spider Middleware which is responsible for extracting data). Extracted data is then sent to Engine.

Engine forwards data to Pipeline which processes it.

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

This creates: `scrapy.cfg` file and `worldometers` directory within `worldometers` directory.

`scrapy.cfg` is important for executing spiders we create and for deploying our spiders to Scrapy deamon, Heroku etc...

`worldometers/worldometers/spiders` is initially an empty Python module (contains only `__init__.py`). This is where out spiders will be implemented.

`worldometers/worldometers/items.py` is used to clean the data we scrape and to store the data inside fields we created. In our case it contains (initially an empty) class `WorldometersItem` which inherits `scrapy.Item`.

`worldometers/worldometers/middlewares.py` contains middlewares which are responsible for requests and responses:
* class `WorldometersDownloaderMiddleware` - Downloader Middleware.
* class `WorldometersSpiderMiddleware` - Spider Middleware.

`worldometers/worldometers/pipelines.py` contains class `WorldometersPipeline` for storing scraped items into data base.

`worldometers/worldometers/settings.py` contains various settings.

# How to create a spider within a project?

It is possible to have multiple spiders within a project. Each spider is uniquely identified by its name.

Example: we want to scrape data from https://www.worldometers.info/world-population/population-by-country/.

![Countries in the world by population](worldometer-countries-homepage.png)

```
$ scrapy genspider countries www.worldometers.info/world-population/population-by-country
Created spider 'countries' using template 'basic' in module:
  worldometers.spiders.countries
```

This creates file `worldometers/worldometers/spiders/countries.py` which contains class `CountriesSpider` which inherits `scrapy.Spider`. It has the following predefined properties:
* `name` - set to name uniquely identifies this spider: `countries`
* `allowed_domains` - list of domain names that spider is allowed to access and scrape. Originally it contains `www.worldometers.info/world-population/population-by-country` but we can remove path in this url and leave only domain name: `www.worldometers.info/`. If any scraped page contains links to web pages at any other domain name, those pages will not be scraped. Domain name does not contain protocol prefix (e.g. `http://`).
* `start_urls` - contains all the links we want to scrape. Originally, it contains `http://www.worldometers.info/world-population/population-by-country/` (Scrapy uses `http://` protocol by default) but we can change it to `https://www.worldometers.info/world-population/population-by-country/` (if website supports https).

This class also contains `parse` method receives a response as its parameter.

# Scrapy shell

It is used before we build spiders, to experiment with website and do some basic element selection, do debug XPath expressions or CSS selectors.
`ipython` package has to be installed.

```
$ scrapy shell
2020-04-28 07:56:52 [scrapy.utils.log] INFO: Scrapy 2.1.0 started (bot: worldometers)
2020-04-28 07:56:52 [scrapy.utils.log] INFO: Versions: lxml 4.5.0.0, libxml2 2.9.10, cssselect 1.1.0, parsel 1.5.2, w3lib 1.21.0, Twisted 20.3.0, Python 3.6.9 (default, Apr 18 2020, 01:56:04) - [GCC 8.4.0], pyOpenSSL 19.1.0 (OpenSSL 1.1.1g  21 Apr 2020), cryptography 2.9.2, Platform Linux-4.15.0-96-generic-x86_64-with-Ubuntu-18.04-bionic
2020-04-28 07:56:52 [scrapy.utils.log] DEBUG: Using reactor: twisted.internet.epollreactor.EPollReactor
2020-04-28 07:56:52 [scrapy.crawler] INFO: Overridden settings:
{'BOT_NAME': 'worldometers',
 'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
 'LOGSTATS_INTERVAL': 0,
 'NEWSPIDER_MODULE': 'worldometers.spiders',
 'ROBOTSTXT_OBEY': True,
 'SPIDER_MODULES': ['worldometers.spiders']}
2020-04-28 07:56:52 [scrapy.extensions.telnet] INFO: Telnet Password: a9bcdf89cb40008b
2020-04-28 07:56:52 [scrapy.middleware] INFO: Enabled extensions:
['scrapy.extensions.corestats.CoreStats',
 'scrapy.extensions.telnet.TelnetConsole',
 'scrapy.extensions.memusage.MemoryUsage']
2020-04-28 07:56:52 [scrapy.middleware] INFO: Enabled downloader middlewares:
['scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware',
 'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware',
 'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware',
 'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware',
 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware',
 'scrapy.downloadermiddlewares.retry.RetryMiddleware',
 'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware',
 'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware',
 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware',
 'scrapy.downloadermiddlewares.cookies.CookiesMiddleware',
 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware',
 'scrapy.downloadermiddlewares.stats.DownloaderStats']
2020-04-28 07:56:52 [scrapy.middleware] INFO: Enabled spider middlewares:
['scrapy.spidermiddlewares.httperror.HttpErrorMiddleware',
 'scrapy.spidermiddlewares.offsite.OffsiteMiddleware',
 'scrapy.spidermiddlewares.referer.RefererMiddleware',
 'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware',
 'scrapy.spidermiddlewares.depth.DepthMiddleware']
2020-04-28 07:56:52 [scrapy.middleware] INFO: Enabled item pipelines:
[]
2020-04-28 07:56:52 [scrapy.extensions.telnet] INFO: Telnet console listening on 127.0.0.1:6023
[s] Available Scrapy objects:
[s]   scrapy     scrapy module (contains scrapy.Request, scrapy.Selector, etc)
[s]   crawler    <scrapy.crawler.Crawler object at 0x7f1244bf6278>
[s]   item       {}
[s]   settings   <scrapy.settings.Settings object at 0x7f1244c72dd8>
[s] Useful shortcuts:
[s]   fetch(url[, redirect=True]) Fetch URL and update local objects (by default, redirects are followed)
[s]   fetch(req)                  Fetch a scrapy.Request and update local objects
[s]   shelp()           Shell help (print this help)
[s]   view(response)    View response in a browser
>>>
```

Let's try to fetch a web page:

```
>>> fetch("https://www.worldometers.info/world-population/population-by-country/")
2020-04-28 08:01:15 [scrapy.core.engine] INFO: Spider opened
2020-04-28 08:01:16 [scrapy.core.engine] DEBUG: Crawled (404) <GET https://www.worldometers.info/robots.txt> (referer: None)
2020-04-28 08:01:16 [protego] DEBUG: Rule at line 2 without any user agent to enforce it on.
2020-04-28 08:01:16 [protego] DEBUG: Rule at line 10 without any user agent to enforce it on.
2020-04-28 08:01:16 [protego] DEBUG: Rule at line 12 without any user agent to enforce it on.
2020-04-28 08:01:16 [protego] DEBUG: Rule at line 14 without any user agent to enforce it on.
2020-04-28 08:01:16 [protego] DEBUG: Rule at line 16 without any user agent to enforce it on.
2020-04-28 08:01:16 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://www.worldometers.info/world-population/population-by-country/> (referer: None)
```

HTTP error 404 (Not Found) for robots.txt means that this website doesn't provide this file so there are no restrictions on pages we can scrape.

We can also create request and pass it to `fetch()`:
```
>>> r = scrapy.Request(url="https://www.worldometers.info/world-population/population-by-country/")
>>> fetch(r)
2020-04-28 08:06:14 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://www.worldometers.info/world-population/population-by-country/> (referer: None)
```

To see the HTML from response:
```
>>> response.body
b'\n<!DOCTYPE html><!--[if IE 8]> <html lang="en" class="ie8">...
...
```

To see how spiders see web page:
```
>>> view(response)
True
>>> Opening in existing browser session.
```

This saves a web page in temp file and opens that file in a default browser.

Spiders see web pages without JavaScript. To see how they see them, we can disable JS on this temp html file in the browser:
* open Developer Tools (CTRL+SHIFT+I)
* open Control Panel (CTRL+SHIFT+P)
* disable JavaScript

Spiders can't render JavaScript.

To exit shell:
```
quit()
```


# References:

https://docs.scrapy.org/en/latest/topics/commands.html


