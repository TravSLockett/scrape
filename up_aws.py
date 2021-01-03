from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs
from requests import get
from lxml import html
import plotly.graph_objects as go
import pandas as pd
import os
import csv
import openpyxl
from openpyxl import load_workbook



#convertion function
def conStr2Num(start, stop):
    #convert AM and PM to numbers
    start_min = 0
    stop_min = 0
    #AM to minutes
    if "PM" in start:
        #for case like 12:01 pm, so that it does not add 12 + 12
        if int(start.split("PM")[0].strip().split(":")[0]) == 12:
            start_min = 12 * 60 + int(start.split("PM")[0].strip().split(":")[1])
        else:
            start_min = (int(start.split("PM")[0].strip().split(":")[0]) + 12)* 60 + int(start.split("PM")[0].strip().split(":")[1])
    elif "AM" in start:
        if int(start.split("AM")[0].strip().split(":")[0]) == 12:
            start_min = int(start.split("AM")[0].strip().split(":")[1])
        else:
            start_min =  (int(start.split("AM")[0].strip().split(":")[0]) )* 60 + int(start.split("AM")[0].strip().split(":")[1])


    #in the case that it goes over to the next day
    if stop[0].isnumeric():
        if "PM" in stop:
            stop_min = (int(stop.split("PM")[0].strip().split(":")[0]) + 12) * 60 + int(stop.split("PM")[0].strip().split(":")[1])
        elif "AM" in stop:
            stop_min = (int(stop.split("AM")[0].strip().split(":")[0])) * 60 + int(stop.split("AM")[0].strip().split(":")[1])

        duration = stop_min - start_min
        if duration  >= 0:
            print(duration)
            return duration
        else:
            print("DURATION IS NOT RIGHT")
    else:

        first_duration = 23 * 60 + 59 - start_min
        second_duration = 0
        nextdaytime = stop.split(",")[1].strip()
        if "AM" in nextdaytime:
            if int(nextdaytime.split("AM")[0].strip().split(":")[0]) == 12:
                second_duration = int(nextdaytime.split("AM")[0].strip().split(":")[1])
            else:
                second_duration =int(nextdaytime.split("AM")[0].strip().split(":")[0]) * 60 +int(nextdaytime.split("AM")[0].strip().split(":")[1])
        elif "PM" in nextdaytime:
            if int(nextdaytime.split("PM")[0].strip().split(":")[0]) == 12:
                second_duration = 12 * 60 + int(nextdaytime.split("PM")[0].strip().split(":")[1])
            else:
                second_duration =(int(nextdaytime.split("PM")[0].strip().split(":")[0]) + 12) * 60 +int(nextdaytime.split("PM")[0].strip().split(":")[1])
        duration = first_duration + second_duration

        if duration > 0:
            print(duration)
            return  duration
        else:
            print(duration)
            print("SOMETHING NOT RIGHT ")


#open the website
browser = webdriver.Chrome(executable_path='/Users/Travishungry/nerd/scrape/chromedriver')
#browser = webdriver.Chrome()
browser.get('https://status.aws.amazon.com/')
browser.maximize_window()
browser.implicitly_wait(30)


#Middle East
browser.find_element_by_xpath('/html/body/div[2]/div[5]/ul/li[6]/div/a').click()
# #Asia Pacific
# browser.find_element_by_xpath('/html/body/div[2]/div[5]/ul/li[5]/div/a').click()
# #Africa
# browser.find_element_by_xpath('/html/body/div[2]/div[5]/ul/li[4]/div/a').click()
# #EU
# browser.find_element_by_xpath('/html/body/div[2]/div[5]/ul/li[3]/div/a').click()
# #LATAM
# browser.find_element_by_xpath('/html/body/div[2]/div[5]/ul/li[2]/div/a').click()


browser.implicitly_wait(30)
#get all the services name
soup_level1 = bs(browser.page_source, 'lxml')


#Middle East
nameCol = soup_level1.find('table', id="MEstatusHistoryContentLeft" )
# #Asia Pacific
# nameCol = soup_level1.find('table', id="APstatusHistoryContentLeft" )
# #Africa
# nameCol = soup_level1.find('table', id="AFstatusHistoryContentLeft" )
# #EU
# nameCol = soup_level1.find('table', id="EUstatusHistoryContentLeft" )
# #NoAM
# nameCol = soup_level1.find('table', id="NAstatusHistoryContentLeft" )
# #LATAM
# nameCol = soup_level1.find('table', id="SAstatusHistoryContentLeft" )

names = nameCol.find_all("tr")
print(names.__len__())

serviceN =[]
data20 = [0] * names.__len__()


