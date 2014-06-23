from .database_connector import DatabaseConnector


class Jobs(DatabaseConnector):
    WAITING = 0
    RUNNING = 1
    FINISHED = 2

    def update_output(self, jobid, stdout, stderr):
        self.cursor.execute('update jobs set stdout=%s, stderr=%s, status=%s where jobid=%s',
                            (stdout, stderr, self.FINISHED, jobid))
        self.connect.commit()

    def insert_job(self, userid, filename):
        self.cursor.execute('insert into jobs (userid,filename,status) values (%s,%s,0)', (userid, filename))
        self.connect.commit()
        return self.cursor.lastrowid

    def jobs_of_userid(self, userid):
        self.cursor.execute('select * from jobs where userid=%s', (userid,))
        rows = self.cursor.fetchall()
        return rows

    def delete_job(self, jobid):
        self.cursor.execute('delete from jobs where jobid=%s', (jobid,))
        self.connect.commit()

    def status_of(self, jobid):
        self.cursor.execute('select status from jobs where jobid=%s limit 1', (jobid,))
        rows = self.cursor.fetchone()
        return rows[0]

    def fetch_job(self, jobid):
        self.cursor.execute('select * from jobs where jobid=%s limit 1', (jobid,))
        return self.cursor.fetchone()

    def start_job(self, jobid):
        self.cursor.execute('update jobs set status=1 where jobid=%s', (jobid,))
