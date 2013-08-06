#!/usr/bin/env python
# coding: utf-8
import logging

from flask import Flask
import camera
from roboflask import robot_client
logger = logging.getLogger(__name__)
app = Flask(__name__)

import views


def prepare_app(config):
    global app
    assert not hasattr(app, 'camera')
    assert not hasattr(app, 'robot_client')
    if config.dummy_cam:
        logger.info('using dummy camera')
        app.camera = camera.DummyCamera()
    else:
        logger.info('using real camera')
        app.camera = camera.Camera(config.cam_num)
    app.camera.fps = config.cam_fps
    app.robot = robot_client.RobotClient(config.robot_host, config.robot_port)
    return app

