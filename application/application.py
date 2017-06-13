import os
import sys
import tornado.web
from application.handlers.ajax_list_handler import AjaxListHandler
from application.handlers.details_handler import DetailsHandler
from application.handlers.main_handler import MainHandler
from application.lib.db.torrents import Torrents


class Application(tornado.web.Application):
    """ Application tornado class """
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

        self.db = Torrents(db_conf)
        self.db.connect()

        self.rows_per_page = rows_per_page
