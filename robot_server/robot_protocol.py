#!/usr/bin/env python
# coding: utf-8
from twisted.internet import protocol
from twisted.protocols.basic import LineReceiver
from robot import Robot, USART_MODE

TIMEOUT = 1
ALIASES = {
    "move_forward": "MU",
    "move_backward": "MD",
    "move_left": "ML",
    "move_right": "MR",
    "cam_up": "CU",
    "cam_down": "CD",
    "cam_left": "CL",
    "cam_right": "CR",
    "W": "CU",
    "Z": "CD",
    "A": "CL",
    "S": "CR",
    "get_temperature": "TG",
    "get_pressure": "PG",
}


class RobotFactory(protocol.Factory):
    def __init__(self, device):
        self.robot = Robot(USART_MODE, device)

    def buildProtocol(self, addr):
        return RobotProtocol(self)

    def invoke_command(self, command):
        command = ALIASES.get(command, command)
        return self.robot.invoke(command)


class RobotProtocol(LineReceiver):
    def __init__(self, factory):
        self.factory = factory

    def lineReceived(self, line):
        result = self.factory.invole_command(line)
        self.transport.write(result+'\n')


