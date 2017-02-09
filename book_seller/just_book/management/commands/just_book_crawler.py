#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Crawler for justbook.fr"""

import logging
from django.conf import settings
from django.core.management.base import BaseCommand

MAIN_HELP_TEXT = "Invoke rsync method to copy data on a specific folder"
COMMAND_NAME = "justbook crawler command"
COMMAND_START_TEXT = "Command %s started"
COMMAND_STOP_TEXT = "Command %s stopped"


class Command(BaseCommand):
    """Command class
    """

    help = MAIN_HELP_TEXT
    name = COMMAND_NAME
    logger = logging.getLogger(settings.LOGGER_NAME)

    def handle(self, *args, **options):
        """Main django command method
        """
        self.logger.info(COMMAND_START_TEXT, self.name)
        print(12)
        self.logger.info(COMMAND_STOP_TEXT, self.name)
