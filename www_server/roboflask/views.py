#!/usr/bin/env python
# coding: utf-8
from __future__ import division
from flask import render_template, Response, current_app, abort, stream_with_context
from roboflask import app
import time


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/mjpeg')
def mjpeg():
    def jpeg_generator(camreader, fps):
        delay = 1/fps
        last_time = time.time()
        while True:
            image = camreader.get_image()

            yield "--aaboundary\r\n"
            yield "Content-Type: image/jpeg\r\n"
            yield "Content-length: " + str(len(image)) + "\r\n\r\n"
            yield image
            yield "\r\n\r\n\r\n"

            current_time = time.time()
            wait = delay - (current_time - last_time)
            if wait > 0:
                time.sleep(wait)
            last_time = time.time()

    camreader = current_app.config.get('CAMREADER')
    fps = current_app.config.get('CAM_FPS', 1)
    if camreader:
        return Response(stream_with_context(jpeg_generator(camreader, fps)),
                        content_type='multipart/x-mixed-replace; boundary=--aaboundary')
    abort(500, 'no camreader')


@app.route('/jpeg')
def jpeg():
    camreader = current_app.config.get('CAMREADER')
    if camreader:
        return Response(camreader.get_image(), 200, content_type='image/jpeg')
    abort(500, 'no camreader')


@app.route('/temperature')
def temperature():
    pass

