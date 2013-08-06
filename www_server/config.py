#!/usr/bin/env python
# coding: utf-8
from configobj import ConfigObj
import logging
import os


class Config(object):
    def __init__(self, config_file):
        config = ConfigObj(config_file, unrepr=True)
        config_dir = os.path.abspath(os.path.dirname(config_file))

        self.log_level = logging.getLevelName(config.get('log_level', 'info').upper())
        self.log_file = os.path.join(config_dir, config.get('log_file', 'www_server.log'))
        self.pid_file = os.path.join(config_dir, config.get('pid_file', 'pid/www_server.pid'))
        self.log_to_stdout = config.get('log_to_stdout', False)
        self.port = config.get('port', 9091)
        self.log_dir = os.path.dirname(self.log_file)

    def create_dirs(self):
        for f in (self.log_file, self.pid_file):
            d = os.path.dirname(f)
            if not os.path.isdir(d):
                os.makedirs(d)





