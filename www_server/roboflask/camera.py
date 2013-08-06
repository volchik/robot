#!/usr/bin/env python
# coding: utf-8
import os
import glob
import itertools
from cv2 import cv


class DummyCamera(object):
    def __init__(self, *_):
        dummy_images = []
        for dummy in glob.glob(os.path.join(os.path.dirname(__file__), 'static', 'dummy', '*.JPG')):
            with open(dummy, 'rb') as f:
                dummy_images.append(f.read())
        self.dummy_images_iterator = itertools.cycle(dummy_images)

    def get_image(self):
        return self.dummy_images_iterator.next()


class Camera(object):
    def __init__(self, cam_num, width=640, height=480, fps=-1, quality=70):
        self.capture = cv.CaptureFromCAM(cam_num)
        self.width = width
        self.height = height
        self.fps = fps
        self.quality = quality

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        cv.SetCaptureProperty(self.capture, cv.CV_CAP_PROP_FRAME_WIDTH, value)
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        cv.SetCaptureProperty(self.capture, cv.CV_CAP_PROP_FRAME_HEIGHT, value)
        self._height = value

    @property
    def fps(self):
        return self._fps

    @fps.setter
    def fps(self, value):
        cv.SetCaptureProperty(self.capture, cv.CV_CAP_PROP_FPS, value)
        self._fps = value

    def get_image(self):
        img = cv.QueryFrame(self.capture)
        cv2mat = cv.EncodeImage(".jpeg", img, (cv.CV_IMWRITE_JPEG_QUALITY, self.quality))
        return cv2mat.tostring()


if __name__ == '__main__':
    pass