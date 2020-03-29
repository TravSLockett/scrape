
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
    gen_url = 'https://www.bestbuy.com/site/beats-by-dr-dre-beats-studio-wireless-noise-cancelling-headphones-gray/6316142.p?skuId=6316142'
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

    XPATH_PRODUCT_NAME= './/h1[contains(@class,"heading-5 v-fw-regular")]'
    #XPATH_PRODUCT_PRICE = '//span[@id="priceblock_ourprice"]/text()'
    #XPATH_PRODUCT_RATING = '//i[@class="a-icon a-icon-star a-star-4"]/text()'

    #raw_product_price = parser.xpath(XPATH_PRODUCT_PRICE)
    raw_product_name = parser.xpath(XPATH_PRODUCT_NAME)
    #raw_product_rating = parser.xpath(XPATH_PRODUCT_RATING)

    #product_price = ''.join(raw_product_price).replace(',', '')
    #product_name = ''.join(raw_product_name).strip()

    print(raw_product_name)

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
    ParseReviews()
    #for asin in AsinList:
    #extracted_data.append(ParseReviews())
    #sleep(5)

    #f = open('amaData.json', 'w')
    #dump(extracted_data, f, indent=4)
    #f.close()

    #writeToExcel(extracted_data)



if __name__ == '__main__':
    parse()