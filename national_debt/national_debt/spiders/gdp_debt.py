# -*- coding: utf-8 -*-
import scrapy


class GdpDebtSpider(scrapy.Spider):
    name = 'gdp_debt'
    allowed_domains = ['worldpopulationreview.com/countries/countries-by-national-debt']
    start_urls = ['http://worldpopulationreview.com/countries/countries-by-national-debt/']

    def parse(self, response):
        country_rows = response.xpath("//tbody/tr")
        for country_row in country_rows:
            country_name = country_row.xpath(".//a/text()").get()
            ratio = country_row.xpath("((.//td)[2])/text()").get()
            yield {
                'country_name': country_name,
                'ratio': ratio
            }
