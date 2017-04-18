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
        db_conf = {
            'host': config['db'].get('host', 'localhost'),
            'port': config['db'].get('port', 5432),
            'user': config['db'].get('username', 'postgres'),
            'password': config['db'].get('password', 'postgres'),
            'database': config['db'].get('dbname', 'postgres')
        }
    except Exception as e:
        logging.error("LOGD: Failed to load configuration. %s" % str(e))
        return 1

    logging.info('Starting main server')
    http_server = tornado.httpserver.HTTPServer(Application(db_conf))
    http_server.listen(options.application_port)

    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
