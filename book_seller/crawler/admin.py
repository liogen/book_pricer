#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""File that define Admin fields"""

from django.contrib import admin
from crawler import models


class BookAdmin(admin.ModelAdmin):
    """BookAdmin class
    """
    list_display = ('isbn', 'title', 'editor', 'distribution_date',
                    'created_at', 'updated_at')
    list_filter = ('isbn', 'title',)
    search_fields = ('isbn', 'title',)


class OfferAdmin(admin.ModelAdmin):
    """OfferAdmin class
    """
    list_display = ('book', 'vendor', 'country', 'price')
    list_filter = ('book', 'vendor', 'country', 'price')
    search_fields = ('book__isbn', 'book__title', 'vendor', 'country', 'price')


admin.site.register(models.Book, BookAdmin)
admin.site.register(models.Offer, OfferAdmin)
