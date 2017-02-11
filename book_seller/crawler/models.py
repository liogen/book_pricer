#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""File that define Timevortex model"""

from django.db import models


APP_NAME = "crawler"


class Book(models.Model):
    """Variables model.
    """
    NEW = '0'
    USED = '1'
    BOOK_TYPE = (
        (NEW, 'Neuf'),
        (USED, 'Occassion'),
    )

    book_type = models.CharField(
        max_length=2,
        choices=BOOK_TYPE,
        null=True,
        blank=True
    )
    isbn = models.CharField(max_length=20)
    vendor = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.CharField(max_length=10, null=True, blank=True)
    shop_img = models.URLField(max_length=200, null=True, blank=True)
    shop_link = models.URLField(max_length=200, null=True, blank=True)

    class Meta:
        app_label = APP_NAME

    def __str__(self):
        return self.isbn