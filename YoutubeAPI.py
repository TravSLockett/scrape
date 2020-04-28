import json
from pytube import YouTube
import re
import urllib.request
import os, sys
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run_flow
from oauth2client.file import Storage
from pandas import ExcelWriter
import pandas as pd

def writeToExcel(data):
  df = pd.DataFrame(data[0])
  df.columns = ['Author', 'Date', 'Rating', 'Title', 'Content', 'ThumbsUp', 'ThumbsDown', 'posted pic?']
  writer = ExcelWriter(
    'Beats by Dr. Dre - Solo Pro Wireless Noise Cancelling On-Ear Headphones - Black' + '_BESTBUY_3_31_2020' + '.xlsx')
  df.to_excel(writer, 'Sheet1', index=False)
  writer.save()


#get the captions
def disable_stout():
  o_stdout = sys.stdout
  o_file = open(os.devnull, 'w')
  sys.stdout = o_file
  return (o_stdout, o_file)


def enable_stout(o_stdout, o_file):
  o_file.close()
  sys.stdout = o_stdout


def get_oauth2_token():
  CLIENT_ID = '127161119291-49j8geg0itp7ua0qetib4au9me92385k.apps.googleusercontent.com'
  CLIENT_SECRET = 'l9VbhWnUPlAdH20eq_seYwXG'
  SCOPE = 'https://www.googleapis.com/auth/youtube'
  REDIRECT_URI = 'http://localhost:8080/'

  o_stdout, o_file = disable_stout()

  flow = OAuth2WebServerFlow(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    scope=SCOPE,
    redirect_uri=REDIRECT_URI)

  storage = Storage('creds.data')
  credentials = run_flow(flow, storage)
  enable_stout(o_stdout, o_file)

  oauthToken = credentials.access_token
  print(oauthToken)

api_key = "AIzaSyAMnFSuK_tdF6Ra6zDNKqS_MDCwzTRnV5s"

#test the url
#video_id = "Z_EltoprrY0"
#url = f"https://www.googleapis.com/youtube/v3/captions/ahHP85spCHfrQTzC_9JoE1raar6W6a8_iUPrpP8tVKk=?key=ya29.a0Ae4lvC0P8u9xo5cpz8vlvQ5C9hANqu_AEK07XQUO90ix109gbNO-aeN0npZxCG22dgcg8vQFlx_BRRkYPRPvzl9hidjyHGHIpHfYC2xv-GENxrmtDum3YR5Tov1hl1VDi1h4MJQG_JSbHmyfKSbJ-GdfCMm8K3UjAog"
#json_url = urllib.request.urlopen(url)
#data = json.loads(json_url.read())
#print(data)



#for parsing the strings
class RG:
  def __init__(self):
    pass
  def no_space(self, title: str):
    title = re.sub('[\W_]+', "_", title)
    return title.lower()
  def get_id(self, url: str):
    return url.rsplit("=",1)[1]
  def time(self, timeStamp: str ):
    return timeStamp.rsplit("T",1)[0]
#getting the data from snippet
class YouTubeStatsSni:
  def __init__(self, url:str):
    self.json_url = urllib.request.urlopen(url)
    self.data = json.loads(self.json_url.read())
  def print(self):
    print(self.data)
  def get_video_title(self):
    return self.data["items"][0]["snippet"]["title"]
  def get_video_des(self):
    return self.data["items"][0]["snippet"]["description"]
    #return self.data["items"][0]["channelTitle"]
  def download_video(self,youtube_url: str, title: str):
    YouTube(youtube_url).streams.first().download(filename=title)
  def get_date(self):
    return self.data["items"][0]["snippet"]["publishedAt"]
  def get_channel(self):
    return self.data["items"][0]["snippet"]["channelTitle"]
  def get_channelId(self):
    return self.data["items"][0]["snippet"]["channelId"]


#getting the data from the statistics
class YouTubeStatsSta:
  def __init__(self, url:str):
    self.json_url = urllib.request.urlopen(url)
    self.data = json.loads(self.json_url.read())
  def print(self):
    print(self.data)
  def get_likes(self):
    return self.data["items"][0]["statistics"]["likeCount"]
  def get_dislikes(self):
    return self.data["items"][0]["statistics"]["dislikeCount"]
  def get_comment(self):
    return self.data["items"][0]["statistics"]["commentCount"]
  def get_views(self):
    return self.data["items"][0]["statistics"]["viewCount"]

class YouTubeCha:
  def __init__(self, url: str):
    self.json_url = urllib.request.urlopen(url)
    self.data = json.loads(self.json_url.read())
  def print(self):
    print(self.data)
  def get_subs(self):
    return self.data["items"][0]["statistics"]["subscriberCount"]

link_file = "something.csv"
with open(link_file, "r") as f:
  content = f.readlines()

content = list(map(lambda s: s.strip(), content))
#content = list (map(lambda s: s.strip(','), content))

regular = RG()
for url in content:
  video_id = regular.get_id(url)
  urlSni = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"
  urlSta = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={api_key}"
  #get channel ID
  yt_statsChaID = YouTubeStatsSni(urlSni)
  channelID = yt_statsChaID.get_channelId()

  urlCha = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channelID}&key={api_key}"
  yt_statsSubs = YouTubeCha(urlCha)
  channelSubs = yt_statsSubs.get_subs()

  yt_statsSni = YouTubeStatsSni(urlSni)
  yt_statsSta = YouTubeStatsSta(urlSta)

  #get title
  title = yt_statsSni.get_video_title()
  title = regular.no_space(title)
  #download video
  #yt_statsSni.download_video(url,title)
  #get the date of publication
  date = yt_statsSni.get_date()
  date = regular.time(date)
  #get description
  description = yt_statsSni.get_video_des()
  #get channel name
  channel = yt_statsSni.get_channel()
  #get likes and dislikes
  likes = yt_statsSta.get_likes()
  dislikes = yt_statsSta.get_dislikes()
  #get number of comments
  commentCount = yt_statsSta.get_comment()
  #get number of views
  views = yt_statsSta.get_views()


  print("title:",title)
  print("date:",date)
  print("description: ",description)
  print("Likes: ",likes)
  print("Dislikes:",dislikes)
  print("Num of Comments: ", commentCount)
  print("Num of views:",views)
  print("Channel: ",channel)
  print("channel subs: ", channelSubs)



#get_oauth2_token()

