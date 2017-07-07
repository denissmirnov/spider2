import json
import logging

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.httpclient import AsyncHTTPClient
from tornado.options import define, options

from application.application import Application

define("application_port", default="7001")
define("config_file", default="config/main.json")
AsyncHTTPClient.configure(None, max_clients=10000)


def main():
    options.parse_command_line()

    config_file = options.config_file
    try:
        config = json.load(open(config_file))
        db_conf = config['db']
        rows_per_page = config.get('rows_per_page', 20),
    except BaseException as exc:
        logging.error("[x] Failed to load configuration. %s", str(exc))
        return 1

    logging.info('Starting main server')
    http_server = tornado.httpserver.HTTPServer(Application(db_conf, rows_per_page[0]))
    http_server.listen(options.application_port)

    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
