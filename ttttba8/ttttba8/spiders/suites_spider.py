import scrapy
import os
import json
#this spider will first read the basicinfo.json to get the first page of the suite
#and then extract all the image urls 
#and then goto the next page if there exists
#and then save all urls and image urls into detail.json

class QuotesSpider(scrapy.Spider):
    name = "suites"
    cookies = None
    def start_requests(self):
        self.load_cookies()
        for dirname in os.listdir("cache"):
            if dirname != '.' and dirname != '..' and dirname != '.DS_Store':#and dirname == 'XIAOYU画语界 2019.02.19 VOL.022 Miko酱 57P'
                if os.path.exists("cache/"+dirname+"/detailed.json"):
                    continue
                file_name="cache/"+dirname+"/basicinfo.json"
                with open(file_name) as f:
                    basicinfo = json.load(f)
                request = scrapy.Request(basicinfo["href"], callback=self.parse,cookies=self.cookies)
                request.meta['dirname']=dirname
                yield request


    def load_cookies(self):
        if self.cookies == None:
            with open("cookies.txt") as f:
                cookieline = f.readline()
            print(cookieline)
            cookies = cookieline.split(";")
            self.cookies = {}
            for cookie_item in cookies:
                print(cookie_item.strip())
                cookie_pair = cookie_item.strip().split("=")
                self.cookies[cookie_pair[0]] = cookie_pair[1]
            print(self.cookies)

    def parse(self, response):
        saved_dict={}

        title = response.meta['dirname']
        tag_cloud=response.xpath('//div[@class="tagcloud"]')
        if tag_cloud != None:
            saved_dict['tag'] = []
            tag_links = tag_cloud.xpath('./a[@rel="tag"]/text()')
            for tag in tag_links:
                saved_dict['tag'].append(tag.extract())
        saved_dict['pages'] = []
        saved_dict['pages'].append(response.url)
        
        page_list=response.xpath('//div[@class="pagelist"]')
        print(page_list)
        if page_list != None:
            links = page_list.xpath('./a/attribute::href')
            for link in links:
                saved_dict['pages'].append(link.extract())

        saved_dict['imgs'] = []
        content = response.xpath('//div[@id="post_content"]')
        print("============")
        content_str = content.extract()[0]
        print(content_str)
        print("============")
        imgs = content.xpath('./p/img/attribute::src')
        for img in imgs:
            saved_dict['imgs'].append(img.extract())
        if len(saved_dict['pages']) == 1:
            with open("cache/"+title+"/detailed.json", 'wb') as f:
                f.write(json.dumps(saved_dict).encode(encoding="utf-8"))
            yield saved_dict
        else:
            request = scrapy.Request(saved_dict['pages'][1], callback=self.parse_left,cookies=self.cookies)
            request.meta['saved_dist'] = saved_dict
            request.meta['current'] = 1
            request.meta['dirname'] = response.meta['dirname']
            yield request
         
    def parse_left(self, response):
        saved_dict=response.meta['saved_dist']
        current = response.meta['current']
        content = response.xpath('//div[@id="post_content"]')
        imgs = content.xpath('./p/img/attribute::src')
        title = response.meta['dirname']
        for img in imgs:
            saved_dict['imgs'].append(img.extract())

        if current == len(saved_dict["pages"])-1:
            with open("cache/"+title+"/detailed.json", 'wb') as f:
                f.write(json.dumps(saved_dict).encode(encoding="utf-8"))
            yield saved_dict
        else:
            request = scrapy.Request(saved_dict['pages'][current+1], callback=self.parse_left,cookies=self.cookies)
            request.meta['saved_dist'] = saved_dict
            request.meta['current'] = current+1
            request.meta['dirname'] = response.meta['dirname']
            yield request
