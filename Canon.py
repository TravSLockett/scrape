import pandas as pd
from bs4 import BeautifulSoup
from lxml import html
from json import dump, loads
from requests import get
from pandas import ExcelWriter


def parseWalmart():

    review_list= []

    #making the connection to the URL
    url = 'https://shop.usa.canon.com/shop/en/catalog/eos-rebel-sl3-18-55-black-kit'
    response = get(url)
    #download the whole html doc.
    html_soup = BeautifulSoup(response.text, 'html.parser')

    #general information, getting the name, price and how many reviews there are
    Name = html_soup.find('span', itemprop = 'name').get_text()
    Price = html_soup.find('span', class_ = 'price final_price').get_text()
    #ReviewCount = html_soup.find('a', class_ = 'bv-rating-label bv-text-link bv-focusable')
    #print(ReviewCount)
    #review_url = 'https://www.walmart.com/reviews/product/350931600'
    #response = get(review_url)
    review_html = BeautifulSoup(response.text, 'html.parser')
    #get info about the review
    Reviews = review_html.find_all('li',  itemprop = 'review')
    idx = len(Reviews)
    print(idx)
    #print(Reviews)
    count = 0
    for Review in Reviews:
        count = count + 1
        print(count)
        ReviewAuthor = Review.find('span', class_ = 'bv-author').get_text()
        ReviewTime = Review.find('span', class_ = 'review-footer-submissionTime').get_text()
        RawReviewStar = Review.find_all('span', class_ = 'star display-inline-block star-rated')
        ReviewStar = len(RawReviewStar)
        #print(ReviewStar)
        raw_review_title = Review.find('h3', class_ ='review-title font-bold')
        if raw_review_title is None:
            ReviewTitle = " "
        else:
            ReviewTitle = Review.find('h3', class_ ='review-title font-bold').get_text()

        RawReviewContent = Review.find('div', class_ = 'collapsable-content-container')
        if RawReviewContent is None:
            ReviewContent = " "
        else:
            ReviewContent = Review.find('div', class_='collapsable-content-container').get_text()

        ReviewThumbsUp = Review.find('a', class_ ='width-full review-help-link thumbs-up s-margin-top').get_text()
        ReviewThumbsDown = Review.find('a', class_ ='width-full review-help-link thumbs-down s-margin-ends').get_text()
        raw_review_img = Review.find('img', class_ = 'review-media-thumbnail')
        if raw_review_img is None:
            ReviewImg = " "
        else:
            #ReviewImg = Review.find('img', class_ = 'review-media-thumbnail').get_text()
            ReviewImg = raw_review_img['src']
        review_dict = [
            ReviewAuthor, ReviewTime, ReviewStar,ReviewTitle,ReviewContent, ReviewThumbsUp, ReviewThumbsDown, ReviewImg
        ]

        review_list.append(review_dict)
    data = [
        Name, Price, review_list
    ]

    return data

def writeToExcel(data):
    df = pd.DataFrame(data[3])
    df.columns = ['Author','Date','Rating','Title','Content','ThumbsUp','ThumbsDown','posted pic?']
    writer = ExcelWriter(str(data[0])+'_WALMART_3_28_2020'+'.xlsx')
    df.to_excel(writer, 'Sheet1', index=False)
    writer.save()

def do():
    extracted_data = parseWalmart()
    #writeToExcel(extracted_data)

    f = open('dataCanon.json', 'w')
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