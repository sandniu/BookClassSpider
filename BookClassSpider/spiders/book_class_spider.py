import scrapy
import re
from scrapy.selector import Selector
from BookClassSpider.items import BookClassItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import (
    ConnectError,
    ConnectionDone,
    ConnectionLost,
    DNSLookupError,
    TCPTimedOutError,
) 

class BookClassSpider(scrapy.Spider):
    name = "book_class"

    def start_requests(self):
        urls = [
            'http://www.ztflh.com/?c=45735',
        ]
        for url in urls:
            print(url)
            self.logger.info(url)
            request = scrapy.Request(url=url, callback=self.parse,cb_kwargs=dict(pcode = "Z"),errback=self.parseError)
            request.cb_kwargs["level"] = 1 
            yield request

    def parse(self, response,pcode,level):
        items = response.xpath('//ul[@id="list"]//li').getall()

        for x in items:
            code = Selector(text=x).xpath('//span/text()').get()
            name = Selector(text=x).xpath('//a/text()').get()
            url = Selector(text=x).xpath('//a/@href').get()

            request = scrapy.Request(url=url, callback=self.parse,cb_kwargs=dict(pcode = code),errback=self.parseError)
            request.cb_kwargs["level"] = level + 1 
            yield request

            yield BookClassItem(code = code,name = name,pcode= pcode,level = level)

    def errorHandler(self,failure):
        # 日志记录所有的异常信息
        self.logger.error(repr(failure))

        # 假设我们需要对指定的异常类型做处理，
        # 我们需要判断异常的类型

        if failure.check(HttpError):
            # HttpError由HttpErrorMiddleware中间件抛出
            # 可以接收到非200 状态码的Response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # 此异常由请求Request抛出
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

    def parseError(self, failure):
        self.errorHandler(failure)
