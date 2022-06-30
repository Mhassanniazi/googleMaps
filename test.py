# import requests

# req = requests.get("https://www.google.com/maps/place/Pullman+Cologne/@50.9403925,6.9458566,17z/data=!4m10!3m9!1s0x47bf25a83a6b163d:0xdf0c46fd9954062c!5m2!4m1!1i2!8m2!3d50.9403925!4d6.9458566!9m1!1b1")
# print(req.text)

from selenium import webdriver
import time


driver = webdriver.Chrome("chromedriver.exe")
driver.get("https://www.google.com/maps/place/Pullman+Cologne/@50.9403925,6.9458566,17z/data=!4m10!3m9!1s0x47bf25a83a6b163d:0xdf0c46fd9954062c!5m2!4m1!1i2!8m2!3d50.9403925!4d6.9458566!9m1!1b1")
time.sleep(1)
print(driver.page_source)
driver.close()
driver.quit()





# import asyncio
# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# import scrapy
# from scrapy.crawler import CrawlerProcess
# # from selenium import webdriver
# import time
# import os
# from scrapy import signals
# from scrapy_playwright.page import PageCoroutine

# class formedLightingSpider(scrapy.Spider):
#     name = "formedLightingSpider"
#     url = "https://www.google.com/maps/place/Pullman+Cologne/@50.9403925,6.9458566,17z/data=!4m10!3m9!1s0x47bf25a83a6b163d:0xdf0c46fd9954062c!5m2!4m1!1i2!8m2!3d50.9403925!4d6.9458566!9m1!1b1"
    
#     def start_requests(self):
#         yield scrapy.Request(url=self.url,callback=self.parse)
#     def parse(self, response):
#         print(response.text)
#         # print("HASSAN",response.xpath('//div[@class="qT3SWc"]/button/div/text()').extract())


# process = CrawlerProcess()
# process.crawl(formedLightingSpider)
# process.start()
