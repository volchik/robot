#!/usr/bin/env python
# coding: utf-8
from twisted.internet import protocol
from twisted.protocols.basic import LineReceiver
from robot import Robot
import logging

logger = logging.getLogger(__name__)


class RobotFactory(protocol.Factory):
    def __init__(self, device, dummy=False):
        self.dummy = dummy
        if not dummy:
            self.robot = Robot(device)
            logger.info(u'подключение к роботу выполнено')
        else:
            logger.info(u'сервер запущен в режиме заглушки. подключение к роботу не выполнено')

    def buildProtocol(self, addr):
        return RobotProtocol(self)

    def invoke_command(self, command):
        logger.info(u'отправлено роботу: "%s"' % command)
        if not self.dummy:
            result = self.robot.invoke(command)
        else:
            result = command
        logger.info(u'получено в ответ: "%s"' % result)
        return result


class RobotProtocol(LineReceiver):
    delimiter = b'\n'

    def __init__(self, factory):
        self.factory = factory

    def lineReceived(self, line):
        result = self.factory.invoke_command(line)
        self.transport.write(result + '\n')


