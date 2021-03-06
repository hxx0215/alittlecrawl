# from scrapy import Spider
import scrapy
from scrapy.selector import Selector
from bgirls.items import BgirlsItem
import urlparse
import random

class bgirlsSpider(scrapy.Spider):
    name = "bgirlsSpider"
    allowed_domain = ["dbmeinv.com"]
    start_urls = [
        "http://www.dbmeinv.com/dbgroup/show.htm?cid=0&pager_offset=1",
        "http://www.dbmeinv.com/dbgroup/today.htm",
        "http://www.dbmeinv.com/dbgroup/rank.htm"
    ]
    cid = 0
    page_offset = [1,1,1]
    mapName = ["/dbgroup/show.htm","/dbgroup/today.htm","/dbgroup/rank.htm"]
    userAgent = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    ]

    def randomHead(self):
        index = random.randint(0,16)
        return {'User-Agent':self.userAgent[index]}

    def start_requests(self):
        header = self.randomHead()
        return [
            scrapy.Request("http://www.dbmeinv.com/dbgroup/show.htm?cid=0&pager_offset=1",headers = header),
            scrapy.Request("http://www.dbmeinv.com/dbgroup/today.htm",headers = header),
            scrapy.Request("http://www.dbmeinv.com/dbgroup/rank.htm",headers = header),
                ]

    def parse(self, response):
        liResults = scrapy.Selector(response).xpath('//li[@class="span3"]')
        for li in liResults:
            for details in li.xpath('.//a[@target="_topic_detail"]'):
                for img in details.xpath('.//img'):
                    item = BgirlsItem()
                    item['currentURL'] = response.url
                    item['title'] = img.xpath('@title').extract()
                    item['src'] = img.xpath('@src').extract()
                    item['detailURL'] = details.xpath('@href').extract()
                    item['_id'] = "".join(item['src'])
                    print item
                    yield item
        if liResults:#next_page
            parse = urlparse.urlparse(response.url)
            urlIndex = self.mapName.index(parse.path)
            self.page_offset[urlIndex] += 1
            if "show.htm" in response.url:
                nextURL = parse.scheme + "://" + parse.netloc + parse.path + "?cid=%d&pager_offset=%d" \
                                                                             % (self.cid,self.page_offset[urlIndex])
            else:
                nextURL = parse.scheme + "://" + parse.netloc + parse.path + "?pager_offset=%d" \
                                                                             % self.page_offset[urlIndex]
            yield scrapy.Request(nextURL,callback=self.parse,headers=self.randomHead())
        else:#next_category
            if "show.htm" in response.url:
                if self.cid == 0:
                    self.cid = 1
                self.cid += 1
                if self.cid > 8:
                    return
                self.page_offset[0] = 1
                nextURL = "http://www.dbmeinv.com/dbgroup/show.htm?cid=%d&pager_offset=%d" %(self.cid,self.page_offset[0])
                yield scrapy.Request(nextURL,callback=self.parse,headers=self.randomHead())


    def parse_detailItem(self, response):
        mainItem = response.request.meta['mainItem']
        yield mainItem
