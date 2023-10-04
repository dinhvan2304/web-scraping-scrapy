import scrapy
import pandas as pd
from scrapy import Request
import os
class PharmapproachSpider(scrapy.Spider):
    name = 'pharmapproach'
    allowed_domains = ['www.pharmapproach.com']
    url = []
    for page in range(1, 2, 1):
        url.append('https://www.pharmapproach.com/list-of-pharmaceutical-companies-in-united-states-of-america/{}/'.format(page))
    
    start_urls = url
    start_urls = ['https://www.pharmapproach.com/list-of-pharmaceutical-companies-in-united-states-of-america/22/']
    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url,callback=self.parse ,headers=headers)
    def parse(self, response):
        # header = response.xpath("//div[@class='row']/div[@class='col-md-8']/div[@class='px-blog-post']/div[@class='px-content']/p[1]/a/text()").extract()
        # print(header)
        for index in range(10,26,1):
            header = response.xpath("//div[@class='px-blog-post']/div[@class='px-content']/h3[{}]/span/text()".format(index)).extract_first()
            
            content = response.xpath("//div[@class='col-md-8']/div[@class='px-blog-post']/div[@class='px-content']/p[{}]/text()".format(index+3)).extract()
            content_solved = [value.replace('\n','') for value in content]
            content_solved = content_solved[:-1]
            
            website = response.xpath("//div[@class='row']/div[@class='col-md-8']/div[@class='px-blog-post']/div[@class='px-content']/p[{}]/a/text()".format(index+3)).extract_first()
            dict_temp = {'header': header,
                         'content': content_solved,
                         'website': website}
            path = '/Users/dinhvan/Projects/Code/crawl/scrapy/Pharmapproach/Pharmapproach/spiders/pharmapproach.csv'
            data = pd.DataFrame([dict_temp])
            data.to_csv(path, mode='a', header=not os.path.exists(path), index=False)
            
