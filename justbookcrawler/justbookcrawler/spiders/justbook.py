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
        url = 'https://www.justbooks.fr/search/?author=&title=&lang=fr&' \
              'new_used=*&destination=fr&currency=EUR&binding=*&isbn=%s&' \
              'keywords=&minprice=&maxprice=&min_year=&max_year=&' \
              'mode=advanced&st=sr&ac=qr' % isbn
        yield scrapy.Request(url, self.parse)

    def book_does_not_exist(self):
        current_book = Book.objects.get(isbn=getattr(self, 'isbn', None))
        current_book.not_found = True
        current_book.save()

    def book_exist(self, book_temp):

        current_book = Book.objects.get(isbn=getattr(self, 'isbn', None))
        current_book.title = book_temp['title']
        current_book.cover_image = book_temp['cover']
        current_book.editor = book_temp['editor']
        current_book.distribution_date = book_temp['distribution']
        current_book.not_found = False
        current_book.save()

        return current_book

    def book_information_parsing(self, response):

        book_temp = {
            'title': '',
            'cover': '',
            'editor': '',
            'distribution': ''
        }
        tables = response.css("table.results-table-Logo")
        if not tables:
            return book_temp, tables, False

        try:
            book_temp['title'] = response.css(
                '#bd-isbn div.attributes div')[1].css(
                'a strong span ::text').extract_first()
        except IndexError:
            return book_temp, tables, False

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

        return book_temp, tables, True

    def offer_creation(self, current_book, table_type, offer_temp):
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

    def offer_info_css(self, tds, first_index, second_index, selector):
        return tds[first_index].css('span')[second_index].css(
            selector).extract_first()

    def offer_crawl(self, current_book, table_type, offer_temp, tds):
        if len(tds[1].css('.results-explanatory-text-Logo')) == 3:
            offer_temp['vendor'] = self.offer_info_css(tds, 1, 0, '::text')
            offer_temp['country'] = self.offer_info_css(tds, 1, 2, '::text')
            offer_temp['shop_img'] = self.offer_info_css(
                tds, 1, 1, 'a img ::attr(src)')
            offer_temp['shop_link'] = self.offer_info_css(
                tds, 1, 1, 'a ::attr(href)')
        offer_temp['description'] = "<br />".join(tds[2].css(
            '::text').extract())
        offer_temp['price'] = float(tds[3].css(
            'a ::text').extract_first().replace("€", "").replace(",", "."))
        self.offer_creation(current_book, table_type, offer_temp)

    def parse(self, response):

        book_temp, tables, book_exist = self.book_information_parsing(response)

        if book_exist:
            current_book = self.book_exist(book_temp)
        else:
            self.book_does_not_exist()
            return

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
                    self.offer_crawl(current_book, table_type, offer_temp, tds)

            table_type = "1"
