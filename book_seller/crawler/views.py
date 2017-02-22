#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""View that start crawler for justbook.fr"""

from scrapyd_api import ScrapydAPI
from django.views import View
from django.shortcuts import render
from crawler.form import BookForm
from crawler.models import Book, Offer


SITE_NAME = 'BookSeller'
SITE_DESCRIPTION = 'The easiest way to know the correct price of an used book'

class CrawlerView(View):

    form_class = BookForm
    initial = {'SITE_NAME': SITE_NAME, 'SITE_DESCRIPTION': SITE_DESCRIPTION}
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        books = Book.objects.all().order_by("-id")
        self.initial['form'] = form
        self.initial['books'] = books[:8]
        self.initial['books_length'] = len(books)
        self.initial['books_limit'] = 8
        return render(request, self.template_name, self.initial)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        isbn = "error"

        if form.is_valid():
            isbn = form.cleaned_data["isbn"]

            for offer in Offer.objects.filter(book__isbn=isbn):
                offer.delete()
            for book in Book.objects.filter(isbn=isbn):
                book.delete()

            try:
                Book.objects.get(isbn=isbn)
            except Book.DoesNotExist:
                Book.objects.create(isbn=isbn)

            scrapyd = ScrapydAPI('http://localhost:6800')
            scrapyd.schedule('justbookcrawler', 'justbook', isbn=isbn)

        self.initial['form'] = form
        self.initial['isbn'] = isbn

        return render(request, self.template_name, self.initial)
