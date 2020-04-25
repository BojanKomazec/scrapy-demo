# scrapy-demo
Scrapy framework demo project

# How to install Scrapy

Scrapy should be installed in virtual environment in order not to mess up globally installed packages:

```
$ virtualenv --python=python3.6 venv
$ source venv/bin/activate
(venv) $ pip install scrapy
```

# How to run a benchmark?

```
$ scrapy bench
```

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

