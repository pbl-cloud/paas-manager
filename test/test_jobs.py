import unittest
import os

os.environ['PAAS_MANAGER_ENV'] = 'test'

from paas_manager.app.models.jobs import Jobs
from paas_manager.app.models.users import Users


class TestJobs(unittest.TestCase):
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

    def test_finish_job(self):
        self.job.update({'stdout': 'stdout', 'stderr': 'stderr'})
        self.assertEqual(self.job.stdout, 'stdout')
        self.assertEqual(self.job.stderr, 'stderr')

    def test_start_job(self):
        self.job.update_one('status', Jobs.RUNNING)
        self.assertEqual(Jobs.RUNNING, self.job.status)

    def test_status_finished(self):
        self.job.finish('stdout', 'stderr')
        self.assertEqual(self.job.status, Jobs.FINISHED)

    def test_remove(self):
        count = Jobs.count()
        j = Jobs.create({'user_id': self.user.id, 'filename': 'foobar'})
        self.assertEqual(count + 1, Jobs.count())
        j.remove()
        self.assertEqual(count, Jobs.count())

if __name__ == '__main__':
    unittest.main()
