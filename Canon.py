import pandas as pd
from bs4 import BeautifulSoup
from lxml import html
from json import dump, loads
from requests import get
from pandas import ExcelWriter
from selenium import webdriver

def parseWalmart():

    review_list= []
    driver = webdriver.Safari()
    driver.get('https://shop.usa.canon.com/shop/en/catalog/eos-rebel-sl3-18-55-black-kit')
    #making the connection to the URL
    #url = 'https://shop.usa.canon.com/shop/en/catalog/eos-rebel-sl3-18-55-black-kit'
    #response = get(url)
    response = driver.execute_script("return document.documentElement.outerHTML")
    driver.quit()
    html_soup = BeautifulSoup(response, 'html.parser')

    #general information, getting the name, price and how many reviews there are
    Name = html_soup.find('span', itemprop = 'name').get_text()
    Price = html_soup.find('span', class_ = 'price final_price').get_text()
    #ReviewCount = html_soup.find('a', class_ = 'bv-rating-label bv-text-link bv-focusable')
    #print(ReviewCount)
    #review_url = 'https://www.walmart.com/reviews/product/350931600'
    #response = get(review_url)
    review_html = BeautifulSoup(response, 'html.parser')
    #get info about the review
    Reviews = review_html.find_all('li', itemtype = 'http://schema.org/Review')
    idx = len(Reviews)
    print(idx)
    #print(Reviews)
    count = 0
    for Review in Reviews:
        count = count + 1
        #print(count)
        ReviewAuthor = Review.find('span', class_ = 'bv-author').get_text()
        ReviewTime = Review.find('span', class_ = 'bv-content-datetime-stamp').get_text().strip()
        ReviewStar = Review.find('span', class_ = 'bv-off-screen').get_text()


        ReviewTitle = Review.find('h3', class_ ='bv-content-title').get_text()

        ReviewContent = Review.find('div', class_ = 'bv-content-summary-body-text').get_text()


        RawReviewThumbsUp = Review.find('button', class_ ='bv-content-btn bv-content-btn-feedback-yes bv-focusable')
        ReviewThumbsUp = RawReviewThumbsUp.find('span', class_ ='bv-content-btn-count').get_text()

        RawReviewThumbsDown = Review.find('button', class_ ='bv-content-btn bv-content-btn-feedback-no bv-focusable')
        ReviewThumbsDown = RawReviewThumbsDown.find('span', class_ ='bv-content-btn-count').get_text()

        raw_review_img = Review.find('ul', class_ = 'bv-content-media-container')
        if raw_review_img is None:
            ReviewImg = "No"
        else:
            #ReviewImg = Review.find('img', class_ = 'review-media-thumbnail').get_text()
            ReviewImg = "Yes"
        print(Name)
        #print(ReviewAuthor, ReviewTime, ReviewStar, ReviewTitle, ReviewContent, ReviewThumbsUp, ReviewThumbsDown, ReviewImg)
        review_dict = [
            ReviewAuthor, ReviewTime, ReviewStar,ReviewTitle,ReviewContent, ReviewThumbsUp, ReviewThumbsDown, ReviewImg
        ]

        review_list.append(review_dict)
    data = [
        Name, Price, review_list
    ]

    return data

def writeToExcel(data):
    df = pd.DataFrame(data[2])
    df.columns = ['Author','Date','Rating','Title','Content','ThumbsUp','ThumbsDown','posted pic?']
    writer = ExcelWriter('EOS Rebel SL3 EF-S 18-55mm f4-5.6 IS STM Lens Kit Black'+'_CANON_3_28_2020'+'.xlsx')
    df.to_excel(writer, 'Sheet1', index=False)
    writer.save()

def do():
    extracted_data = parseWalmart()
    writeToExcel(extracted_data)

    #f = open('dataCanon.json', 'w')
    #dump(extracted_data, f, indent=4)
    #f.close()


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