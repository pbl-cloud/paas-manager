from .database_connector import DatabaseConnector


class Jobs(DatabaseConnector):
    table = 'jobs'
    WAITING = 0
    RUNNING = 1
    FINISHED = 2

    def update_output(self, job_id, stdout, stderr):
        self.cursor.execute('update ' + self.table + ' set stdout=%s, stderr=%s, status=%s where id=%s',
                            (stdout, stderr, self.FINISHED, job_id))
        self.connect.commit()

    def insert_job(self, user_id, filename):
        self.cursor.execute('insert into ' + self.table +
                            ' (user_id,filename,status) values (%s,%s,0)', (user_id, filename))
        self.connect.commit()
        return self.cursor.lastrowid

    def jobs_of_userid(self, user_id):
        self.cursor.execute(
            'select * from ' + self.table + ' where user_id=%s', (user_id,))
        rows = self.cursor.fetchall()
        return rows

    def delete_job(self, job_id):
        self.cursor.execute(
            'delete from ' + self.table + ' where id=%s', (job_id,))
        self.connect.commit()

    def fetch_job(self, job_id):
        self.cursor.execute(
            'select * from ' + self.table + ' where id=%s limit 1', (job_id,))
        return self.cursor.fetchone()

    def start_job(self, job_id):
        self.cursor.execute(
            'update ' + self.table + ' set status=1 where id=%s', (job_id,))
