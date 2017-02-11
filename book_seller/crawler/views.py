#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""View that start crawler for justbook.fr"""

from scrapyd_api import ScrapydAPI
from django.views import View
from django.shortcuts import render
from crawler.form import BookForm
from crawler.models import Book


class CrawlerView(View):

    form_class = BookForm
    initial = {'key': 'value'}
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        isbn = "error"

        if form.is_valid():
            isbn = form.cleaned_data["isbn"]
            for book in Book.objects.filter(isbn=isbn):
                book.delete()

            scrapyd = ScrapydAPI('http://localhost:6800')
            scrapyd.schedule('justbookcrawler', 'justbook', isbn=isbn)

        return render(request, self.template_name, {'form': form, 'isbn': isbn})
