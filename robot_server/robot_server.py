#!/usr/bin/env python
# coding: utf-8
import os
import sys
import twisted.python.log
import logging
from robot_protocol import RobotFactory
from twisted.internet import reactor
import argparse
from daemon import Daemon
from config import Config

logger = logging.getLogger('main')


def configure_logging(config):
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    observer = twisted.python.log.PythonLoggingObserver()
    observer.start()
    formatter = logging.Formatter('%(asctime)-15s %(levelname)-7s %(name)-10s %(message)s')

    if config.log_to_stdout:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        root_logger.addHandler(stdout_handler)

    file_handler = logging.FileHandler(config.log_filename)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)


def start_server(config_file):
    config = Config(config_file)
    configure_logging(config)

    factory = RobotFactory(config.device)
    reactor.listenTCP(config.port, factory)
    logger.info("starting server...")
    reactor.callLater(0, logging.info, "ok")
    reactor.run()
    logger.info("server stopped")


class Server(Daemon):
    def __init__(self, _pid_filename):
        self.conf_filename = ""
        path = os.path.abspath(os.path.dirname(_pid_filename) + "/../log/stderr.log")
        super(Server, self).__init__(_pid_filename, '/dev/null', '/dev/null', path)

    def set_config(self, config_filename):
        self.conf_filename = config_filename

    def run(self):
        if self.conf_filename == "":
            return
        start_server(self.conf_filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help=u"файл конфигурации", default='robot_server.conf')
    parser.add_argument('-p', '--pid', help=u"pid файл")
    parser.add_argument('action', nargs='?', choices=['start', 'stop', 'restart'])

    args = parser.parse_args()
    config = args.config

    pid = args.pid or os.path.join(os.path.dirname(config), 'pid', os.path.basename(__file__) + '.pid')

    config_filename = os.path.abspath(config)
    pid_file = os.path.abspath(pid)

    serverobj = Server(pid_file)
    serverobj.set_config(config_filename)

    if args.action == 'start':
        serverobj.start()
    elif args.action == 'stop':
        serverobj.stop()
    elif args.action == 'restart':
        serverobj.restart()
    else:
        start_server(config_filename)
