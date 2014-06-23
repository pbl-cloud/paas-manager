import unittest
from paas_manager.app.jobs import Jobs


class TestJobs(unittest.TestCase):
    jobs = Jobs()
    jobid = None
    jobs.table = 'test_jobs'

    def setUp(self):
        self.jobid = self.jobs.insert_job(1, 'test.jar')

    def tearDown(self):
        self.jobs.delete_job(self.jobid)

    def test_update_output(self):
        self.jobs.update_output(self.jobid, 'stdout', 'stderr')
        row = self.jobs.fetch_job(self.jobid)
        self.assertEqual(row[4], 'stdout')
        self.assertEqual(row[5], 'stderr')

    def test_status_finished(self):
        self.jobs.update_output(self.jobid, 'stdout', 'stderr')
        self.assertEqual(self.jobs.fetch_job(self.jobid)[3], self.jobs.FINISHED)

    def test_start_job(self):
        self.assertEqual(self.jobs.fetch_job(self.jobid)[3], self.jobs.WAITING)
        self.jobs.start_job(self.jobid)
        self.assertEqual(self.jobs.fetch_job(self.jobid)[3], self.jobs.RUNNING)

if __name__ == '__main__':
    unittest.main()
