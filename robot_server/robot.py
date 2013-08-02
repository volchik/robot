# coding: utf-8
import logging
from threading import RLock
from I2C import I2C
import serial
import time

I2C_MODE = 1
USART_MODE = 2

logger = logging.getLogger(__name__)


class I2CTransport(object):
    def __init__(self, address):
        self.i2c = I2C(address)
        self.address = address
        self.lock = RLock()

    def send(self, data):
        with self.lock:
            self.busy = True
            for char in data:
                self.i2c.write_byte(ord(char))
            self.i2c.write_byte(13)
        return data

    def close(self):
        pass


class USARTTransport(object):
    def __init__(self, port):
        self.port = serial.Serial(port, 9600, timeout=0.1)
        time.sleep(1)  # todo: сделать по нормальному
        self.lock = RLock()

    def send(self, data):
        with self.lock():
            self.port.write(data + '\r')
            result = self.port.readline()
            return result.replace('\n', '').replace('\r', '')

    def close(self):
        self.port.close()


class Robot(object):
    def __init__(self, mode, address):
        self.mode = mode
        if self.mode == I2C_MODE:
            self.transport = I2CTransport(address)
        elif self.mode == USART_MODE:
            self.transport = USARTTransport(address)

    def invoke(self, command):
        return self.transport.send(command)
