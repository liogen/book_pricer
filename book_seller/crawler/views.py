#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""View that start crawler for justbook.fr"""

import logging
from scrapyd_api import ScrapydAPI
from datetime import timedelta
from django.views import View
from django.conf import settings
from django.utils import timezone
from django.shortcuts import render
from django.http import JsonResponse
from crawler.form import BookForm
from crawler.models import Book, Offer

LOGGER = logging.getLogger(settings.LOGGER_NAME)
SITE_NAME = 'BookSeller'
SITE_DESCRIPTION = 'The easiest way to know the correct price of an used book'


class CrawlerView(View):

    form_class = BookForm
    initial = {'SITE_NAME': SITE_NAME, 'SITE_DESCRIPTION': SITE_DESCRIPTION}
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        books = Book.objects.filter(title__isnull=False).order_by("-id")
        self.initial['form'] = form
        self.initial['books'] = books[:8]
        self.initial['books_length'] = len(books)
        self.initial['books_limit'] = 8
        return render(request, self.template_name, self.initial)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        json_response = {}
        isbn = "error"

        if form.is_valid():
            isbn = form.cleaned_data["isbn"]
            book = None
            start_crawler = False
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
                    json_response['book_title'] = book.title
                    json_response['cover_image'] = book.cover_image
                    json_response['editor'] = book.editor
                    json_response['distribution_date'] = book.distribution_date
            else:
                start_crawler = True

            if start_crawler is True:
                scrapyd = ScrapydAPI('http://localhost:6800')
                scrapyd.schedule('justbookcrawler', 'justbook', isbn=isbn)

        json_response['isbn'] = isbn
        json_response['crawler_started'] = start_crawler

        return JsonResponse(json_response)


class ISBNInfoView(View):

    def get(self, request, *args, **kwargs):
        isbn = kwargs['isbn']
        book = None
        json_response = {}
        crawler_started = True
        try:
            book = Book.objects.get(isbn=isbn)
        except Book.DoesNotExist:
            pass

        if book is not None and book.title is not None:
            if book.updated_at > timezone.now() + timedelta(days=-2):
                json_response['book_title'] = book.title
                json_response['cover_image'] = book.cover_image
                json_response['editor'] = book.editor
                json_response['distribution_date'] = book.distribution_date
                crawler_started = False

        json_response['crawler_started'] = crawler_started
        json_response['isbn'] = isbn

        return JsonResponse(json_response)
