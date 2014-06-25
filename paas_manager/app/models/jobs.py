from .database_connector import DatabaseConnector


class Jobs(DatabaseConnector):
    table = 'jobs'
    WAITING = 0
    RUNNING = 1
    FINISHED = 2

    def finish(self, stdout, stderr):
        self.update(stdout=stdout, stderr=stderr, status=Jobs.FINISHED)
