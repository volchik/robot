#!/usr/bin/env python
# coding: utf-8
import os
import glob
import itertools


class DummyCamReader(object):
    def __init__(self, *params, **configuration):
        dummy_images = []
        for dummy in glob.glob(os.path.join(os.path.dirname(__file__), 'static', 'dummy', '*.JPG')):
            with open(dummy, 'r') as f:
                dummy_images.append(f.read())
        self.dummy_images_iterator = itertools.cycle(dummy_images)

    def configure(self, **params):
        pass  # todo: написать сюда что-то полезное

    def get_image(self):
        return self.dummy_images_iterator.next()

#todo: впилить сюда чтение картинок с камеры
CamReader = DummyCamReader


if __name__ == '__main__':
    pass