from bs4 import BeautifulSoup
from lxml import html
from json import dump, loads
from requests import get
#import pandas as pd
#from pandas import ExcelWriter


def parseWalmart():

    review_list= []

    #making the connection to the URL
    url = 'https://www.walmart.com/ip/Beats-Studio3-Wireless-Over-Ear-Noise-Cancelling-Headphones-Matte-Black/56180487'
    response = get(url)
    #download the whole html doc.
    html_soup = BeautifulSoup(response.text, 'html.parser')

    #general information, getting the name, price and how many reviews there are
    Name = html_soup.find('h1', class_ = 'prod-ProductTitle font-normal').get_text()
    Price = html_soup.find('span', class_ = 'price-characteristic').get_text()
    ReviewCount = html_soup.find('span', class_ = 'stars-reviews-count-node').get_text()
    #ReviewTitle = html_soup.find('h3', class_='review-title font-bold').get_text()
    review_url = 'https://www.walmart.com/reviews/product/56180487'
    response = get(review_url)
    review_html = BeautifulSoup(response.text, 'html.parser')
    #get info about the review
    Reviews = review_html.find_all('div', class_ = 'Grid ReviewList-content')
    idx = len(Reviews)
    print(idx)
    #print(Reviews)
    count = 0
    for Review in Reviews:
        count = count + 1
        print(count)
        ReviewAuthor = Review.find('span', class_ = 'review-footer-userNickname').get_text()
        ReviewTime = Review.find('span', class_ = 'review-footer-submissionTime').get_text()
        raw_review_title = Review.find('h3', class_ ='review-title font-bold')
        if raw_review_title is None:
            ReviewTitle = " "
        else:
            ReviewTitle = Review.find('h3', class_ ='review-title font-bold').get_text()
        ReviewContent = Review.find('div', class_ = 'collapsable-content-container').get_text()
        ReviewThumbsUp = Review.find('a', class_ ='width-full review-help-link thumbs-up s-margin-top').get_text()
        ReviewThumbsDown = Review.find('a', class_ ='width-full review-help-link thumbs-down s-margin-ends').get_text()
        raw_review_img = Review.find('img', class_ = 'review-media-thumbnail')
        if raw_review_img is None:
            ReviewImg = " "
        else:
            ReviewImg = Review.find('img', class_ = 'review-media-thumbnail').get_text()
        #print(ReviewImg)
        print(ReviewTitle)
        review_dict = [
            ReviewAuthor, ReviewTime, ReviewTitle,ReviewContent, ReviewThumbsUp, ReviewThumbsDown, ReviewImg
        ]

        review_list.append(review_dict)
    data = [
        Name, Price, ReviewCount, review_list
    ]

    return data

def do():
    extracted_data = parseWalmart()
    f = open('dataWal.json', 'w')
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