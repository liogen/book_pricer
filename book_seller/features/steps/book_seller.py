#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Functionnal test for book_seller"""

import json
import logging
from behave import when, then  # pylint: disable=E0611
from django.test import Client
from crawler.models import Book


LOGGER = logging.getLogger("book_seller")
KEY_ISBN = 'isbn'
KEY_TITLE = 'title'
KEY_EDITOR = 'editor'
KEY_CRAWLER_STARTED = 'crawler_started'
KEY_DISTRIBUTION_DATE = 'distribution_date'
BOOK_TITLE = "Economix : la première histoire de l'économie en BD (2e édition)"
BOOK_INFO = {
    KEY_ISBN: '978-2-35204-384-3',
    KEY_TITLE: BOOK_TITLE,
    KEY_EDITOR: 'Les Arènes',
    KEY_DISTRIBUTION_DATE: '2014'
}


@when("I ask for an ISBN book to crawl")
def run_backup_command(context):
    """Run backup command"""
    # pylint: disable=unused-argument
    client = Client()
    response = client.post('/', {'isbn': BOOK_INFO[KEY_ISBN]})
    LOGGER.error(response.content)
    assert response.status_code == 200
    body = json.loads(response.content.decode('utf-8'))
    LOGGER.error(body)
    assert body[KEY_ISBN] == BOOK_INFO[KEY_ISBN]
    assert body[KEY_CRAWLER_STARTED] is True


@then("I should see the book in DB")
def no_data_expected(context):
    """No data expected"""
    # pylint: disable=unused-argument
    Book.objects.get(isbn=BOOK_INFO[KEY_ISBN])
