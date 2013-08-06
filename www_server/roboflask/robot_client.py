#!/usr/bin/env python
#coding: utf-8
# todo: допилить реконнект
import logging
from socket import socket, AF_INET, SOCK_STREAM

logger = logging.getLogger(__name__)
TIMEOUT = 5


class RobotClient(object):
    delimiter = b'\n'

    def __init__(self, host, port, timeout=TIMEOUT):
        self.reconnect = True
        self.timeout = timeout
        self.host = host
        self.port = port
        self.buffer = ''
        self._connect()

    def _connect(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.settimeout(self.timeout)
        self.socket.connect((self.host, self.port))

    def _send(self, data):
        self.socket.send(data + self.delimiter)

    def _recv(self):
        while True:
            data = self.socket.recv(4096)
            logger.debug('получены данные %r' % data)
            if not data:
                logger.info('connection closed')
                return
            self.buffer += data

            if self.delimiter in self.buffer:
                result, rest = self.buffer.split(self.delimiter, 1)
                self.buffer = rest
                return result

    def invoke(self, command, check=True):
        logger.info(u"отправка комманды %s" % command)
        self._send(command)
        logger.info(u"ожидание ответа...")
        result = self._recv()
        logger.info(u"ответ получен: %s" % result)
        if check and result != command:
            raise RuntimeError(result)
        return result

    def move_forward(self):
        self.invoke('MU')

    def move_backward(self):
        self.invoke('MD')

    def move_left(self):
        self.invoke('ML')

    def move_right(self):
        self.invoke('MR')

    def cam_up(self):
        self.invoke('CU')

    def cam_down(self):
        self.invoke('CD')

    def cam_left(self):
        self.invoke('CL')

    def cam_right(self):
        self.invoke('CR')

    def get_temperature(self):
        # todo написать проверку возвращаемых значений
        return self.invoke('TG', False)[2:] or 'dummy_temp'

    def get_pressure(self):
        # todo написать проверку возвращаемых значений
        return self.invoke('PG', False)[2:] or 'dummy_pressure'


if __name__ == '__main__':
    client = RobotClient('localhost', 9090)
    client.move_forward()
    client.move_backward()
    client.invoke('hello, robot!')

