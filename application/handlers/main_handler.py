import tornado.web

from application.lib.system import System


class MainHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    async def get(self, *args, **kwargs):
        system = System(self.application.db)
        page_count = await system.get_page_count(self.application.rows_per_page)

        genre_filter = self.get_argument('genre_filter', None)
        page_num = self.get_argument('page_num', 1)
        render_params = {
            'genre_filter': genre_filter,
            'search_filter': None,
            'page_num': page_num,
            'page_count': page_count,
        }
        self.render('index.twig', **render_params)

    async def post(self, *args, **kwargs):
        system = System(self.application.db)
        page_count = await system.get_page_count(self.application.rows_per_page)

        genre_filter = self.get_argument('genre_filter', None)
        search_filter = self.get_argument('search_filter', None)
        page_num = self.get_argument('page_num', 1)
        render_params = {
            'genre_filter': genre_filter,
            'search_filter': search_filter,
            'page_num': page_num,
            'page_count': page_count,
        }
        self.render('index.twig', **render_params)
