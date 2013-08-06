#!/usr/bin/env python
# coding: utf-8
from __future__ import division
from flask import render_template, Response, current_app, request, stream_with_context, abort
from roboflask import app
import time
import logging

logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/mjpeg')
def mjpeg():
    def jpeg_generator(camreader, fps):
        delay = 1 / fps
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

    # todo куда-нибудь вынести fps
    fps = 0.2
    return Response(stream_with_context(jpeg_generator(current_app.camreader, fps)),
                    content_type='multipart/x-mixed-replace; boundary=--aaboundary')


@app.route('/jpeg')
def jpeg():
    return Response(current_app.camreader.get_image(), 200, content_type='image/jpeg')


@app.route('/invoke/<command>', methods=['POST', 'GET'])
def invoke(command):
    method = getattr(current_app.robot, command, None)
    if callable(method):
        logger.info('requested command %s(%s)' % (command, ', '.join(['='.join(i) for i in request.args.items()])))
        result = method(**request.args)
        if result:
            return result
        else:
            return '%s - OK!' % command
    else:
        abort(404)


@app.route('/main')
def main():
    return render_template('main.html')
