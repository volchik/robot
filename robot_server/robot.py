# coding: utf-8
import logging
from threading import RLock
import time

import serial

logger = logging.getLogger(__name__)


class Robot(object):
    def __init__(self, device):
        logger.info(u'открытие порта %s...' % device)
        self.lock = RLock()
        try:
            self.port = serial.Serial(device, 9600, timeout=0.1)
            logger.info(u'порт открыт')
        except Exception as e:
            logger.error(u'ошибка: %s' % e.message)
        time.sleep(1)  # todo: сделать по нормальному

    def invoke(self, data):
        with self.lock():
            self.port.write(data + '\r')
            result = self.port.readline().replace('\n', '').replace('\r', '')
            logger.info(u'обработка посылки "%s" -> "%s"' % (data, result))
            return result

    def close(self):
        logger.info(u'порт закрыт')
        self.port.close()

