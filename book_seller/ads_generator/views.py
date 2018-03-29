#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""View that display ads according to spreadsheet configuration"""

# import io
import csv
import urllib.request
import logging
from django.views import View
from django.conf import settings
from django.shortcuts import render

LOGGER = logging.getLogger(settings.LOGGER_NAME)


def data_population(datareader):
    first_row = True
    data = {
        "books": []
    }

    for row in datareader:
        if first_row:
            data["title"] = row[0]
            data["intro"] = row[1]
            data["prices"] = {}
            data["prices"]["actual_price"] = row[2]
            data["prices"]["selling_price"] = row[3]
            data["prices"]["reduction_price"] = row[4]
            data["prices"]["reduction_percentage"] = row[5]
        else:
            data["books"].append({
                "title": row[0],
                "status": row[1],
                "actual_price": row[2],
                "pictures": row[4],
                "description": row[3]
            })
        first_row = False


def get_ads_information():
    csv_url = 'https://docs.google.com/spreadsheets/d/1sqAJ-RDP_-K1jgsbhroYXs'\
              '65nQSPhoRvXhadCO7dB4o/pub?gid=1989620233&single=true&output=csv'

    webpage = urllib.request.urlopen(csv_url)
    datareader = csv.reader(webpage.read().decode('utf-8').splitlines())

    return data_population(datareader)


class AdsGeneratorView(View):

    template_name = 'ads_generator.html'

    def get(self, request, *args, **kwargs):  # noqa
        data = get_ads_information()
        return render(request, self.template_name, data)
