#!/usr/bin/env python
# coding: utf-8
import argparse
import functools
import logging
import os
import sys
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
from daemon import Daemon
from config import Config
import roboflask
from twisted.internet import reactor


logger = logging.getLogger('main')


def configure_logging(config):
    root_logger = logging.getLogger()
    root_logger.setLevel(config.log_level)
    formatter = logging.Formatter('%(asctime)-15s %(levelname)-7s %(name)-10s %(message)s')
    if config.log_to_stdout:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        root_logger.addHandler(stdout_handler)
    file_handler = logging.FileHandler(config.log_file)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)


def start_server(config):
    configure_logging(config)
    app = roboflask.prepare_app(config)

    resource = WSGIResource(reactor,
                            reactor.getThreadPool(),
                            app)
    factory = Site(resource)
    endpoint = TCP4ServerEndpoint(reactor, config.port)
    d = endpoint.listen(factory)
    logger.info(u"starting sq_server...")
    d.addCallback(lambda _: logger.info(u'порт открыт'))
    d.addErrback(lambda failure: (logger.error(u'ошибка открытия порта: %s' % failure.getErrorMessage()) or
                                  logger.error(u'stopping reactor') or
                                  reactor.callLater(0, reactor.stop)))

    reactor.run()


class Server(Daemon):
    def __init__(self, target, pidfile, stdout='/dev/null', stderr='/dev/null'):
        self.target = target
        super(Server, self).__init__(pidfile, '/dev/null', stdout, stderr)

    def set_config(self, config_filename):
        self.conf_filename = config_filename

    def run(self):
        self.target()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help=u"файл конфигурации",  default='www_server.conf')
    parser.add_argument('action', nargs='?', choices=['start', 'stop', 'restart'])
    args = parser.parse_args()

    config = Config(args.config)
    config.create_dirs()
    pid = config.pid_file
    stdout = os.path.join(config.log_dir, 'stdout.log')
    stderr = os.path.join(config.log_dir, 'stderr.log')

    target = functools.partial(start_server, config)

    server = Server(target, pid, stdout, stderr)

    if args.action == 'start':
        server.start()
    elif args.action == 'stop':
        server.stop()
    elif args.action == 'restart':
        server.restart()
    else:
        target()
