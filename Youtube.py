import pandas as pd
from bs4 import BeautifulSoup
from lxml import html
from json import dump, loads
from requests import get
from pandas import ExcelWriter
import requests
from bs4 import BeautifulSoup as bs

def parseYoutube():
    # sample youtube video url
    video_url = "https://www.youtube.com/watch?v=k6nUX131lLY"
    # get the html content
    content = requests.get(video_url)
    # create bs object to parse HTML
    soup = bs(content.content, "html.parser")
    result = {}
    result['title'] = soup.find("span", attrs={"class": "watch-title"}).text.strip()
    result['views'] = int(soup.find("div", attrs={"class": "watch-view-count"}).text[:-6].replace(",", ""))
    result['description'] = soup.find("p", attrs={"id": "eow-description"}).text
    result['date_published'] = soup.find("strong", attrs={"class": "watch-time-text"}).text
    result['likes'] = int(soup.find("button", attrs={"title": "I like this"}).text.replace(",", ""))
    result['dislikes'] = int(soup.find("button", attrs={"title": "I dislike this"}).text.replace(",", ""))
    result['CommentNum'] = soup.find("h2", attrs={"class": "style-scope ytd-comments-header-renderer"})
    #print(result)

    # channel details
    channel_tag = soup.find("div", attrs={"class": "yt-user-info"}).find("a")
    # channel name
    channel_name = channel_tag.text
    # channel URL
    channel_url = f"https://www.youtube.com{channel_tag['href']}"
    # number of subscribers as str
    channel_subscribers = soup.find("span", attrs={"class": "yt-subscriber-count"}).text.strip()
    result['channel'] = {'name': channel_name, 'url': channel_url, 'subscribers': channel_subscribers}
    print(result)
    # write all HTML code into a file
    #open("video.html", "w", encoding='utf8').write(content.text)


def writeToExcel(data):
    df = pd.DataFrame(data[2])
    df.columns = ['Author','Date','Rating','Title','Content','ThumbsUp','ThumbsDown','posted pic?']
    writer = ExcelWriter('EOS Rebel SL3 EF-S 18-55mm f4-5.6 IS STM Lens Kit Black'+'_CANON_3_28_2020'+'.xlsx')
    df.to_excel(writer, 'Sheet1', index=False)
    writer.save()

def do():
    extracted_data = parseYoutube()
    #writeToExcel(extracted_data)

    #f = open('dataYoutube.json', 'w')
    #dump(extracted_data, f, indent=4)
    #f.close()


if __name__ == '__main__':
    do()