#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Alpha Olomi"
__version__ = "0.1.0"
__license__ = "Apache 2"

from logzero import logger


def main():
    """ Main entry point of the app """
    logger.info("hello world")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()