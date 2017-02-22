#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Form that collect ISBN"""

from django import forms


class BookForm(forms.Form):

    isbn = forms.CharField(label='ISBN', max_length=100,
                           widget=forms.TextInput(attrs={'placeholder': 'Enter your ISBN. Ex: 978-2-84933-377-8',
                                                         'class': 'form-control wow fadeIn',
                                                         'data-wow-delay': '1.0s',
                                                         'id': 'isbn-value'}))