import unittest

# FIXME: use proper environment setup
from paas_manager import config
config['mysql']['database'] += '_test'
from paas_manager.app.models.jobs import Jobs
from paas_manager.app.models.users import Users


class TestJobs(unittest.TestCase):
    jobs = Jobs()
    users = Users()
    jobid = None

    def setUp(self):
        self.users.register_user('test@test', 'test')
        id = self.users.user_id('test@test')
        self.jobid = self.jobs.insert_job(id, 'test.jar')

    def tearDown(self):
        self.jobs.cursor.execute('truncate ' + self.jobs.table)
        self.jobs.connect.commit()
        self.users.delete_user('test@test')

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
