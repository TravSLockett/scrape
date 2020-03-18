
# -*- coding: utf-8 -*-

from lxml import html
from json import dump, loads
from requests import get
import pandas as pd
from pandas import ExcelWriter
import json
from re import sub
#from dateutil import parser as dateparser
from time import sleep



def ParseReviews():
    #GENRAL INFO
    gen_url = 'https://www.amazon.com/dp/B082MQFG76'
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
    #for i in range(5):
    response = get(gen_url, headers=headers, verify=False, timeout=30)
    if response.status_code == 404:
        return {"url": gen_url, "error": "page not found"}
    #if response.status_code != 200:
    #    continue

    # Removing the null bytes from the response.
    cleaned_response = response.text.replace('\x00', '')
    parser = html.fromstring(cleaned_response)

    XPATH_PRODUCT_NAME= '//span[@id="productTitle"]/text()'
    XPATH_PRODUCT_PRICE = '//span[@id="priceblock_ourprice"]/text()'
    #XPATH_PRODUCT_RATING = '//i[@class="a-icon a-icon-star a-star-4"]/text()'

    raw_product_price = parser.xpath(XPATH_PRODUCT_PRICE)
    raw_product_name = parser.xpath(XPATH_PRODUCT_NAME)
    #raw_product_rating = parser.xpath(XPATH_PRODUCT_RATING)

    product_price = ''.join(raw_product_price).replace(',', '')
    product_name = ''.join(raw_product_name).strip()


    #REVIEWS
    #ratings_dict = {}
    reviews_list = []
    for n in range(1):
        amazon_url ='https://www.amazon.com/GoPro-Silver-Elite-X-microSDHC-Adapter-UHS-I/product-reviews/B07XZK2S9C/ref=cm_cr_arp_d_paging_btm_next_'+str(n+1)+'?ie=UTF8&reviewerType=all_reviews&pageNumber='+str(n+1)

        # Add some recent user agent to prevent amazon from blocking the request
        # Find some chrome user agent strings  here https://udger.com/resources/ua-list/browser-detail?browser=Chrome
        headers = {
            'User-Agent':'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
            #'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
        #for i in range(5):
        response = get(amazon_url, headers=headers, verify=False, timeout=30)
        if response.status_code == 404:
            return {"url": amazon_url, "error": "page not found"}
        if response.status_code != 200:
            continue

        # Removing the null bytes from the response.
        cleaned_response = response.text.replace('\x00', '')

        parser = html.fromstring(cleaned_response)
        #XPATH_AGGREGATE = '//span[@id="acrCustomerReviewText"]'
        XPATH_REVIEW_SECTION_1 = '//div[contains(@id,"reviews-summary")]'
        XPATH_REVIEW_SECTION_2 = '//div[@data-hook="review"]'
        #XPATH_AGGREGATE_RATING = '//table[@id="histogramTable"]//tr'

        #total_ratings = parser.xpath(XPATH_AGGREGATE_RATING)
        reviews = parser.xpath(XPATH_REVIEW_SECTION_1)


        if not reviews:
            reviews = parser.xpath(XPATH_REVIEW_SECTION_2)

        # Grabing the rating  section in product page
        #for ratings in total_ratings:
        #    extracted_rating = ratings.xpath('./td//a//text()')
        #    if extracted_rating:
        #        rating_key = extracted_rating[0]
        #        raw_raing_value = extracted_rating[1]
        #        rating_value = raw_raing_value
        #        if rating_key:
        #            ratings_dict.update({rating_key: rating_value})



        # Parsing individual reviews
        for review in reviews:
            XPATH_RATING = './/i[@data-hook="review-star-rating"]//text()'
            XPATH_REVIEW_HEADER = './/a[@data-hook="review-title"]//text()'
            XPATH_REVIEW_POSTED_DATE = './/span[@data-hook="review-date"]//text()'
            XPATH_REVIEW_TEXT_1 = './/span[@data-hook="review-body"]//text()'
            XPATH_REVIEW_TEXT_2 = './/div//span[@data-action="columnbalancing-showfullreview"]/@data-columnbalancing-showfullreview'
            XPATH_AUTHOR = './/span[contains(@class,"profile-name")]//text()'
            XPATH_REVIEW_TEXT_3 = './/div[contains(@id,"dpReviews")]/div/text()'
            XPATH_REVIEW_VP = './/span[@data-hook="avp-badge"]//text()'
            XPATH_REVIEW_POSTEDPIC = './/img[@data-hook="review-image-tile"]/@src'
            XPATH_REVIEW_HELPFUL = './/span[@data-hook="helpful-vote-statement"]//text()'

            raw_review_author = review.xpath(XPATH_AUTHOR)
            raw_review_rating = review.xpath(XPATH_RATING)
            raw_review_header = review.xpath(XPATH_REVIEW_HEADER)
            raw_review_posted_date = review.xpath(XPATH_REVIEW_POSTED_DATE)
            raw_review_text1 = review.xpath(XPATH_REVIEW_TEXT_1)
            raw_review_text2 = review.xpath(XPATH_REVIEW_TEXT_2)
            raw_review_text3 = review.xpath(XPATH_REVIEW_TEXT_3)
            raw_review_vp = review.xpath(XPATH_REVIEW_VP)
            raw_review_posted_pic = review.xpath(XPATH_REVIEW_POSTEDPIC)
            raw_review_helpful = review.xpath(XPATH_REVIEW_HELPFUL)
            #raw_pic = review.xpath(XPATH_PIC)

            # Cleaning data
            author = ' '.join(' '.join(raw_review_author).split())
            review_rating = ''.join(raw_review_rating).replace('out of 5 stars', '')
            review_header = ' '.join(' '.join(raw_review_header).split())

            #try:
            #    review_posted_date = dateparser.parse(''.join(raw_review_posted_date)).strftime('%d %b %Y')
            #except:
            #    review_posted_date = None
            review_text = ' '.join(' '.join(raw_review_text1).split())

            # Grabbing hidden comments if present
            if raw_review_text2:
                json_loaded_review_data = loads(raw_review_text2[0])
                json_loaded_review_data_text = json_loaded_review_data['rest']
                cleaned_json_loaded_review_data_text = re.sub('<.*?>', '', json_loaded_review_data_text)
                full_review_text = review_text + cleaned_json_loaded_review_data_text
            else:
                full_review_text = review_text
            if not raw_review_text1:
                full_review_text = ' '.join(' '.join(raw_review_text3).split())

            review_dict = [
                author,
                raw_review_posted_date,
                 review_rating,
                review_header,
               full_review_text,
                raw_review_vp,
                raw_review_posted_pic,
                 raw_review_helpful
            ]
            reviews_list.append(review_dict)

        data = [
            product_name,
            product_price,
            reviews_list
        ]
    return data
    #return {"error": "failed to process the page", "url": amazon_url}

def writeToExcel(data):
    df = pd.DataFrame(data[2])
    df.columns = ['Author','Date','rating','header','text','verified?','posted pic','helpful?']
    writer = ExcelWriter(str(data[0])+'.xlsx')
    df.to_excel(writer, 'Sheet1', index=False)
    writer.save()



def parse():
    # Add your own ASINs here
    #AsinList = ['B07WHMQNPC']
    #review_printed = 0
    #extracted_data = []
    extracted_data = ParseReviews()
    #for asin in AsinList:
    #extracted_data.append(ParseReviews())
    sleep(5)

    f = open('amaData.json', 'w')
    dump(extracted_data, f, indent=4)
    f.close()

    #writeToExcel(extracted_data)



if __name__ == '__main__':
    parse()