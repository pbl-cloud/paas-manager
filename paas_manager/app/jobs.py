from .database_connector import DatabaseConnector


class Jobs(DatabaseConnector):
    table = 'jobs'
    WAITING = 0
    RUNNING = 1
    FINISHED = 2

    def update_output(self, jobid, stdout, stderr):
        self.cursor.execute('update ' + self.table + ' set stdout=%s, stderr=%s, status=%s where jobid=%s',
                            (stdout, stderr, self.FINISHED, jobid))
        self.connect.commit()

    def insert_job(self, userid, filename):
        self.cursor.execute('insert into ' + self.table + ' (userid,filename,status) values (%s,%s,0)', (userid, filename))
        self.connect.commit()
        return self.cursor.lastrowid

    def jobs_of_userid(self, userid):
        self.cursor.execute('select * from ' + self.table + ' where userid=%s', (userid,))
        rows = self.cursor.fetchall()
        return rows

    def delete_job(self, jobid):
        self.cursor.execute('delete from ' + self.table + ' where jobid=%s', (jobid,))
        self.connect.commit()

    def fetch_job(self, jobid):
        self.cursor.execute('select * from ' + self.table + ' where jobid=%s limit 1', (jobid,))
        return self.cursor.fetchone()

    def start_job(self, jobid):
        self.cursor.execute('update ' + self.table + ' set status=1 where jobid=%s', (jobid,))
