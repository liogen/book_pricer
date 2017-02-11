#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Crawler for justbook.fr"""

import scrapy
from scrapy_djangoitem import DjangoItem
from crawler.models import Book


class BookItem(DjangoItem):
    django_model = Book


class BlogSpider(scrapy.Spider):
    name = 'justbook'

    def start_requests(self):
        isbn = getattr(self, 'isbn', None)
        url = 'http://www.justbooks.fr/search/?author=&title=&lang=fr&new_used=*&destination=fr&currency=EUR&' \
              'binding=*&isbn=%s&keywords=&minprice=&maxprice=&min_year=&max_year=&mode=advanced&' \
              'st=sr&ac=qr&ps=bp' % isbn
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        prices = response.css('span.results-price a')
        for price in prices:
            yield {'price': price.css('::text').extract_first()}

        tables = response.css("table.results-table-Logo")
        table_type = "0"
        if len(tables) == 1:
            table_type = "1"
        for table in tables:
            for tr in table.css('tr'):
                tds = tr.css("td")
                vendor = ""
                shop_img = ""
                shop_link = ""
                country = ""
                if len(tds) == 4:
                    self.logger.info(tds[1])
                    if len(tds[1].css('.results-explanatory-text-Logo')) == 3:
                        vendor = tds[1].css('span')[0].css('::text').extract_first()
                        country = tds[1].css('span')[2].css('::text').extract_first()
                        shop_img = tds[1].css('span')[1].css('a img ::attr(src)').extract_first()
                        shop_link = tds[1].css('span')[1].css('a ::attr(href)').extract_first()
                    description = "<br />".join(tds[2].css('::text').extract())
                    price = tds[3].css('a ::text').extract_first()
                    book = BookItem()
                    book['isbn'] = getattr(self, 'isbn', None)
                    book['book_type'] = table_type
                    book['vendor'] = vendor
                    book['shop_img'] = shop_img
                    book['shop_link'] = shop_link
                    book['country'] = country
                    book['description'] = description
                    book['price'] = price
                    book.save()

                    yield book

            table_type = "used"
