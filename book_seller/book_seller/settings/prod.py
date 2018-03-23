#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""local.py"""

from book_seller.settings.base import *  # noqa

#####
# Book_seller configuration
#
DEBUG = True

INSTALLED_APPS += [  # noqa
#     'django_nose',
#     'behave_django',
#     'stubs',
#     'livereload',
]

MIDDLEWARE += [  # noqa
    # 'livereload.middleware.LiveReloadScript',
]


ALLOWED_HOSTS += ["192.168.0.253", "127.0.0.1"]  # noqa

#####
# Logging configuration
#
LOG_BASE_FOLDER = "/tmp"
LOGGING['handlers']['file']['filename'] = '%s/%s.log' % (LOG_BASE_FOLDER, LOGGER_NAME)  # noqa
LOGGING['loggers'][LOGGER_NAME]['level'] = 'DEBUG'  # noqa

#####
# Scrapy configuration
#

SCRAPY_URL = 'http://localhost:6800'
