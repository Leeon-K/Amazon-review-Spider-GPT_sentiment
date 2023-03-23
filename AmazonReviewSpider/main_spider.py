# encoding='utf8'
# from AmazonReviewSpider.html_downloader import Downloader
# from AmazonReviewSpider.html_parser import HtmlParser
# from AmazonReviewSpider.spider_output import OutPutUse
# from AmazonReviewSpider.url_manager import UrlManager

from html_downloader import Downloader
from html_parser import HtmlParser
from spider_output import OutPutUse
from url_manager import UrlManager
'''
在尝试重新打包并且使用--hidden-import queue 后，程序能够正常运行。
pyinstaller -F --hidden-import=queue main_spider.py  
'''
import requests

class Scheduler(object):
    def __init__(self):
        self.url_manager = UrlManager()
        self.downloader = Downloader()
        self.parser = HtmlParser(self.url_manager.get_amazon_base_url())
        self.output = OutPutUse()
        # self.headers = {
        #     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36',
        # }
        self.headers = {'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        self.proxy_id = { "http": "http://61.135.155.82:443"}
        self.cookie = {'session-id':'459-4568418-5692641', 'ubid-acbcn':'459-5049899-3055220','x-wl-uid':'1AK7YMFc9IzusayDn2fT6Topjz3iAOpR3EeA2UQSqco8fo5PbK2aCpyBA/fdPMfKFqZRHc4IeyuU=','session-token':'"OH1wPvfOj6Tylq2nnJcdn5wyxycR/lqyGsGU3+lUtU4mbC0ZD9s8/4Oihd1BlskUQG8zRbLVs9vfWXuiJmnRlDT4x35ircp2uLxOLNYQ4j5pzdFJIqqoZUnhHSJUq2yK80P3LqH8An7faXRCPW9BIqX1wu0WmHlSS9vYAPKA/2SGdV9b//EljYjIVCBjOuR/dKRiYEeGK3li0RJOVz7+vMWg7Rnzbx89QxlbCp0WyquZyVxG6f2mNw=="','csm-hit':'tb:0J5M3DH92ZKHNKA0QBAF+b-0J5M3DH92ZKHNKA0QBAF|1544276572483&adb:adblk_no','session-id-time':'2082787201l'}


    def get_all_review_url(self, main_page_reviews_url):
        # review_content = self.downloader.download(main_page_reviews_url, retry_count=2, headers=self.headers)
        review_content = requests.get(main_page_reviews_url, headers=self.headers, proxies=self.proxy_id,cookies=self.cookie)
        reviews_url_list = [main_page_reviews_url]
    
        next_reviews_url = self.parser.get_next_reviews_url(review_content)
        # i=0
        while next_reviews_url != "":
            # i = i+1 # 先爬10页
            reviews_url_list.append(next_reviews_url)
            # review_content = self.downloader.download(next_reviews_url, retry_count=2, headers=self.headers)
            review_content = requests.get(next_reviews_url, headers=self.headers, proxies=self.proxy_id,cookies=self.cookie)
            next_reviews_url = self.parser.get_next_reviews_url(review_content)
        return reviews_url_list

    def run(self):
        main_url_list = self.url_manager.get_all_main_url_from_file()

        for index in range(len(main_url_list)):
            main_url = main_url_list[index]
            try:
                self.run_a_main_url(index, main_url)
            except BaseException as e:
                print("商品抓取评论失败，地址:" + main_url + str(e))
            # self.output.save_review_info() # 不需要多余的保存
        self.output.save_review_info()

    def run_a_main_url(self, index, main_url):
        # content = self.downloader.download(main_url, retry_count=2, headers=self.headers, proxies=self.proxy_id,cookies=self.cookie)
        content =  requests.get(main_url, headers=self.headers, proxies=self.proxy_id,cookies=self.cookie)
        main_page_reviews_url = self.parser.parse_main_page_reviews_url(content)
        print("Scheduler.run开始下载商品评论，index=" + str(index))
        all_review_url = self.get_all_review_url(main_page_reviews_url)
        
        # 没下载完先保存一下
        print("Scheduler.run商品评论下载完毕，index=" + str(index))
        review_info_list = []
        for url in all_review_url:
            # content = self.downloader.download(url, retry_count=2, headers=self.headers)
            content = requests.get(url, headers=self.headers, proxies=self.proxy_id,cookies=self.cookie)
            try:
                review_info_list.extend(self.parser.get_reviews_info(content))
            except BaseException as e:
                print("extend error:" + str(e))
            
        
        self.output.add_review_info("NO_" + str(index + 1), main_url, review_info_list)


if __name__ == '__main__':
    schedule = Scheduler()
    schedule.run()
    # schedule.run()
