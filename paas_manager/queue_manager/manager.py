from kazoo.client import KazooClient
from kazoo.recipe.queue import LockingQueue
from .. import config
from ..hadoop_modules import HadoopModules


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

        self.hadoop = HadoopModules()

        self.lock = self.zk.lock('/settings/lock', 'lock')

    def enqueue_job(self, job):
        with lock:
            node = "/jobs/{0}".format(job.id)
            if not self.zk.exists(node):
                self.zk.create(node)
                self.zk.create(node + "/jar_path", job.jar_path.encode())
                return True
        return False

    def execute_next_job(self):
        with lock:
            children = self.zk.get_children('/jobs')
            if not children:
                return
            children = map(lambda s: int(s.decode()), children)
            next_job_id = min(children)
            self.execute_job(next_job_id, False)

    def execute_job(self, id, take_lock=True):
        if take_lock:
            with lock:
                self.execute_job_no_lock(id)
        else:
            self.execute_job_no_lock(id)

    def hadoop_callback(self):
        self.execute_next_job()

    def execute_job_no_lock(self, id):
        path, _ = self.zk.get("/jobs/{0}/jar_path".format(id))
        self.hadoop.start_hadoop(path.decode(), [], self.hadoop_callback)
