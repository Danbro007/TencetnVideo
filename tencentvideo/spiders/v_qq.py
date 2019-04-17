# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.http import Request
import re


class VQqSpider(scrapy.Spider):
    name = 'v.qq'
    allowed_domains = ['video.coral.qq.com']
    next = 6507261712650141754
    timestamp = 1555465577190
    videoid = 3753518160
    user_url = "http://video.coral.qq.com/review/user/{userid}"
    start_url = "https://video.coral.qq.com/varticle/{videoid}/comment/v2?callback=_varticle{videoid}commentv2&orinum=10&oriorder=o&pageflag=1&cursor={next}&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=132&_={timestamp}"

    def start_requests(self):
        yield Request(url=self.start_url.format(videoid=self.videoid, next=self.next, timestamp=self.timestamp),
                      callback=self.CommentList_parse)

    def CommentList_parse(self, response):
        result = json.loads(re.search("commentv2\((.*)\)", response.text).group(1))
        self.next = result.get("data").get("last")
        self.timestamp += 1
        userlist = result["data"]["userList"]

        for item in result.get("data").get("oriCommList"):
            print(userlist[item["userid"]]["nick"], item["content"])
        yield Request(url=self.start_url.format(videoid=self.videoid, next=self.next, timestamp=self.timestamp),
                      callback=self.CommentList_parse)
