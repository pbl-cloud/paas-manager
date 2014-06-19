import unittest
from paas_manager.hadoop_modules import start_hadoop, exec_hadoop


class MyTestCase(unittest.TestCase):
    def callback(out, err):
        print(out)
        print(err)

    def test_start_hadoop(self):
        start_hadoop()
        self.assertEqual(True, False)

    def test_exec_hadoop(self):
        command = ["dir"]
        exec_hadoop(command, self.callback)

if __name__ == '__main__':
    unittest.main()
