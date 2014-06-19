import unittest
from paas_manager.hadoop_modules import HadoopModules


class Test_hadoop_modules(unittest.TestCase):
    hadoopModules = HadoopModules()
    def test_start_hadoop(self):
        jar_path = "path"
        args = []

        def callback(out, err):
            print("stdout: " + out)
            print("stderr: " + err)

        t = self.hadoopModules.start_hadoop(jar_path, args, callback)

        t.join()

    def test_exec_hadoop(self):
        mock_path = "test/mock_exec_hadoop.sh"

        def callback(out, err):
            self.assertEqual(out, "fin\n")
            self.assertEqual(err, "err\n")

        command = [mock_path]
        self.hadoopModules.exec_hadoop(command, callback)

if __name__ == '__main__':
    unittest.main()
