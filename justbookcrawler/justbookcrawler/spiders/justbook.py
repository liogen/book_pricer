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
        url = 'http://www.justbooks.fr/search/?author=&title=&lang=fr&' \
              'new_used=*&destination=fr&currency=EUR&binding=*&isbn=%s&' \
              'keywords=&minprice=&maxprice=&min_year=&max_year=&' \
              'mode=advanced&st=sr&ac=qr&ps=bp' % isbn
        yield scrapy.Request(url, self.parse)

    def parse(self, response):

        current_book = Book.objects.get(isbn=getattr(self, 'isbn', None))
        book_temp = {
            'title': '',
            'cover': '',
            'editor': '',
            'distribution': ''
        }

        tables = response.css("table.results-table-Logo")
        if not tables:
            current_book.not_found = True
            current_book.save()
            return

        try:
            book_temp['title'] = response.css(
                '#bd-isbn div.attributes div')[1].css(
                'a strong span ::text').extract_first()
        except IndexError:
            current_book.not_found = True
            current_book.save()
            return

        book_temp['cover'] = response.css(
            'img#coverImage ::attr(src)').extract_first()
        book_temp['editor'] = response.css(
            'span.describe-isbn ::text').extract_first().split(",")[0]
        book_temp['distribution'] = response.css(
            'span.describe-isbn ::text').extract_first().split(",")[1].replace(
            " ", "")
        # self.logger.info('book_title: %s', book_title)
        # self.logger.info('book_cover: %s', book_cover)
        # self.logger.info('book_editor: %s', book_editor)
        # self.logger.info('book_distribution: %s', book_distribution)
        current_book.title = book_temp['title']
        current_book.cover_image = book_temp['cover']
        current_book.editor = book_temp['editor']
        current_book.distribution_date = book_temp['distribution']
        current_book.not_found = False
        current_book.save()
        table_type = "0"
        if len(tables) == 1:
            table_type = "1"
        for table in tables:
            for tr in table.css('tr'):
                tds = tr.css("td")
                offer_temp = {
                    'vendor': '',
                    'shop_img':  '',
                    'shop_link':  '',
                    'country': '',
                    'description': '',
                    'price': ''
                }
                if len(tds) == 4:
                    # self.logger.info(tds[1])
                    if len(tds[1].css('.results-explanatory-text-Logo')) == 3:
                        offer_temp['vendor'] = tds[1].css('span')[0].css(
                            '::text').extract_first()
                        offer_temp['country'] = tds[1].css('span')[2].css(
                            '::text').extract_first()
                        offer_temp['shop_img'] = tds[1].css('span')[1].css(
                            'a img ::attr(src)').extract_first()
                        offer_temp['shop_link'] = tds[1].css('span')[1].css(
                            'a ::attr(href)').extract_first()
                    offer_temp['description'] = "<br />".join(tds[2].css(
                        '::text').extract())
                    offer_temp['price'] = float(tds[3].css(
                        'a ::text').extract_first().replace("€", ""))
                    offer = OfferItem()
                    offer['book'] = current_book
                    offer['book_condition'] = table_type
                    offer['vendor'] = offer_temp['vendor']
                    offer['shop_img'] = offer_temp['shop_img']
                    offer['shop_link'] = offer_temp['shop_link']
                    offer['country'] = offer_temp['country']
                    offer['description'] = offer_temp['description']
                    offer['price'] = offer_temp['price']
                    offer.save()

                    # yield offer

            table_type = "1"
