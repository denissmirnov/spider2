import json
import scrapy
from scrapy.http import TextResponse

from spider2.lib.system import System


class TorrentsSpider(scrapy.Spider):
    name = "torrents"
    db_conf = system = base_url = None

    def setup(self):
        config = json.load(open("config/main.json"))
        self.db_conf = {
            'host': config['db'].get('host', 'localhost'),
            'port': config['db'].get('port', 5432),
            'user': config['db'].get('username', 'postgres'),
            'password': config['db'].get('password', 'postgres'),
            'database': config['db'].get('dbname', 'postgres'),
        }
        self.base_url = config['torrent_base_url']
        self.system = System(self.db_conf)

    def start_requests(self):
        self.setup()
        urls = [
            self.base_url + '/kino',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.xpath('//tr[@class="gai"]//td[@colspan="2"]//a[contains(@href, "/torrent/")]'):
            torrent = {
                'url': self.base_url + quote.xpath('@href').extract()[0],
                'text': quote.xpath('text()').extract()[0]
            }
            res = self.system.add_torrent(torrent)

            if res:
                next_page = torrent['url']
                next_page = response.urljoin(next_page)
                request = scrapy.Request(next_page, callback=self.parse_torrent)
                request.meta['url'] = torrent['url']
                request.meta['name'] = torrent['text']
                yield request

    def parse_torrent(self, response):
        details_node = response.xpath('//table[@id="details"]//tr//td[not(contains(@style,"vertical-align:top;"))]')
        torrent = details_node.xpath('//a[contains(@href, "download")]')
        torrent_url = [{'name': response.meta['name'], 'url': self.base_url + torrent.xpath('@href').extract_first()}]
        kinopoisk = details_node.xpath('//a[contains(@href, "kinopoisk")]')
        kinopoisk_url = kinopoisk.xpath('@href').extract_first()
        self.system.add_torrent_url(response.meta['url'], torrent_url)

        if kinopoisk_url:
            request = scrapy.Request(kinopoisk_url, callback=self.parse_kinopoisk)
            request.meta['url'] = response.meta['url']
            yield request

    def parse_kinopoisk(self, response):
        details = {}
        img = response.xpath('//img[contains(@src, "film_iphone")]')
        details['image'] = img.xpath('@src').extract_first()
        details['synopsys'] = response.xpath('//div[@class="brand_words film-synopsys"]/text()').extract_first()
        details['rating'] = response.xpath('//span[@class="rating_ball"]/text()').extract_first()
        details['name'] = response.xpath('//h1[@class="moviename-big"]/text()').extract_first()
        if not details['rating']:
            details['rating'] = 0
        details['year'] = response.xpath('//a[contains(@href, "year")]/text()').extract_first()
        genre = []
        for q_genre in response.xpath('//a[contains(@href, "genre")]'):
            genre.append(q_genre.xpath('text()').extract()[0])
        details['genre'] = genre

        self.system.add_details(response.meta['url'], json.dumps(details))
