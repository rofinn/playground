# -*- coding: utf-8 -*-
from pathlib import Path

"""Top-level package for playground."""

__author__ = """Rory Finnegan"""
__email__ = 'rory.finnegan@gmail.com'
__version__ = '0.0.1'

"""
FS structure

    # playground.initialize()
    # mkdir bin + playground.<lang>.initialize()
    ~/.playground/
        /bin/
        julia/
            tmp/
            src/
            bin/    # symlink -> ../bin
            share/  # playgrounds
        python/
            bin/    # symlink -> ../bin
            share/  # playgrounds
        R/
            bin/    # symlink -> ../bin
            share/


    # Environment == playground.<lang>.Environment

"""

class Config(object):
    def __init__(self, path=None):
        self.path = Path.home() if path is None else path

    @property
    def path(self):
        return self.path

    @property
    def bin(self):
        return self.path.joinpath('bin')

    def initialize(self):
        for p in (self.path, self.bin):
            if not os.path.exists(p):
                os.makedirs(p)