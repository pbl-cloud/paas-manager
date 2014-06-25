import threading
import subprocess
import os
from datetime import datetime

from .. import config

THREAD_ERR_MSG = "Duplicate threads: please wait " + \
    "until the end of the existing thread."


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class HadoopModules(metaclass=Singleton):
    hostname = "{login_user}@{host}".format(**config['hadoop'])
    config = config['hadoop']

    def __init__(self):
        self.t = None

    # command is for testing or debugging
    def start_hadoop(self, path, args, callback, **kwargs):
        if self.t is not None and self.t.is_alive():
            raise Exception(THREAD_ERR_MSG)

        output_path = self._get_output_path(path)
        run_command = kwargs.get('run_command', self._get_run_command(output_path, args))
        copy_command = kwargs.get('copy_command', self._get_copy_command(path, output_path))

        self.t = threading.Thread(
            target=self.run_hadoop,
            args=(copy_command, run_command, callback),
            daemon=True
        )
        self.t.start()
        return self.t

    def run_hadoop(self, copy_command, run_command, callback):
        p = subprocess.Popen(
            copy_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        self.exec_hadoop(run_command, callback)

    def exec_hadoop(self, command, callback):
        p = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        callback(bytes.decode(out), bytes.decode(err))

    def _get_output_path(self, path):
        prefix = datetime.now().isoformat().replace(':', '-').replace('.', '')
        output_file = prefix + "-" + os.path.basename(path)
        return os.path.join(self.config['tmp_dir'], output_file)

    def _get_copy_command(self, input_path, output_path):
        return [
            "scp", input_path,
            self.hostname + ":" + output_path
        ]

    def _get_run_command(self, path, args):
        command = [
            "ssh", self.hostname,
            "HADOOP_USER_NAME={0}".format(self.config['hadoop_user']),
            self.config['command'], "jar", path
        ]
        command.extend(args)
        return command
