# from scrapy import Spider
import scrapy
from scrapy.selector import Selector
from bgirls.items import BgirlsItem
# http://www.doubanmeinv.com/daxiongmei/list_1_2.html
# http://www.doubanmeinv.com/xiaoqiaotun/list_2_2.html
# http://www.doubanmeinv.com/heisiwa/list_3_2.html
# http://www.doubanmeinv.com/meituikong/list_4_2.html
# http://www.doubanmeinv.com/youyanzhi/list_5_2.html
# http://www.doubanmeinv.com/dazahui/list_6_2.html
class bgirlsSpider(scrapy.Spider):
    name = "bgirlsSpider"
    allowed_domain = ["doubanmeinv.com"]
    start_urls = [
        "http://www.doubanmeinv.com",
        "http://www.doubanmeinv.com/daxiongmei/list_1_1.html",
        "http://www.doubanmeinv.com/xiaoqiaotun/list_2_1.html",
        "http://www.doubanmeinv.com/heisiwa/list_3_1.html",
        "http://www.doubanmeinv.com/meituikong/list_4_1.html",
        "http://www.doubanmeinv.com/youyanzhi/list_5_1.html",
        "http://www.doubanmeinv.com/dazahui/list_6_1.html"
    ]
    mapName = ['flag','daxiongmei','xiaoqiaotun','heisiwa','meituikong','youyanzhi','dazahui']
    index = [0,1,1,1,1,1,1]

    def parse(self, response):
        if response.request.meta:
            print response.meta
        liResults = scrapy.Selector(response).xpath('//li[@class="span3"]')
        for li in liResults:
            for details in li.xpath('.//a[@target="_topic_detail"]'):
                for img in details.xpath('.//img'):
                    item = BgirlsItem()
                    item['currentURL'] = response.url
                    item['title'] = img.xpath('@title').extract()
                    item['src'] = img.xpath('@src').extract()
                    item['detailURL'] = details.xpath('@href').extract()
                    item['_id'] = response.url + ''.join(item['src'])
                    print item
                    yield item
            # self.index += 1
            # print self.index
        # nextPage = Selector(response).xpath('//li[@class="next next_page"]')
        # nextURL = nextPage.xpath('.//a').xpath('@href').extract()
        # print nextURL[0]
        # yield scrapy.Request(nextURL[0],callback=self.parse)
        url = response.url
        arr = url.split('/')
        if len(arr) > 3:
            urlIndex = self.mapName.index(arr[3])
            self.index[urlIndex] += 1
            nextIndexURL = 'list_%d_%d.html' % (urlIndex,self.index[urlIndex])
            arr[-1] = nextIndexURL
            # print 'url:' + '/'.join(arr)
            nextURL = '/'.join(arr)
            yield  scrapy.Request(nextURL,callback=self.parse,meta={'a':1})

