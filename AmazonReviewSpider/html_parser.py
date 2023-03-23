from lxml import etree

# from AmazonReviewSpider.baidu_trans import BaiduTrans
from baidu_trans import BaiduTrans

class HtmlParser(object):
    def __init__(self, base_url):
        self.amazon_base_url = base_url
        self.trans = BaiduTrans()

    # 从主页获取See all 73 positive reviews的url链接
    def parse_main_page_reviews_url(self, content):
        # content = str(content)
        content = content.text
        html = etree.HTML(content)
        # subject = html.xpath('//a[@id="dp-summary-see-all-reviews" and @class="a-link-emphasis"]') # subject
        # subject = html.xpath('//div//a[@class="a-link-normal"]') # subject
        # subject = html.xpath('//div[@id="customer_review-R3MNR85L9DMQJX"]')
        subject = html.xpath('//*[@id="reviews-medley-footer"]/div[2]/a')
        a_href = subject[0].get('href')

        return self.amazon_base_url + a_href

    def get_next_reviews_url(self, content):
        # content = str(content)
        content = content.text
        html = etree.HTML(content)
        subject = html.xpath('//li[@class="a-last"]/a')
        # 表示已经没有下一页
        if len(subject) == 0:
            return ""

        a_href = subject[0].get('href')
        return self.amazon_base_url + a_href

    def get_reviews_info(self, content):
        # content = str(content)
        content = content.text
        content = content.replace("<br>", "")
        content = content.replace("<br />", "")
        html = etree.HTML(content)

        star_list = html.xpath('//a/i[@data-hook="review-star-rating"]/span[@class="a-icon-alt"]/text()')
        # title_list = html.xpath('//div[@class="a-row"]/a[@data-hook="review-title"]/text()')
        title_list = html.xpath('//div[@class="a-row"]/a[@data-hook="review-title"]//text()[normalize-space()]')
        # profile_name_list = html.xpath('//div[@id="cm_cr-review_list"]//div[@class="a-profile-content"]/span[@class="a-profile-name"]/text()')
        # profile_name_list = html.xpath('//div[@id="cm_cr-review_list"]//div[@class="a-profile-content"]/span[@class="a-profile-name" and not(ancestor::div[@class="a-row a-spacing-mini review-data review-format-strip"])]/text()')
        profile_name_list = html.xpath('//div[@id="cm_cr-review_list"]//div[@class="a-profile-content"]/span[@class="a-profile-name" and not(ancestor::div[@class="a-row a-spacing-mini review-data review-format-strip"])]/text()')
        profile_name_list = list(set(profile_name_list))
        # review_body_list = html.xpath('//div[@class="a-row review-data"]/span['
        #                               '@data-hook="review-body"]/text()')
        # review_body_list = html.xpath('//div[@class="a-row a-spacing-small review-data"]')
        review_body_list = html.xpath('//span[@data-hook="review-body"]//text()[normalize-space()]')
        review_time_list = html.xpath('//span[@data-hook="review-date"]/text()')

        all_review_list = []
        for index in range(len(star_list)):
            star_num = star_list[index][:1]
            if int(star_num) < 0: # 只抓取4星以上
                continue
            # all_review_list.append(
            #     {"star": star_num, "title": title_list[index], "body": review_body_list[index],
            #      'trans': self.trans.transEn2Zh(review_body_list[index])})
            try:
                if index < len(title_list) and index < len(review_body_list):
                    all_review_list.append(
                        {"star": star_num, "title": title_list[index], "body": review_body_list[index], "time": review_time_list[index]
                        #  "profile_name":profile_name_list[index]
                        })
                else:
                    print("debug")
            except BaseException as e:
                print("问题在这")

        return all_review_list


if __name__ == '__main__':
    from html_downloader import Downloader
    downloader = Downloader()
    from url_manager import UrlManager

    parser = HtmlParser(UrlManager().get_amazon_base_url())
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36',
    # }

    # url = "https://www.amazon.co.uk/Transmission-Lullabies-Temperature-Monitoring-Discoball%C2%AE/product-reviews/B01HXPQUUI/ref=cm_cr_getr_d_paging_btm_12?ie=UTF8&pageNumber=12&reviewerType=all_reviews"
    # # url_final = "https://www.amazon.co.uk/Transmission-Lullabies-Temperature-Monitoring-Discoball%C2%AE/product-reviews/B01HXPQUUI/ref=cm_cr_getr_d_paging_btm_12?ie=UTF8&reviewerType=all_reviews&pageNumber=12";
    # content2 = downloader.download(url, retry_count=2, headers=headers).decode('utf8')
    # HtmlParser().get_reviews_info(content2)
    content = downloader.download('https://www.amazon.co.uk/Britax-Romer-Kidfix-SICT-Seat/dp/B016223NC6/ref=pd_rhf_dp_s_cp_3?_encoding=UTF8&pd_rd_i=B016223NC6&pd_rd_r=YWRA2FJ7QAEV45XJTBRT&pd_rd_w=VCHfZ&pd_rd_wg=IoH31&psc=1&refRID=YWRA2FJ7QAEV45XJTBRT', retry_count=2, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36',
        })
    url =parser.parse_main_page_reviews_url(content)
    star = '1.0 of 5'
    print(star[:1])
