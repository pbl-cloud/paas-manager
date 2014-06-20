from kazoo.client import KazooClient
from kazoo.recipe.queue import LockingQueue
from . import config

class Manager:
    def __init__(self):
        super(Manager, self).__init__()
        self.config = config.get_config()
        self.zk = KazooClient(hosts=self.config['zookeeper']['hosts'])
        self.zk.start()
        transaction = self.zk.transaction()
        if not transaction.exists('/jobs'):
            transaction.create('/jobs')
        if not transaction.exists('/settings'):
            transaction.create('/settings')
        transaction.commit()

        self.lock = self.zk.lock('/settings/lock', 'lock')

    def enqueue_job(self, job):
        with lock:
            node = "/jobs/{0}".format(job.id)
            if not self.zk.exists(node):
                self.zk.create(node)
                self.zk.create(node + "/jar_path", job.jar_path)
                return True

            if not self.zk.exists('/settings/next_job'):
                self.zk.create('/settings/next_job', job.id)
        return False

