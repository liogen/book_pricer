#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""View that start crawler for justbook.fr"""

import math
import logging
import statistics
from scrapyd_api import ScrapydAPI
from datetime import timedelta
from django.views import View
from django.conf import settings
from django.utils import timezone
from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from crawler.models import Book, Offer

LOGGER = logging.getLogger(settings.LOGGER_NAME)
SITE_NAME = 'BookPricer'
SITE_DESCRIPTION = 'The easiest way to know the correct price of an used book'


def get_chart_distribution(new_offers, used_offers):
    prices_info = {
        'max_price': 0,
        'interval_size': 5,
        'new_prices_array': [],
        'used_prices_array': [],
        'total_prices_array': [],
        'offer_mean': 0,
        'offer_stdev': 0
    }

    for condition in [new_offers, used_offers]:
        for offer in condition:
            prices_info['total_prices_array'].append(offer.price)

    try:
        prices_info['offer_mean'] = statistics.mean(
            prices_info['total_prices_array'])
        prices_info['offer_stdev'] = statistics.stdev(
            prices_info['total_prices_array'])
    except statistics.StatisticsError:
        prices_info['offer_mean'] = 0
        prices_info['offer_stdev'] = 0

    lower_bound = prices_info['offer_mean'] - 2 * prices_info[
        'offer_stdev']
    upper_bound = prices_info['offer_mean'] + 2 * prices_info[
        'offer_stdev']
    for offer in new_offers:
        if lower_bound < offer.price < upper_bound:
            prices_info['new_prices_array'].append(offer.price)
            if offer.price > prices_info['max_price']:
                prices_info['max_price'] = offer.price

    for offer in used_offers:
        if lower_bound < offer.price < upper_bound:
            prices_info['used_prices_array'].append(offer.price)
            if offer.price > prices_info['max_price']:
                prices_info['max_price'] = offer.price

    max_price_rounded = math.ceil(prices_info['max_price'] / 10) * 10
    interval_number = int(max_price_rounded / prices_info['interval_size']) + 1

    new_offers_array = [0] * interval_number
    used_offers_array = [0] * interval_number

    for offer in prices_info['new_prices_array']:
        new_offers_array[int(offer / prices_info['interval_size'])] += 1

    for offer in prices_info['used_prices_array']:
        used_offers_array[int(offer / prices_info['interval_size'])] += 1

    array_chart_offers = [["Price", "New offers", "Used offers"]]

    for i in range(len(new_offers_array)):
        column_name = "%s-%s€" % (
            i * prices_info['interval_size'],
            (i + 1) * prices_info['interval_size'])
        array_chart_offers.append([column_name, new_offers_array[i],
                                   used_offers_array[i]])

    try:
        new_mean = statistics.mean(prices_info['used_prices_array'])
    except statistics.StatisticsError:
        new_mean = 0

    return array_chart_offers, new_mean


def get_book_information(book, json_response):
    new_offers = Offer.objects.filter(
        book=book, book_condition=Offer.NEW).order_by('price')
    used_offers = Offer.objects.filter(
        book=book, book_condition=Offer.USED).order_by('price')
    total_offer_nb = len(new_offers) + len(used_offers)
    json_response['lowest_new_price'] = None
    json_response['lowest_used_price'] = None
    json_response['book_title'] = book.title
    json_response['cover_image'] = book.cover_image
    json_response['editor'] = book.editor
    json_response['distribution_date'] = book.distribution_date
    json_response['new_offers'] = serializers.serialize(
        'json',
        new_offers,
        fields=('book', 'book_condition', 'vendor', 'country', 'description',
                'price', 'shop_img', 'shop_link', ))
    json_response['used_offers'] = serializers.serialize(
        'json',
        used_offers,
        fields=('book', 'book_condition', 'vendor', 'country', 'description',
                'price', 'shop_img', 'shop_link', ))
    json_response['total_offer_nb'] = total_offer_nb
    chart_offers, median_offers = get_chart_distribution(new_offers,
                                                         used_offers)
    json_response['chart_offers'] = chart_offers
    json_response['median_offers'] = "%.2f" % median_offers
    if new_offers:
        json_response['lowest_new_price'] = new_offers[0].price
    if used_offers:
        json_response['lowest_used_price'] = used_offers[0].price

    return json_response


class CrawlerView(View):

    initial = {'SITE_NAME': SITE_NAME, 'SITE_DESCRIPTION': SITE_DESCRIPTION}
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):  # noqa
        books = Book.objects.filter(title__isnull=False).order_by("-id")
        self.initial['books'] = books[:8]
        self.initial['books_length'] = len(books)
        self.initial['books_limit'] = 8
        return render(request, self.template_name, self.initial)

    def post(self, request, *args, **kwargs):  # noqa
        json_response = {}
        isbn = request.POST.get('isbn', 'error')
        LOGGER.info('request.POST: {0}'.format(request.POST))
        LOGGER.info('isbn: {0}'.format(isbn))
        start_crawler = False

        if isbn not in ['error']:
            book = None
            try:
                book = Book.objects.get(isbn=isbn)
            except Book.DoesNotExist:
                Book.objects.create(isbn=isbn)

            if book is not None and book.title is not None:
                if book.updated_at <= timezone.now() + timedelta(days=-2):
                    for offer in Offer.objects.filter(book__isbn=isbn):
                        offer.delete()
                    start_crawler = True
                else:
                    json_response = get_book_information(book, json_response)
            else:
                start_crawler = True

            if start_crawler is True:
                scrapyd = ScrapydAPI('http://localhost:6800')
                scrapyd.schedule('justbookcrawler', 'justbook', isbn=isbn)

        json_response['isbn'] = isbn
        json_response['crawler_started'] = start_crawler

        return JsonResponse(json_response)


class ISBNInfoView(View):

    def get(self, request, *args, **kwargs):  # noqa
        isbn = kwargs['isbn']
        json_response = {}
        crawler_started = True
        error_404 = JsonResponse({
            "isbn": isbn,
            "status_code": 404,
            "error": "The resource was not found"}, status=404)
        try:
            book = Book.objects.get(isbn=isbn)
        except Book.DoesNotExist:
            return error_404

        if book.not_found is True:
            return error_404

        if book is not None and book.title is not None:
            if book.updated_at > timezone.now() + timedelta(days=-2):
                json_response = get_book_information(book, json_response)
                crawler_started = False

        json_response['crawler_started'] = crawler_started
        json_response['isbn'] = isbn

        return JsonResponse(json_response)
