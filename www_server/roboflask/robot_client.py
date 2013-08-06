#!/usr/bin/env python
#coding: utf-8
# todo прикрутить реконнект

from socket import socket, AF_INET, SOCK_STREAM
TIMEOUT = 5


class RobotClient(object):
    def __init__(self, host, port, timeout=TIMEOUT):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.settimeout(timeout)
        self.socket.connect((host, port))
        self.fileobj = self.socket.makefile()

    def invoke(self, command, check=True):
        self.fileobj.write(command + '\n')
        self.fileobj.flush()
        result = self.fileobj.readline().strip()
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

