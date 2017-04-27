import json


class System:
    def __init__(self, db):
        self.db = db

    async def get_torrents(self,
                           page_num,
                           rows_per_page,
                           rating_order,
                           year_order,
                           stamp_order,
                           genre_filter=None,
                           search_filter=None):
        sql = """
            SELECT 
                id, torrent_name, rating, year, genre, details, stamp, torrent, torrent_url
            FROM 
                torrents
        """

        if genre_filter:
            sql += "WHERE genre ? '%s'" % genre_filter

        if search_filter:
            if genre_filter:
                sql += ' AND '
            else:
                sql += ' WHERE '
            sql += "torrent_name ILIKE '%%" + search_filter + "%%'"

        if rating_order or year_order or stamp_order:
            sql += "ORDER BY"
            if rating_order:
                sql += " rating DESC, year, stamp "
            if year_order:
                sql += " year DESC, rating, stamp "
            if stamp_order:
                sql += " stamp DESC, rating, year "

        sql += " LIMIT %s OFFSET %s "

        offset = (page_num - 1) * rows_per_page
        cursor = await self.db.execute(sql, [rows_per_page, offset])
        res = cursor.fetchall()

        return res

    async def get_torrent(self, torrent_id):
        sql = """
            SELECT 
                *
            FROM 
                torrents t
            WHERE
                id = %s
        """
        cursor = await self.db.execute(sql, [torrent_id])
        res = cursor.fetchone()
        return res

    async def get_page_count(self, rows_on_page):
        sql = """
            SELECT 
                count(*) as cnt
            FROM 
                torrents
        """
        cursor = await self.db.execute(sql)
        res = cursor.fetchone()
        rows_count = res['cnt']

        os = rows_count % rows_on_page
        if os > 0:
            r = int(rows_count / rows_on_page) + 1
        else:
            r = int(rows_count / rows_on_page)
        return r
