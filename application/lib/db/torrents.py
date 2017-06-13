from application.lib.db.db import DB


class Torrents(DB):
    """ Model class torrents for selecting rows from table torrents """
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
        res = await self._query_all(sql, [rows_per_page, offset])

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
        res = await self._query(sql, [torrent_id])
        return res

    async def get_page_count(self, rows_on_page):
        sql = """
            SELECT 
                count(*) as cnt
            FROM 
                torrents
        """
        res = await self._query(sql, [])
        rows_count = res['cnt']

        os = rows_count % rows_on_page
        if os > 0:
            r = int(rows_count / rows_on_page) + 1
        else:
            r = int(rows_count / rows_on_page)
        return r

