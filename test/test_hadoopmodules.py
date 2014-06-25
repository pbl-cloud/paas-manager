import unittest
from os import path
from paas_manager.app.hadoop_modules import HadoopModules


class Test_HadoopModules(unittest.TestCase):
    hadoopModules = HadoopModules()
    mock_path = path.join(
        path.dirname(path.realpath(__file__)), "mock_exec_hadoop.sh")

    command = [mock_path]
    kwargs = {'run_command': command, 'copy_command': command}

    def test_start_hadoop(self):
        jar_path = "path"
        args = []

        def callback(out, err):
            self.assertEqual(out, "fin\n")
            self.assertEqual(err, "err\n")

        t = self.hadoopModules.start_hadoop(jar_path, args, callback, **self.kwargs)

        t.join()

    def test_exec_hadoop(self):

        def callback(out, err):
            self.assertEqual(out, "fin\n")
            self.assertEqual(err, "err\n")

        self.hadoopModules.exec_hadoop(self.command, callback)

    def test_duplicate_threads(self):
        def callback(out, err):
            self.assertEqual(out, "fin\n")
            self.assertEqual(err, "err\n")
        command = [self.mock_path]

        t = self.hadoopModules.start_hadoop("", [], callback, **self.kwargs)
        try:
            self.hadoopModules.start_hadoop("", [], callback, **self.kwargs)
        except Exception as e:
            self.assertEqual(
                e.args[0], "Duplicate threads: please wait until the end of the existing thread.")

        t.join()
        t = self.hadoopModules.start_hadoop("", [], callback, **self.kwargs)
        t.join()

if __name__ == '__main__':
    unittest.main()
