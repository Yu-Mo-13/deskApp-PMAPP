# coding: UTF-8
import subprocess

class Subprocess:
    def __init__(self, command):
        self.command = command

    def run(self):
        subprocess.run(self.command)
