import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    async def get(self, *args, **kwargs):
        genre_filter = self.get_argument('genre_filter', None)
        render_params = {
            'genre_filter': genre_filter,
            'search_filter': None
        }
        self.render('index.twig', **render_params)

    async def post(self, *args, **kwargs):
        genre_filter = self.get_argument('genre_filter', None)
        search_filter = self.get_argument('search_filter', None)
        render_params = {
            'genre_filter': genre_filter,
            'search_filter': search_filter
        }
        self.render('index.twig', **render_params)
