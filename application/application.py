import logging
import os

import momoko
import psycopg2
import psycopg2.extras
import sys
import tornado.web

from application.handlers.ajax_list_handler import AjaxListHandler
from application.handlers.details_handler import DetailsHandler
from application.handlers.main_handler import MainHandler


class Application(tornado.web.Application):
    def __init__(self, db_conf, rows_per_page):
        handlers = [
            (r"/", MainHandler),
            (r"/ajax_list", AjaxListHandler),
            (r"/details/id/([^/]+)", DetailsHandler),
            (r'/static/(.*)', tornado.web.StaticFileHandler,
             {'path': os.path.realpath(os.path.dirname(sys.argv[0])) + '/static/'}),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            debug=True,
            autoreload=True
        )
        super(Application, self).__init__(handlers, **settings)

        try:
            dsn = ("dbname=%s user=%s password=%s host=%s port=%s" % (
                db_conf['database'], db_conf['user'], db_conf['password'], db_conf['host'], db_conf['port']))
            self.db = momoko.Pool(
                dsn=dsn,
                size=1,
                cursor_factory=psycopg2.extras.RealDictCursor,
                max_size=1,
                reconnect_interval=500
            )
            self.db.connect()
        except Exception as e:
            logging.error('DB connection error ' + str(e))
            return

        self.rows_per_page = rows_per_page
