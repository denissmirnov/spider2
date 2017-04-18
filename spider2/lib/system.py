import json
import logging

import psycopg2
import psycopg2.extras


class System:
    db_conf = db = cur = app = None

    def __init__(self, db_conf):
        self.db_conf = db_conf
        self.db_connect()

    def db_connect(self):
        try:
            self.db = psycopg2.connect(**dict(self.db_conf))
            self.db.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            self.cur = self.db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        except BaseException as e:
            logging.error('DB connection error %s' % str(e))
            pass

    def add_torrent(self, torrent):
        sql = """
                SELECT 
                    *
                FROM 
                    torrents 
                WHERE 
                    url = %s
                """
        self.cur.execute(sql, [torrent['url']])
        res = self.cur.fetchone()

        if not res:
            sql = """
                INSERT INTO torrents 
                (
                    url, 
                    text
                ) VALUES (
                    %s, 
                    %s
                ) RETURNING id;
            """
            self.cur.execute(sql, [torrent['url'], torrent['text']])
            return True
        else:
            return None

    def add_details(self, url, details):
        j = json.loads(details)
        sql = """
                UPDATE 
                    torrents
                SET
                    details = %s,
                    rating = %s,
                    year = %s,
                    genre = %s,
                    torrent_name = %s
                WHERE 
                    url = %s
                """
        self.cur.execute(sql, [details, j['rating'], j['year'], json.dumps(j['genre']), j['name'], url])

    def add_torrent_url(self, url, torrent_url):
        sql = """
                UPDATE 
                    torrents
                SET
                    torrent_url = %s
                WHERE 
                    url = %s
                """
        self.cur.execute(sql, [json.dumps(torrent_url), url])
