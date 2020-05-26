# -*- coding: utf-8 -*-
import scrapy
import logging


class CountriesSpider(scrapy.Spider):
    name = 'countries'

    # If domain has trailing slash, when following urls we'll get:
    # [scrapy.spidermiddlewares.offsite] DEBUG: Filtered offsite request to 'www.worldometers.info': <GET https://www.worldometers.info/world-population/china-population/>
    # so we need to make sure the values here do not have trailing '/'.
    allowed_domains = ['www.worldometers.info']

    start_urls = ['http://www.worldometers.info/world-population/population-by-country/']

    # Naive approach to pass the current state of the object to the callback at the moment when callback is scheduled.
    # Don't use it!
    country_name = ''

    def _parse_original(self, response):
        pass

    def _parse_v1(self, response):
        title = response.xpath("//h1/text()").get()
        countries = response.xpath("//td/a/text()").getall()

        print("type = ", type(response.xpath("//h1")))

        # Make sure yield is used when returning a list as if we used 'return', only first item would have been returned.
        yield {
            'title': title,
            'countries': countries
        }

    def _parse_v2(self, response):
        # xpath() returns <class 'scrapy.selector.unified.SelectorList'>
        # That's the list of selector objects and each object represents one selected (filtered) node.
        # Test:
        # Open Scrapy shell:
        #       scrapy shell http://www.worldometers.info/world-population/population-by-country/
        # >>> countries = response.xpath("//td/a")
        # >>> countries
        # [<Selector xpath='//td/a' data='<a href="/world-population/china-popu...'>,
        #  <Selector xpath='//td/a' data='<a href="/world-population/india-popu...'>,
        # ...]

        # When executing xpath against response object, we start query with '//' (root).
        countries = response.xpath("//td/a")

        # country is of type Selector and therefore we can execute XPath query against it
        for country in countries:
            # When executing xpath against Selector object, we start query with './/'
            # get() returns string (instead of Selector)
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()

            yield {
                'country_name': name,
                'country_link': link
            }

    # fetch() method used from shell can't be used inside the spider; we need to use request class
    def _parse_v3(self, response):
        countries = response.xpath("//td/a")

        for country in countries:
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()

            yield scrapy.Request(url=link)
            # this outputs:
            #   ValueError: Missing scheme in request url: /world-population/china-population/
            # This means Scrapy does not know whether to use http or https and domain as the url above is the relative url.

    def _parse_v4(self, response):
        countries = response.xpath("//td/a")

        for country in countries:
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()

            # python3 style formatting - f""
            absolute_url = f"https://www.worldometers.info{link}"
            yield scrapy.Request(url=absolute_url)
            # this outputs:
            #   [scrapy.spidermiddlewares.offsite] DEBUG: Filtered offsite request to 'www.worldometers.info': <GET https://www.worldometers.info/world-population/china-population/>
            #   [scrapy.core.engine] INFO: Closing spider (finished)
            # This happens as we have allowed_domains = ['www.worldometers.info/'] so need to remove trailing '/'.

    def _parse_v4(self, response):
        countries = response.xpath("//td/a")

        for country in countries:
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()

            # response object already contains domain information
            # If put mouse pointer on scrapy.Spider and press F12 we'll get
            # venv/lib/python3.6/site-packages/scrapy/spiders/__init__.py
            # If put mouse pointer on scrapy.http and press F12 we'll get
            # venv/lib/python3.6/site-packages/scrapy/http/__init__.py
            # If put mouse pointer on Response and press F12 we'll get
            # we venv/lib/python3.6/site-packages/scrapy/http/response/__init__.py
            # where we can see:
            # def urljoin(self, url):
            #     """Join this Response's url with a possible relative url to form an
            #     absolute interpretation of the latter."""
            #     return urljoin(self.url, url)
            absolute_url = response.urljoin(link)
            yield scrapy.Request(url=absolute_url)

    # We need to define where does response from country link requests go to.
    # This is a function which handles it.
    def _parse_country(self, response):
        print("_parse_country()")
        # this prints:
        #_parse_country()

        logging.info(response.url)
        # this prints e.g.:
        # 2020-05-24 15:22:43 [root] INFO: https://www.worldometers.info/world-population/malaysia-population/

        # rows is a collection of selectors on which we can call xpath (to get another selector)
        rows = response.xpath("(//table[@class=\"table table-striped table-bordered table-hover table-condensed table-list\"])[1]/tbody/tr")
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()
            yield {
                'name': self.country_name,
                'year': year,
                'population': population
            }

    # This callback is reading country name from Request's meta information.
    def _parse_country2(self, response):
        print("_parse_country()")
        logging.info(response.url)
        name = response.request.meta['country_name']

        # rows is a collection of selectors on which we can call xpath (to get another selector)
        rows = response.xpath("(//table[@class=\"table table-striped table-bordered table-hover table-condensed table-list\"])[1]/tbody/tr")
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()
            yield {
                'country_name': name,
                'year': year,
                'population': population
            }

    def _parse_v5(self, response):
        countries = response.xpath("//td/a")

        for country in countries:
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()

            absolute_url = response.urljoin(link)
            yield scrapy.Request(url=absolute_url, callback=self._parse_country)

    def _parse_v6(self, response):
        countries = response.xpath("//td/a")

        for country in countries:
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()

            yield response.follow(url=link, callback=self._parse_country)

    def _parse_v7(self, response):
        countries = response.xpath("//td/a")

        for country in countries:
            name = country.xpath(".//text()").get()

            # This approach will not work as by the time callbacks are called, self.country_name is already
            # set to the name of the last country in countries.
            self.country_name = name
            print("_parse_v7(): self.country_name =", self.country_name)

            link = country.xpath(".//@href").get()

            yield response.follow(url=link, callback=self._parse_country)

    def _parse_v8(self, response):
        countries = response.xpath("//td/a")

        for country in countries:
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()

            # To send or sync data between two parse methods we need to use "Requesst Meta".
            # Request Meta is a dictionary which we send alongside request.
            yield response.follow(url=link, callback=self._parse_country2, meta={'country_name': name})

    def parse(self, response):
        # self._parse_original(self, response)
        # self._parse_v1(self, response)
        # return self._parse_v3(response)
        # return self._parse_v4(response)
        # return self._parse_v5(response)
        # return self._parse_v6(response)
        # return self._parse_v7(response)
        return self._parse_v8(response)
