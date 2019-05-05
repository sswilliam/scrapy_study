import scrapy
import os
import json
#this spider will first read the basicinfo.json to get the first page of the suite
#and then extract all the image urls 
#and then goto the next page if there exists
#and then save all urls and image urls into detail.json

class QuotesSpider(scrapy.Spider):
    name = "debug_suite_page_download"
    cookies = None
    def start_requests(self):
        print(self.cookies)
        if self.cookies == None:
            with open("cookies.json") as f:
                self.cookies = json.load(f)

        print(self.cookies)
        print(self.cookies['__cfduid'])
        # exit("hello")
        for dirname in os.listdir("cache1"):
            if dirname != '.' and dirname != '..' and dirname != '.DS_Store':
                if os.path.exists("cache1/"+dirname+"/detailed.json"):
                    continue
                file_name="cache1/"+dirname+"/basicinfo.json"
                with open(file_name) as f:
                    basicinfo = json.load(f)
                request = scrapy.Request(basicinfo["href"], callback=self.parse,cookies={
                    '__cfduid':self.cookies['__cfduid'],
                    'UM_distinctid':self.cookies['UM_distinctid'],
                    'wordpress_test_cookie':self.cookies['wordpress_test_cookie'],
                    'wordpress_logged_in_fcc244ea95ea78eb7ad8f215abfc28a9':self.cookies['wordpress_logged_in_fcc244ea95ea78eb7ad8f215abfc28a9'],
                    'wp-settings-time-87463':self.cookies['wp-settings-time-87463'],
                    'CNZZDATA1257363932':self.cookies['CNZZDATA1257363932']

                })
                # request = scrapy.Request(basicinfo["href"], callback=self.parse,cookies={
                #     '__cfduid':'d5f5332409feec15b6e02a84cab5584cb1535950652',
                #     'UM_distinctid':'1659dcb09351c3-065f1f288e81b4-34647908-232800-1659dcb0936221',
                #     'wordpress_test_cookie':'WP+Cookie+check',
                #     'wordpress_logged_in_fcc244ea95ea78eb7ad8f215abfc28a9':'dafunk%7C1541735903%7CF5kxhDv4w50mzhYWaFrWady1guRG8WTTIPzMGF8us9T%7C93dbe975ee7ba9590a601cf4c5f62169b01a56c7c904106af943cc17a999c120',
                #     'wp-settings-time-87463':'1541563103',
                #     'CNZZDATA1257363932':'166401380-1535946494-%7C1541562927'

                # })
                # print(request.cookies)
                # exit("hello")
                request.meta['dirname']=dirname
                yield request


    def parse(self, response):
        title = response.meta['dirname']
        print("-----------------"+title)
        with open("cache1/"+title+"/body.html", 'wb') as f:
            f.write(response.body)
        
        # saved_dict={}

        # title = response.meta['dirname']
        # tag_cloud=response.xpath('//div[@class="tagcloud"]')
        # if tag_cloud != None:
        #     saved_dict['tag'] = []
        #     tag_links = tag_cloud.xpath('./a[@rel="tag"]/text()')
        #     for tag in tag_links:
        #         saved_dict['tag'].append(tag.extract())
        # saved_dict['pages'] = []
        # saved_dict['pages'].append(response.url)
        
        # page_list=response.xpath('//div[@class="pagelist"]')
        # print(page_list)
        # if page_list != None:
        #     links = page_list.xpath('./a/attribute::href')
        #     for link in links:
        #         saved_dict['pages'].append(link.extract())

        # saved_dict['imgs'] = []
        # content = response.xpath('//div[@id="post_content"]')
        # imgs = content.xpath('./p/img/attribute::src')
        # for img in imgs:
        #     saved_dict['imgs'].append(img.extract())
        # if len(saved_dict['pages']) == 1:
        #     with open("cache1/"+title+"/detailed.json", 'wb') as f:
        #         f.write(json.dumps(saved_dict).encode(encoding="utf-8"))
        #     yield saved_dict
        # else:
        #     request = scrapy.Request(saved_dict['pages'][1], callback=self.parse_left,cookies={
        #             '__cfduid':self.cookies['__cfduid'],
        #             'UM_distinctid':self.cookies['UM_distinctid'],
        #             'wordpress_test_cookie':self.cookies['wordpress_test_cookie'],
        #             'wordpress_logged_in_fcc244ea95ea78eb7ad8f215abfc28a9':self.cookies['wordpress_logged_in_fcc244ea95ea78eb7ad8f215abfc28a9'],
        #             'wp-settings-time-87463':self.cookies['wp-settings-time-87463'],
        #             'CNZZDATA1257363932':self.cookies['CNZZDATA1257363932']

        #         })
        #     request.meta['saved_dist'] = saved_dict
        #     request.meta['current'] = 1
        #     request.meta['dirname'] = response.meta['dirname']
        #     yield request
         
    def parse_left(self, response):
        saved_dict=response.meta['saved_dist']
        current = response.meta['current']
        content = response.xpath('//div[@id="post_content"]')
        imgs = content.xpath('./p/img/attribute::src')
        title = response.meta['dirname']
        for img in imgs:
            saved_dict['imgs'].append(img.extract())

        if current == len(saved_dict["pages"])-1:
            with open("cache1/"+title+"/detailed.json", 'wb') as f:
                f.write(json.dumps(saved_dict).encode(encoding="utf-8"))
            yield saved_dict
        else:
            request = scrapy.Request(saved_dict['pages'][current+1], callback=self.parse_left,cookies={
                    '__cfduid':self.cookies['__cfduid'],
                    'UM_distinctid':self.cookies['UM_distinctid'],
                    'wordpress_test_cookie':self.cookies['wordpress_test_cookie'],
                    'wordpress_logged_in_fcc244ea95ea78eb7ad8f215abfc28a9':self.cookies['wordpress_logged_in_fcc244ea95ea78eb7ad8f215abfc28a9'],
                    'wp-settings-time-87463':self.cookies['wp-settings-time-87463'],
                    'CNZZDATA1257363932':self.cookies['CNZZDATA1257363932']

                })
            request.meta['saved_dist'] = saved_dict
            request.meta['current'] = current+1
            request.meta['dirname'] = response.meta['dirname']
            yield request
