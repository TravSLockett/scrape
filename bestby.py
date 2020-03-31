import pandas as pd
from bs4 import BeautifulSoup
from lxml import html
from json import dump, loads
from requests import get
from pandas import ExcelWriter
from selenium import webdriver

def parseBestBy():

    review_list= []
    #driver = webdriver.Safari()
    #driver.get('https://www.bestbuy.com/site/canon-eos-rebel-sl3-dslr-camera-with-ef-s-18-55mm-is-stm-lens/6346259.p?skuId=6346259')
    #making the connection to the URL
    #url = 'https://shop.usa.canon.com/shop/en/catalog/eos-rebel-sl3-18-55-black-kit'
    #response = get(url)
    #response = driver.execute_script("return document.documentElement.outerHTML")
    #driver.quit()
    #html_soup = BeautifulSoup(response, 'html.parser')

    #general information, getting the name, price and how many reviews there are
    #Name = html_soup.find('h1', class_ = 'heading-5 v-fw-regular').get_text()
    #Price = html_soup.find('div', class_ = 'priceView-hero-price priceView-customer-price').get_text()
    #ReviewCount = html_soup.find('a', class_ = 'bv-rating-label bv-text-link bv-focusable')
    #print(ReviewCount)
    count = 0
    for n in range(11):
        review_url = 'https://www.bestbuy.com/site/reviews/beats-by-dr-dre-solo-pro-wireless-noise-cancelling-on-ear-headphones-black/6383116?variant=A&page='+str(n+1)
        driver = webdriver.Safari()
        driver.get(review_url)
        response = driver.execute_script("return document.documentElement.outerHTML")
        driver.quit()
        review_html = BeautifulSoup(response, 'html.parser')
        #get info about the review
        Reviews = review_html.find_all('li', class_ = 'review-item')
        idx = len(Reviews)
        print(idx)
        #print(Reviews)
        count = 0
        for Review in Reviews:
            count = count + 1
            #print(count)
            ReviewAuthor = Review.find('div', class_ = 'ugc-author v-fw-medium body-copy-lg').get_text()
            ReviewTime = Review.find('time', class_ = 'submission-date').get_text()
            ReviewStar = Review.find('p', class_ = 'sr-only').get_text()

            ReviewTitle = Review.find('h4', class_ ='review-title c-section-title heading-5 v-fw-medium').get_text()


            ReviewContent = Review.find('p', class_ = 'pre-white-space').get_text()

            ReviewThumbsUp = Review.find('button', class_ ='btn btn-outline btn-sm helpfulness-button no-margin-l').get_text()
            #ReviewThumbsUp = RawReviewThumbsUp.find('span', class_ ='bv-content-btn-count').get_text()

            ReviewThumbsDown = Review.find('button', class_ ='btn-default-link link neg-feedback').get_text()
            #ReviewThumbsDown = RawReviewThumbsDown.find('span', class_ ='bv-content-btn-count').get_text()

            raw_review_img = Review.find('ul', class_ = 'carousel gallery-preview')
            if raw_review_img is None:
                ReviewImg = "No"
            else:
                #ReviewImg = Review.find('img', class_ = 'review-media-thumbnail').get_text()
                ReviewImg = "Yes"
            #print(ReviewAuthor, ReviewTime, ReviewStar, ReviewTitle, ReviewContent, ReviewThumbsUp, ReviewThumbsDown, ReviewImg)
            #print(ReviewAuthor, ReviewTime, ReviewStar, ReviewTitle, ReviewContent, ReviewThumbsUp, ReviewThumbsDown, ReviewImg)
            review_dict = [
                ReviewAuthor, ReviewTime, ReviewStar,ReviewTitle,ReviewContent, ReviewThumbsUp, ReviewThumbsDown, ReviewImg
            ]

            review_list.append(review_dict)

        data = [
            review_list
        ]

    return data

def writeToExcel(data):
    df = pd.DataFrame(data[0])
    df.columns = ['Author','Date','Rating','Title','Content','ThumbsUp','ThumbsDown','posted pic?']
    writer = ExcelWriter('Beats by Dr. Dre - Solo Pro Wireless Noise Cancelling On-Ear Headphones - Black'+'_BESTBUY_3_31_2020'+'.xlsx')
    df.to_excel(writer, 'Sheet1', index=False)
    writer.save()

def do():
    extracted_data = parseBestBy()
    writeToExcel(extracted_data)

    f = open('dataBestBy.json', 'w')
    dump(extracted_data, f, indent=4)
    f.close()


if __name__ == '__main__':
    do()
#print(Price)
#print(ReviewCount)
#print(Name)
#print(ReviewAuthor)
#print(ReviewTitle)
#print(ReviewContent)
#print(ReviewTime)
#print(ReviewThumbsUp)
#print(Reviews)