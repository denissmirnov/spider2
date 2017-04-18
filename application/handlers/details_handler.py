import tornado.web
from bs4 import BeautifulSoup

from application.lib.system import System


class DetailsHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    async def get(self, torrent_id, *args, **kwargs):
        system = System(self.application.db)
        torrent = await system.get_torrent(torrent_id)

        render_params = {
            'torrent': torrent,
        }
        self.render('details.twig', **render_params)
