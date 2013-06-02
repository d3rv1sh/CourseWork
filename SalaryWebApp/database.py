import pymysql

class AppData:
    #Params
    server   = {'host': '127.0.0.1',
                'port': 3306 }
    user     = {'username': 'cwork',
                'password': '7HgMoGl7N6FDyP9mIbCp' }
    database = 'cwork'

    def __enter__(self):
        self.connection = pymysql.connect( host   = self.server['host'],
                                           port   = self.server['port'],
                                           user   = self.user['username'],
                                           passwd = self.user['password'],
                                           db     = self.database )
        self.cursor = self.connection.cursor()
        #print('Entered')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.close()
        #print('Cleared')

    def execute(self, sql):
        self.cursor.execute(sql)
        return self.cursor

    def reset(self):
        self.cursor.close()
        self.cursor = self.connection.cursor()
