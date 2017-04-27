import json

import tornado.web

from application.lib.system import System


class AjaxListHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    async def post(self, *args, **kwargs):
        req = json.loads(self.request.body.decode())
        rating_order = req.get('rating_order', False)
        year_order = req.get('year_order', False)
        stamp_order = req.get('stamp_order', False)
        genre_filter = req.get('genre_filter', None)
        if genre_filter == 'None':
            genre_filter = None
        search_filter = req.get('search_filter', None)
        if search_filter == 'None':
            search_filter = None
        page_num = req.get('page_num', 1)

        system = System(self.application.db)
        torrents = await system.get_torrents(page_num,
                                             self.application.rows_per_page,
                                             rating_order,
                                             year_order,
                                             stamp_order,
                                             genre_filter,
                                             search_filter)

        render_params = {
            'torrents': torrents
        }
        self.render('list.twig', **render_params)
