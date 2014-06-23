from .database_connector import DatabaseConnector


class Jobs(DatabaseConnector):
    WAITING = 0
    RUNNING = 1
    FINISHED = 2

    def update_output(self, jobid, stdout, stderr):
        self.cursor.execute('update jobs set stdout=%s, stderr=%s, status=2 where jobid=%s',
                            (stdout, stderr, str(jobid)))
        self.connect.commit()

    def insert_job(self, userid, filename):
        self.cursor.execute('insert into jobs (userid,filename) values (%s,%s)', (str(userid), filename))
        self.connect.commit()
        return self.cursor.lastrowid

    def jobs_of_userid(self, userid):
        self.cursor.execute('select * from jobs where userid=%s', (str(userid),))
        rows = self.cursor.fetchall()
        return rows

    def delete_job(self, jobid):
        self.cursor.execute('delete from jobs where jobid=%s', (str(jobid),))
        self.connect.commit()

    def status_of(self, jobid):
        self.cursor.execute('select status from jobs where jobid=%s', (str(jobid),))
        rows = self.cursor.fetchall()
        return rows[0][0]

    def fetch_job(self, jobid):
        self.cursor.execute('select * from jobs where jobid=%s limit 1', (str(jobid),))
        return self.cursor.fetchone()

    def start_job(self, jobid):
        self.cursor.execute('update jobs set status=1 where jobid=%s', (str(jobid),))
