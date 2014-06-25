from kazoo.client import KazooClient
from kazoo.recipe.queue import LockingQueue
import threading
import logging as log

from .. import config
from ..app.hadoop_modules import HadoopModules
from ..app.models import Jobs


class Manager:
    def __init__(self):
        super(Manager, self).__init__()

        self._terminated = False

        self.config = config['zookeeper']
        self.zk = KazooClient(**self.config)
        self.zk.start()

        self.zk.ensure_path('/jobs')
        self.zk.ensure_path('/settings/running')
        self.zk.set('/settings/running', 'false'.encode())

        self.hadoop = HadoopModules()

        self.lock = self.zk.Lock('/settings/lock', 'lock')

        self._start_polling()

    def _start_polling(self):
        t = threading.Thread(
            target=self._try_execute_job,
            daemon=True
        )
        t.start()

    def _try_execute_job(self):
        if not self._terminated:
            threading.Timer(5.0, self._try_execute_job).start()
            self.execute_next_job()

    def enqueue_job(self, job):
        if job.id is None:
            return
        success = False
        with self.lock:
            node = "/jobs/{0}".format(job.id)
            if not self.zk.exists(node):
                self.zk.create(node)
                self.zk.create(node + "/jar_path", job.file_full_path().encode())
                self.zk.create(node + "/retries", '0'.encode())
                success = True
                log.info("Enqueued job {0}".format(job.id))
        return success

    def execute_next_job(self):
        with self.lock:
            if self._is_running():
                return
            children = self.zk.get_children('/jobs')
            if not children:
                return
            children = map(lambda s: int(s), children)
            next_job_id = min(children)
            if self._check_retries(next_job_id):
                return self.execute_job(next_job_id, False)
            else:
                Jobs.update_entity(next_job_id, status=Jobs.FAILED)
                self._delete_job(next_job_id)
                log.info("Removing job {0} after 3 failures".format(next_job_id))
        self.execute_next_job()

    def _delete_job(self, id):
        self.zk.delete("/jobs/{0}".format(id), recursive=True)

    def _check_retries(self, id):
        retries, _ = self.zk.get("/jobs/{0}/retries".format(id))
        return int(retries.decode()) < 3

    def execute_job(self, id, take_lock=True):
        if take_lock:
            with self.lock:
                self.execute_job_no_lock(id)
        else:
            self.execute_job_no_lock(id)

    def hadoop_callback(self, job_id, return_code, stdout, stderr):
        job = Jobs.find(job_id)
        if job:
            job.update(stdout=stdout, stderr=stderr)
        with self.lock:
            self._set_running(False)
            if return_code == 0:
                job.update(status=Jobs.FINISHED)
                self._delete_job(job_id)

    def execute_job_no_lock(self, id):
        log.info("Executing job {0}".format(id))
        self._set_running(True)
        self._increase_retries(id)
        job = Jobs.find(id)
        job.update_entity(id, status=Jobs.RUNNING)
        path, _ = self.zk.get("/jobs/{0}/jar_path".format(id))
        callback = lambda ret, out, err: self.hadoop_callback(id, ret, out, err)
        self.hadoop.start_hadoop(path.decode(), job.arguments_list(), callback)

    def _set_running(self, is_running):
        value = ('true' if is_running else 'false').encode()
        self.zk.set('/settings/running', value)

    def _is_running(self):
        v, _ = self.zk.get('/settings/running')
        return v.decode() == 'true'

    def _increase_retries(self, id):
        key = "/jobs/{0}/retries".format(id)
        retries, _ = self.zk.get(key)
        new_retries = int(retries.decode()) + 1
        Jobs.update_entity(id, retries=new_retries)
        self.zk.set(key, str(new_retries).encode())
