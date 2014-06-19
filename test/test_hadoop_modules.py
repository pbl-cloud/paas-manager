import unittest
from paas_manager.hadoop_modules import start_hadoop, exec_hadoop


class MyTestCase(unittest.TestCase):
    def test_start_hadoop(self):
        start_hadoop()
        self.assertEqual(True, False)

    def test_exec_hadoop(self):
        mock_path = "test/mock_exec_hadoop.sh"

        def callback(self, out, err):
            self.assertEqual(out, "fin\n")
            self.assertEqual(err, "err\n")

        command = [mock_path]
        exec_hadoop(command, callback)

if __name__ == '__main__':
    unittest.main()
