import json

import logging
import psycopg2
import psycopg2.extras


class Cleaner:
    db_conf = db = cur = None

    def setup(self):
        config = json.load(open("config/main.json"))
        self.db_conf = {
            'host': config['db'].get('host', 'localhost'),
            'port': config['db'].get('port', 5432),
            'user': config['db'].get('username', 'postgres'),
            'password': config['db'].get('password', 'postgres'),
            'database': config['db'].get('dbname', 'postgres'),
        }

        try:
            self.db = psycopg2.connect(**dict(self.db_conf))
            self.db.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            self.cur = self.db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        except BaseException as e:
            logging.error('DB connection error %s' % str(e))
            pass

    def clean(self):
        sql = """
            DELETE from torrents
            WHERE
              details IS NULL OR rating = 0
        """
        self.cur.execute(sql)


def main():
    cleaner = Cleaner()
    cleaner.setup()
    cleaner.clean()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
