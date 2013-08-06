#!/usr/bin/env python
# coding: utf-8
from flask import Flask
import camera
from roboflask import robot_client

app = Flask(__name__)

import views


def prepare_app(config):
    global app
    assert not hasattr(app, 'camreader')
    assert not hasattr(app, 'robot_client')
    app.camreader = camera.CamReader()
    app.robot = robot_client.RobotClient(config.robot_host, config.robot_port)
    return app

