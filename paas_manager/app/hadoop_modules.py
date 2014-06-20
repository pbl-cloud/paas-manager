import threading
import subprocess


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class HadoopModules(metaclass=Singleton):
    t = None
    hostname = "star@192.168.122.10"

    def __init__(self):
        pass

    def start_hadoop(self, path, args, callback, command=None):  # command is for testing or debugging
        if command is None:
            command = ["ssh", self.hostname, "hadoop", "jar", path]
        command.extend(args)

        if self.t is not None and self.t.is_alive():
            raise Exception("Duplicate threads: please wait until the end of the existing thread.")

        self.t = threading.Thread(target=self.exec_hadoop, args=(command, callback), daemon=True)
        self.t.start()
        return self.t

    @staticmethod
    def exec_hadoop(command, callback):
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()

        callback(bytes.decode(out), bytes.decode(err))
