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
        self.user = Users.create({'email': 'test@test', 'password': 'test'})
        self.job = Jobs.create({'user_id': self.user.id, 'filename': 'test.jar'})

    def tearDown(self):
        Jobs.remove_all()
        Users.remove_all()

    def test_find(self):
        job = Jobs.find(self.job.id)
        self.assertEqual('test.jar', job.filename)

    def test_user_jobs(self):
        jobs = Jobs.query({'user_id': self.user.id})
        self.assertEqual(1, len(jobs))
        self.assertEqual('test.jar', jobs[0].filename)

    def test_update_output(self):
        self.jobs.update_output(self.job.id, 'stdout', 'stderr')
        row = self.jobs.fetch_job(self.job.id)
        self.assertEqual(row[4], 'stdout')
        self.assertEqual(row[5], 'stderr')

    def test_status_finished(self):
        self.jobs.update_output(self.job.id, 'stdout', 'stderr')
        self.assertEqual(
            self.jobs.fetch_job(self.job.id)[3], self.jobs.FINISHED)

    def test_start_job(self):
        self.assertEqual(self.jobs.fetch_job(self.job.id)[3], self.jobs.WAITING)
        self.jobs.start_job(self.job.id)
        self.assertEqual(self.jobs.fetch_job(self.job.id)[3], self.jobs.RUNNING)

    def test_remove(self):
        count = Jobs.count()
        j = Jobs.create({'user_id': self.user.id, 'filename': 'foobar'})
        self.assertEqual(count + 1, Jobs.count())
        j.remove()
        self.assertEqual(count, Jobs.count())

if __name__ == '__main__':
    unittest.main()
