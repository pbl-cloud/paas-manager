import os

from .database_connector import DatabaseConnector
from .. import config
from werkzeug import secure_filename


class Jobs(DatabaseConnector):
    table = 'jobs'
    WAITING = 0
    RUNNING = 1
    FINISHED = 2
    FAILED = 3

    @classmethod
    def submit(cls, user_id, jar_file, args):
        job = cls.create(
            user_id=user_id,
            filename=jar_file.filename,
            arguments=args
        )
        job.save_file(jar_file)
        return job

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
            Jobs.FINISHED: '完了',
            Jobs.FAILED: '失敗'
        }[self.status]

    def arguments_list(self):
        if not hasattr(self, 'arguments') or self.arguments is None:
            return []
        return self.arguments.split(' ')
