# from scrapy import Spider
import scrapy
from scrapy.selector import Selector
from bgirls.items import BgirlsItem
import urlparse

class bgirlsSpider(scrapy.Spider):
    name = "bgirlsSpider"
    allowed_domain = ["dbmeinv.com"]
    start_urls = [
        # "http://www.doubanmeinv.com",
        # "http://www.doubanmeinv.com/daxiongmei/list_1_1.html",
        # "http://www.doubanmeinv.com/xiaoqiaotun/list_2_1.html",
        # "http://www.doubanmeinv.com/heisiwa/list_3_1.html",
        # "http://www.doubanmeinv.com/meituikong/list_4_1.html",
        # "http://www.doubanmeinv.com/youyanzhi/list_5_1.html",
        # "http://www.doubanmeinv.com/dazahui/list_6_1.html"
        # http://dbhaohaizi.host3v.com/fuli1.html
        "http://www.dbmeinv.com/dbgroup/show.htm?cid=0&pager_offset=1",
        "http://www.dbmeinv.com/dbgroup/today.htm",
        "http://www.dbmeinv.com/dbgroup/rank.htm"
    ]
    # mapName = ['flag','daxiongmei','xiaoqiaotun','heisiwa','meituikong','youyanzhi','dazahui']
    # index = [0,1,1,1,1,1,1]
    cid = 0
    #TODO: change offset to Array
    page_offset = 1

    def start_requests(self):
        header = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        return [
            scrapy.Request("http://www.dbmeinv.com/dbgroup/show.htm?cid=0&pager_offset=1",headers = header),
            scrapy.Request("http://www.dbmeinv.com/dbgroup/today.htm",headers = header),
            scrapy.Request("http://www.dbmeinv.com/dbgroup/rank.htm",headers = header),
                ]

    def parse(self, response):
        # if response.request.meta:
        #     print response.meta
        liResults = scrapy.Selector(response).xpath('//li[@class="span3"]')
        for li in liResults:
            for details in li.xpath('.//a[@target="_topic_detail"]'):
                for img in details.xpath('.//img'):
                    item = BgirlsItem()
                    item['currentURL'] = response.url
                    item['title'] = img.xpath('@title').extract()
                    item['src'] = img.xpath('@src').extract()
                    item['detailURL'] = details.xpath('@href').extract()
                    item['_id'] = "".join(item['detailURL'])
                    print item
                    yield item
        if liResults:#next_page
            parse = urlparse.urlparse(response.url)
            self.page_offset += 1
            if "show.htm" in response.url:
                nextURL = parse.scheme + "://" + parse.netloc + parse.path + "?cid=%d&pager_offset=%d" % (self.cid,self.page_offset)
            else:
                nextURL = parse.scheme + "://" + parse.netloc + parse.path + "?pager_offset=%d" % self.page_offset
            yield scrapy.Request(nextURL,callback=self.parse)
        else:#next_category
            if "show.htm" in response.url:
                if self.cid == 0:
                    self.cid = 1
                self.cid += 1
                self.page_offset = 1
                nextURL = "http://www.dbmeinv.com/dbgroup/show.htm?cid=%d&pager_offset=%d" %(self.cid,self.page_offset)
                yield scrapy.Request(nextURL,callback=self.parse)
            else:
                self.page_offset = 1


        # url = response.url
        # arr = url.split('/')
        # if len(arr) > 3:
        #     urlIndex = self.mapName.index(arr[3])
        #     self.index[urlIndex] += 1
        #     nextIndexURL = 'list_%d_%d.html' % (urlIndex,self.index[urlIndex])
        #     arr[-1] = nextIndexURL
        #     nextURL = '/'.join(arr)
        #     yield  scrapy.Request(nextURL,callback=self.parse,meta={'a':1})

    def parse_detailItem(self, response):
        mainItem = response.request.meta['mainItem']
        yield mainItem