#clean the name string and add to serviceN set
for name in names:
    cleanedName = " ".join(name.text.replace('\n', '').split())
    length =cleanedName.__len__()
    serviceN.append(cleanedName)
#-----------------------
#click thru the pages
#51
for x in range(51):
    # get however many rows first
    soup_level1 = bs(browser.page_source, 'lxml')
    #ME
    statusParent = soup_level1.find('div', id = 'MEstatusHistoryContentParent')
    # #AP
    # statusParent = soup_level1.find('div', id = 'APstatusHistoryContentParent')
    # #AF
    # statusParent = soup_level1.find('div', id = 'AFstatusHistoryContentParent')
    # #EU
    # statusParent = soup_level1.find('div', id = 'EUstatusHistoryContentParent')
    # #NA
    # statusParent = soup_level1.find('div', id = 'NAstatusHistoryContentParent')
    # #LATAM
    # statusParent = soup_level1.find('div', id = 'SAstatusHistoryContentParent')
    statusGroup = statusParent.find('table', class_ = "statusHistory statusHistoryContent")
    statusRows = statusGroup.find_all('tr')
    #print(statusRows.__len__())
    index = 0
    for row in statusRows:
        items = row.find_all('td')
        for item in items:
            print(item)
            start = ''
            stop = ''
            #check each td length
            #if more than one, check the first element to see if first image is status3
            span = item.find_all("span")
            print(span.__len__())
            if span.__len__() > 1:
                print("down time down time")
                c = 0
                for i in span:
                    if c == 0:
                        status = i.find('img')
                        print("the string status is " + str(status))
                    #get the event data
                    #get the start
                    if c >= 2:
                        if c == 2:
                            #check if the 3rd one is the note or not
                            #if it is a letter, skip to next one
                            if i.text.strip()[0].isnumeric():
                                start =i.text.strip().split("PST")[0]
                        #the first one is the note, add the start time on this round
                        if c == 3 and start == '' :
                            start = i.text.strip().split("PST")[0]

                        #get the stop time
                        if c == span.__len__() - 1:
                            stop = i.text.strip().split("PST")[0]
                    c = c + 1
            #finished grabbing the start time and end time, convert into number and put into list
            if start != '' and stop != '':
                print(start)
                print(stop)
                duration_hour = conStr2Num(start, stop) / 60
                data20[index] = data20[index] + duration_hour

        index = index + 1

    #flipping pages
    # #norAM
    # browser.find_element_by_xpath('/html/body/div[2]/div[5]/div/div[1]/table/tbody/tr/td[3]/table/tbody/tr[1]/th/a').click()
    # #LATAM
    # browser.find_element_by_xpath('/html/body/div[2]/div[5]/div/div[2]/table/tbody/tr/td[3]/table/tbody/tr[1]/th/a').click()
    # #EU
    # browser.find_element_by_xpath('/html/body/div[2]/div[5]/div/div[3]/table/tbody/tr/td[3]/table/tbody/tr[1]/th/a').click()
    # #Africa
    # browser.find_element_by_xpath('/html/body/div[2]/div[5]/div/div[4]/table/tbody/tr/td[3]/table/tbody/tr[1]/th/a').click()
    # #Asia Pacific
    # browser.find_element_by_xpath('/html/body/div[2]/div[5]/div/div[5]/table/tbody/tr/td[3]/table/tbody/tr[1]/th/a').click()
    #Middle East
    browser.find_element_by_xpath('/html/body/div[2]/div[5]/div/div[6]/table/tbody/tr/td[3]/table/tbody/tr[1]/th/a').click()
    time.sleep(0.5)

idx = 0
#convert data into score
final = []
ii = data20.__len__()
for service in data20:
    if idx == 0:
        final.append('')
    elif idx < ii:
        final.append("{0:.5g}".format((1 - (service / 8760))*100))
    idx = idx + 1
print(final)
print(final.__len__())
print(serviceN)
print(serviceN.__len__())

#write the data to excel
writer = pd.ExcelWriter('up_aws_me.xlsx', engine='openpyxl')
wb  = writer.book
df = pd.DataFrame({'Service Name': serviceN,
                  '2020': final})
df.to_excel(writer, "Middle East")
wb.save('up_aws_me.xlsx')


#graph the table
fig = go.Figure(data=[go.Table(
    header=dict(values=['Service Name', '2020'],
                line_color='darkslategray',
                fill_color='lightskyblue',
                align='left'),
    cells=dict(values=[serviceN, # 1st column
                       final], # 2nd column
               line_color='darkslategray',
               fill_color='lightcyan',
               align='left'))
])

fig.show()


browser.implicitly_wait(30)
browser.quit()
