import scrapy
import os
import json
import xml.etree.ElementTree as ET

#this spider will first read the basicinfo.json to get the first page of the suite
#and then extract all the image urls 
#and then goto the next page if there exists
#and then save all urls and image urls into detail.json

class QuotesSpider(scrapy.Spider):
    name = "debug_suite_page_parser"
    cookies = None
    def start_requests(self):
        self.load_cookies()
        request = scrapy.Request("http://www.ttttba8.com/zatu/wanimal-201901/", callback=self.parse,cookies=self.cookies)
        # request = scrapy.Request("http://www.ttttba8.com/zatu/wanimal-201901/", callback=self.parse)
        request.meta['dirname']="test"
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
        # title = response.meta['dirname']
        # with open("cache1/test/body1.html", 'wb') as f:
        #     f.write(response.body)
        # print("----------------")
        # print(response.body)
        # print("----------------")
        
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
        # print(")))))))))))-------------debug block")
        # print(content.extract()[0])
        # content_str = content.extract()[0]
        # content_str = content_str.replace("<br>","")
        # print(content_str)
        # print(")))))))))))")
        # xml = etree.parse("./py24.xml")
        # tree = ET.fromstring(content.extract()[0])
        # root = tree.getroot()
        # print(root)

        # print(")))))))))))-------------debug block")
        # imgs = content.xpath('./p')
        # imgs = content.xpath('./p/img[@data-lazy-type="image"]/attribute::data-lazy-src')
        imgs = content.xpath('./p/img/attribute::src')
        print("===================")
        print(len(imgs))
        print("===================")
        for img in imgs:
            print("        "+img.extract())
            saved_dict['imgs'].append(img.extract())
        # if len(saved_dict['pages']) == 1:
        #     with open("cache1/"+title+"/detailed.json", 'wb') as f:
        #         f.write(json.dumps(saved_dict).encode(encoding="utf-8"))
        #     yield saved_dict
        # else:
        #     print("no else")
            # request = scrapy.Request(saved_dict['pages'][1], callback=self.parse_left,cookies={
            #         '__cfduid':self.cookies['__cfduid'],
            #         'UM_distinctid':self.cookies['UM_distinctid'],
            #         'wordpress_test_cookie':self.cookies['wordpress_test_cookie'],
            #         'wordpress_logged_in_fcc244ea95ea78eb7ad8f215abfc28a9':self.cookies['wordpress_logged_in_fcc244ea95ea78eb7ad8f215abfc28a9'],
            #         'wp-settings-time-87463':self.cookies['wp-settings-time-87463'],
            #         'CNZZDATA1257363932':self.cookies['CNZZDATA1257363932']

            #     })
            # request.meta['saved_dist'] = saved_dict
            # request.meta['current'] = 1
            # request.meta['dirname'] = response.meta['dirname']
            # yield request
         
    # def parse_left(self, response):
    #     saved_dict=response.meta['saved_dist']
    #     current = response.meta['current']
    #     content = response.xpath('//div[@id="post_content"]')
    #     imgs = content.xpath('./p/img/attribute::src')
    #     title = response.meta['dirname']
    #     for img in imgs:
    #         saved_dict['imgs'].append(img.extract())

    #     if current == len(saved_dict["pages"])-1:
    #         with open("cache1/"+title+"/detailed.json", 'wb') as f:
    #             f.write(json.dumps(saved_dict).encode(encoding="utf-8"))
    #         yield saved_dict
    #     else:
    #         request = scrapy.Request(saved_dict['pages'][current+1], callback=self.parse_left,cookies={
    #                 '__cfduid':self.cookies['__cfduid'],
            #         'UM_distinctid':self.cookies['UM_distinctid'],
            #         'wordpress_test_cookie':self.cookies['wordpress_test_cookie'],
            #         'wordpress_logged_in_fcc244ea95ea78eb7ad8f215abfc28a9':self.cookies['wordpress_logged_in_fcc244ea95ea78eb7ad8f215abfc28a9'],
            #         'wp-settings-time-87463':self.cookies['wp-settings-time-87463'],
            #         'CNZZDATA1257363932':self.cookies['CNZZDATA1257363932']

            #     })
            # request.meta['saved_dist'] = saved_dict
            # request.meta['current'] = current+1
            # request.meta['dirname'] = response.meta['dirname']
            # yield request
