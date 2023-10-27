from psycopg2 import pool


class ConnectionPool(object):
    def __init__(self, **kwargs):
        self.pool_size = kwargs.pop('POOL_SIZE', 5)
        self.conn_pool = None
        super(ConnectionPool, self).__init__(**kwargs)

    def ensure_connection_pool(self):
        if self.conn_pool is None:
            self.conn_pool = pool.SimpleConnectionPool(
                1,
                self.pool_size,
                database=self.settings_dict['NAME'],
                user=self.settings_dict['USER'],
                password=self.settings_dict['PASSWORD'],
                host=self.settings_dict['HOST'],
                port=self.settings_dict['PORT']
            )

    def _close(self):
        if self.connection is not None:
            self.conn_pool.putconn(self.connection)
            self.connection = None

    def _cursor(self, *args, **kwargs):
        self.ensure_connection_pool()
        if self.connection is None:
            self.connection = self.conn_pool.getconn()
        return super(ConnectionPool, self)._cursor(*args, **kwargs)
