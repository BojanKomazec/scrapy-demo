# -*- coding: utf-8 -*-
import scrapy


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info/']
    start_urls = ['http://www.worldometers.info/world-population/population-by-country/']

    def _parse_original(self, response):
        pass

    def _parse_v1(self, response):
        title = response.xpath("//h1/text()").get()
        countries = response.xpath("//td/a/text()").getall()

        print("type = ", type(response.xpath("//h1")))

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

    def parse(self, response):
        # self._parse_original(self, response)
        # self._parse_v1(self, response)
        return self._parse_v2(response)
