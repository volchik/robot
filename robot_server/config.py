#!/usr/bin/env python
# coding: utf-8
import os
from configobj import ConfigObj


class Config(object):
    def __init__(self, filename):
        config = ConfigObj(filename, unrepr=True)
        self.__dict__.update(config)
        config_dir = os.path.abspath(os.path.dirname(filename))
        log_relative = config.get('log_filename', 'robot_server.log')
        log_absolute = os.path.join(config_dir, log_relative)
        self.log_filename = log_absolute
        self.dummy = config.get('dummy', False)

