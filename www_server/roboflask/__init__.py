#!/usr/bin/env python
# coding: utf-8
from flask import Flask
import camera

app = Flask(__name__)
app.config['CAMREADER'] = camera.CamReader()
app.config['CAM_FPS'] = 0.2

import views


