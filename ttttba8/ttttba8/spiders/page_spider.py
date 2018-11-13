import scrapy
import os
import json
import URL as urlconfig

#this spider will open the site page from the first one
#and then check whether this suite exists in the cache folder or not
#if hit the cache
#exit directly because we have already donwload the suites info before
#it will generate the cache file and generate the basicinfo.json
#in the basicinfo.json, the most important is the first page of the suite
#anc the cover url
class QuotesSpider(scrapy.Spider):
    name = "page"

    def start_requests(self):
       #entry page is the index page
        url = urlconfig.home_url
        request = scrapy.Request(url= url, callback=self.parse)
        request.meta['page']=1
        yield request

    def parse(self, response):
        all_li = response.xpath('//li[@class="post box row "]')
        for each_li in all_li:
            href = each_li.xpath('./div/a[@class="zoom"]/attribute::href').extract_first()
            title = each_li.xpath('./div/a[@class="zoom"]/attribute::title').extract_first()
            if os.path.exists("cache/"+title):
                print(title+" already exist, exit the crap")
                exit("hello")
            cover = each_li.xpath('./div/a[@class="zoom"]/img/attribute::src').extract_first()
            category = each_li.xpath('./div[@class="info"]/span/a[@rel="category tag"]/text()').extract_first()
            basic_info = {
                'href': each_li.xpath('./div/a[@class="zoom"]/attribute::href').extract_first(),
                'title': each_li.xpath('./div/a[@class="zoom"]/attribute::title').extract_first(),
                'cover': each_li.xpath('./div/a[@class="zoom"]/img/attribute::src').extract_first(),
                'category': each_li.xpath('./div[@class="info"]/span/a[@rel="category tag"]/text()').extract_first()
            }
            
            os.makedirs("cache/"+title)
            with open("cache/"+title+"/basicinfo.json", 'wb') as f:
                f.write(json.dumps(basic_info).encode(encoding="utf-8"))
        page = response.meta['page']+1
        url = urlconfig.home_url+'page/'+str(page)+'/'
        request = scrapy.Request(url= url, callback=self.parse)
        request.meta['page']=page
        yield request