import tornado.web


class DetailsHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    async def get(self, torrent_id, *args, **kwargs):
        db = self.application.db
        torrent = await db.get_torrent(torrent_id)

        render_params = {
            'torrent': torrent,
        }
        self.render('details.html', **render_params)
