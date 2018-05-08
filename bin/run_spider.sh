#!/bin/sh
PATH=/usr/local/bin:/usr/local/bin/scrapy:/usr/local/sbin:~/bin:/usr/bin:/bin:/usr/sbin:/sbin
cd /Users/den/Projects/local/spider2
scrapy crawl torrents
python3 clean_db.py

