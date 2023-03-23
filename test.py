import requests
from lxml import etree

# url = 'https://www.amazon.com/dp/B07VGRJDFY'
url = 'https://www.amazon.co.uk/Britax-Romer-Kidfix-SICT-Seat/dp/B016223NC6/ref=pd_rhf_dp_s_cp_3?_encoding=UTF8&pd_rd_i=B016223NC6&pd_rd_r=YWRA2FJ7QAEV45XJTBRT&pd_rd_w=VCHfZ&pd_rd_wg=IoH31&psc=1&refRID=YWRA2FJ7QAEV45XJTBRT'
head = {'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
proxy_id = { "http": "http://61.135.155.82:443"}
cookie = {'session-id':'459-4568418-5692641', 'ubid-acbcn':'459-5049899-3055220','x-wl-uid':'1AK7YMFc9IzusayDn2fT6Topjz3iAOpR3EeA2UQSqco8fo5PbK2aCpyBA/fdPMfKFqZRHc4IeyuU=','session-token':'"OH1wPvfOj6Tylq2nnJcdn5wyxycR/lqyGsGU3+lUtU4mbC0ZD9s8/4Oihd1BlskUQG8zRbLVs9vfWXuiJmnRlDT4x35ircp2uLxOLNYQ4j5pzdFJIqqoZUnhHSJUq2yK80P3LqH8An7faXRCPW9BIqX1wu0WmHlSS9vYAPKA/2SGdV9b//EljYjIVCBjOuR/dKRiYEeGK3li0RJOVz7+vMWg7Rnzbx89QxlbCp0WyquZyVxG6f2mNw=="','csm-hit':'tb:0J5M3DH92ZKHNKA0QBAF+b-0J5M3DH92ZKHNKA0QBAF|1544276572483&adb:adblk_no','session-id-time':'2082787201l'}

# r = requests.get(url,headers=head,proxies=proxy_id,cookies=cookie)

response = requests.get(url,headers=head,proxies=proxy_id,cookies=cookie)
html = etree.HTML(response.text)

reviews_url = html.xpath('//*[@id="reviews-medley-footer"]/div[2]/a/@href')

review_content = requests.get(reviews_url, headers=head, proxies=proxy_id,cookies=cookie)
# demo
content = content.text
content = content.replace("<br>", "")
content = content.replace("<br />", "")
html = etree.HTML(content)

star_list = html.xpath('//a/i[@data-hook="review-star-rating"]/span[@class="a-icon-alt"]/text()')
# title_list = html.xpath('//div[@class="a-row"]/a[@data-hook="review-title"]/text()')
title_list = html.xpath('//div[@class="a-row"]/a[@data-hook="review-title"]')
profile_name_list = html.xpath('//div[@class="a-profile-content"]/span[@class="a-profile-name"]/text()')
# 多一个
profile_name_list = profile_name_list[1:]

# review_body_list = html.xpath('//div[@class="a-row review-data"]/span['
#                               '@data-hook="review-body"]/text()')
# review_body_list = html.xpath('//div[@class="a-row a-spacing-small review-data"]')
review_body_list = html.xpath('//span[@data-hook="review-body"]')
