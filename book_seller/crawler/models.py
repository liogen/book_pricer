#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""File that define Timevortex model"""

from django.db import models


APP_NAME = "crawler"


class Book(models.Model):
    """Book model.
    """
    isbn = models.SlugField(max_length=20, unique=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    cover_image = models.URLField(max_length=200, null=True, blank=True)
    editor = models.CharField(max_length=200, null=True, blank=True)
    distribution_date = models.CharField(max_length=4, null=True, blank=True)
    not_found = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = APP_NAME

    def __str__(self):
        return self.isbn


class Offer(models.Model):
    """Offer model.
    """
    NEW = '0'
    USED = '1'
    BOOK_CONDITION = (
        (NEW, 'Neuf'),
        (USED, 'Occassion'),
    )

    book = models.ForeignKey(Book)
    book_condition = models.CharField(max_length=2, choices=BOOK_CONDITION, null=True,blank=True)
    vendor = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    shop_img = models.URLField(max_length=200, null=True, blank=True)
    shop_link = models.URLField(max_length=200, null=True, blank=True)

    class Meta:
        app_label = APP_NAME

    def __str__(self):
        return self.book.isbn
