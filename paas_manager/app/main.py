import os
from flask import Flask, render_template, request, redirect, url_for, session
from .gmail import *
from .hadoop_modules import HadoopModules


class Item:

    def __init__(item, name, filename, status):
        item.name = name
        item.filename = filename
        item.status = status


class QueueManager:

    def __init__(self, jar_path, args):
        self.hadoop_modules = HadoopModules()
        self.jar_path = jar_path
        self.args = args
        self.result = ''
        self.resulterr = ''

    def piyo(self):

        def callback(stdout, stderr):
            self.result = stdout
            self.resulterr = stderr

        t = self.hm.start_hadoop(self.jar_path, self.args, callback)
