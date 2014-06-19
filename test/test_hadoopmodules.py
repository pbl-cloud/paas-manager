import unittest
from paas_manager.hadoop_modules import HadoopModules


class Test_HadoopModules(unittest.TestCase):
    hadoopModules = HadoopModules()
    mock_path = "test/mock_exec_hadoop.sh"

    def test_start_hadoop(self):
        jar_path = "path"
        args = []

        command = ["ssh", "localhost", "test/paas-manager/" + self.mock_path]

        def callback(out, err):
            self.assertEqual(out, "fin\n")
            self.assertEqual(err, "err\n")

        t = self.hadoopModules.start_hadoop(jar_path, args, callback, command)

        t.join()

    def test_exec_hadoop(self):

        def callback(out, err):
            self.assertEqual(out, "fin\n")
            self.assertEqual(err, "err\n")

        command = [self.mock_path]
        self.hadoopModules.exec_hadoop(command, callback)

    def test_duplicate_threads(self):
        def callback(out, err):
            self.assertEqual(out, "fin\n")
            self.assertEqual(err, "err\n")
        command = ["ssh", "localhost", "test/paas-manager/" + self.mock_path]

        t = self.hadoopModules.start_hadoop("", [], callback, command)
        try:
            self.hadoopModules.start_hadoop("", [], callback, command)
        except Exception as e:
            self.assertEqual(e.args[0], "Duplicate threads: please wait until the end of the existing thread.")

        t.join()

if __name__ == '__main__':
    unittest.main()
