import logging
import momoko
from tornado import gen
from tornado.ioloop import IOLoop
from psycopg2.extras import RealDictCursor


class DB:
    """ Base DB class """
    def __init__(self, config, db_logging=True):
        self.db = None
        self.dsn = "dbname={dbname} user={user} password={password} host={host} port={port}".format(**config)
        self.db_logging = db_logging

    def connect(self):
        try:
            self.db = momoko.Pool(
                dsn=self.dsn,
                max_size=1,
                cursor_factory=RealDictCursor,
                raise_connect_errors=True
            )
            io = IOLoop().current()
            io.run_sync(self.db.connect)
        except Exception as e:
            logging.exception("DB %s connection error %s" % (self.__class__.__name__, str(e)))
            return

    @gen.coroutine
    def _execute(self, sql, args):
        try:
            yield self.db.execute(sql, args)
        except Exception as e:
            logging.error('DB %s error: %s' % (self.__class__.__name__, str(e)))

    @gen.coroutine
    def _query(self, sql, args):
        try:
            cursor = yield self.db.execute(sql, args)
            res = cursor.fetchone()
        except Exception as e:
            logging.error('DB %s error: %s' % (self.__class__.__name__, str(e)))
            res = None
        return res

    @gen.coroutine
    def _query_all(self, sql, args):
        try:
            cursor = yield self.db.execute(sql, args)
            res = cursor.fetchall()
        except Exception as e:
            logging.error('DB %s error: %s' % (self.__class__.__name__, str(e)))
            res = None
        return res
