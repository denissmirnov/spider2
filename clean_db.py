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

    def normalize(self):
        sql = """
            SELECT torrent_name
            FROM torrents
            GROUP BY torrent_name
            HAVING count(*) > 1 AND torrent_name IS NOT NULL
        """
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for row in res:
            name = row['torrent_name']
            sql = """
                SELECT *
                FROM torrents
                WHERE torrent_name = %s
            """
            self.cur.execute(sql, [name])
            torrents = self.cur.fetchall()
            ins_torrent = {}
            torrent_url = []
            for torrent in torrents:
                ins_torrent = torrent
                torrent_url += ins_torrent['torrent_url']
            ins_torrent['torrent_url'] = torrent_url
            sql = """
                DELETE from torrents
                WHERE
                  torrent_name = %s
            """
            self.cur.execute(sql, [name])
            sql = """
                INSERT INTO torrents 
                (
                    stamp,
                    details,
                    rating,
                    year,
                    genre,
                    torrent_name,
                    torrent_url,
                    torrent
                ) VALUES (
                    NOW(), 
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                );
            """
            self.cur.execute(sql, [json.dumps(ins_torrent['details']),
                                   ins_torrent['rating'],
                                   ins_torrent['year'],
                                   json.dumps(ins_torrent['genre']),
                                   ins_torrent['torrent_name'],
                                   json.dumps(ins_torrent['torrent_url']),
                                   json.dumps(ins_torrent['torrent'])])


def main():
    cleaner = Cleaner()
    cleaner.setup()
    cleaner.clean()
    cleaner.normalize()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
