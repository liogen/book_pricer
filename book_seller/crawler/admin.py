#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""File that define Admin fields"""

from django.contrib import admin
from crawler import models


class BookAdmin(admin.ModelAdmin):
    """SiteAdmin class
    """
    list_display = ('isbn', 'vendor', 'country', 'price')
    list_filter = ('isbn', 'vendor', 'country', 'price')
    search_fields = ('isbn', 'vendor', 'country', 'price')


admin.site.register(models.Book, BookAdmin)
