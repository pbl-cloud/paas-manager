import os

from .database_connector import DatabaseConnector
from .. import config
from werkzeug import secure_filename


class Jobs(DatabaseConnector):
    table = 'jobs'
    WAITING = 0
    RUNNING = 1
    FINISHED = 2

    def finish(self, stdout, stderr):
        self.update(stdout=stdout, stderr=stderr, status=Jobs.FINISHED)

    def file_full_path(self):
        if not hasattr(self, 'filename'):
            return None
        return os.path.join(self.upload_dir(), self.filename)

    def save_file(self, f):
        if not os.path.exists(self.upload_dir()):
            os.makedirs(self.upload_dir(), 0o755)
        f.save(self.file_full_path())

    def before_save(self):
        if hasattr(self, 'filename'):
            self.filename = secure_filename(self.filename)

    def human_status(self):
        if not hasattr(self, 'status'):
            return '不明'
        return {
            Jobs.WAITING: '待機中',
            Jobs.RUNNING: '実行中',
            Jobs.FINISHED: '完了'
        }[self.status]
