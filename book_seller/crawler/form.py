#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Form that collect ISBN"""

from django import forms


class BookForm(forms.Form):

    isbn = forms.CharField(label='ISBN', max_length=100)