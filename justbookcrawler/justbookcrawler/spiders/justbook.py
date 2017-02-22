#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Crawler for justbook.fr"""

import scrapy
from scrapy_djangoitem import DjangoItem
from crawler.models import Book, Offer


class OfferItem(DjangoItem):
    django_model = Offer


class BlogSpider(scrapy.Spider):
    name = 'justbook'

    def start_requests(self):
        isbn = getattr(self, 'isbn', None)
        url = 'http://www.justbooks.fr/search/?author=&title=&lang=fr&new_used=*&destination=fr&currency=EUR&' \
              'binding=*&isbn=%s&keywords=&minprice=&maxprice=&min_year=&max_year=&mode=advanced&' \
              'st=sr&ac=qr&ps=bp' % isbn
        yield scrapy.Request(url, self.parse)

    def parse(self, response):

        tables = response.css("table.results-table-Logo")
        book_title = response.css('#bd-isbn div.attributes div')[1].css('a strong span ::text').extract_first()
        book_cover = response.css('img#coverImage ::attr(src)').extract_first()
        book_editor = response.css('span.describe-isbn ::text').extract_first().split(",")[0]
        book_distribution = response.css('span.describe-isbn ::text').extract_first().split(",")[1].replace(" ", "")
        self.logger.info('book_title: %s', book_title)
        # self.logger.info('book_cover: %s', book_cover)
        # self.logger.info('book_editor: %s', book_editor)
        # self.logger.info('book_distribution: %s', book_distribution)
        current_book = Book.objects.get(isbn=getattr(self, 'isbn', None))
        current_book.title = book_title
        current_book.cover_image = book_cover
        current_book.editor = book_editor
        current_book.distribution_date = book_distribution
        current_book.save()
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
                    # self.logger.info(tds[1])
                    if len(tds[1].css('.results-explanatory-text-Logo')) == 3:
                        vendor = tds[1].css('span')[0].css('::text').extract_first()
                        country = tds[1].css('span')[2].css('::text').extract_first()
                        shop_img = tds[1].css('span')[1].css('a img ::attr(src)').extract_first()
                        shop_link = tds[1].css('span')[1].css('a ::attr(href)').extract_first()
                    description = "<br />".join(tds[2].css('::text').extract())
                    price = float(tds[3].css('a ::text').extract_first().replace("€", ""))
                    offer = OfferItem()
                    offer['book'] = current_book
                    offer['book_condition'] = table_type
                    offer['vendor'] = vendor
                    offer['shop_img'] = shop_img
                    offer['shop_link'] = shop_link
                    offer['country'] = country
                    offer['description'] = description
                    offer['price'] = price
                    offer.save()

                    # yield offer

            table_type = "used"
