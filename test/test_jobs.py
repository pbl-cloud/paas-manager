import unittest
import os

os.environ['PAAS_MANAGER_ENV'] = 'test'

from paas_manager.app.models.jobs import Jobs
from paas_manager.app.models.users import Users


class TestJobs(unittest.TestCase):
    jobs = Jobs()
    users = Users()
    jobid = None

    def setUp(self):
        self.users.register_user('test@test', 'test')
        self.id = self.users.user_id('test@test')
        self.jobid = self.jobs.insert_job(self.id, 'test.jar')

    def tearDown(self):
        Jobs.remove_all()
        Users.remove_all()

    def test_user_jobs(self):
        jobs = Jobs.find({'user_id': self.id})
        self.assertEqual(1, len(jobs))
        self.assertEqual('test.jar', jobs[0].filename)

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
