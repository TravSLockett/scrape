from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import signal
from requests import get
from lxml import html
import plotly.graph_objects as go
import pandas as pd
import os
import csv
import openpyxl
from openpyxl import load_workbook


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


serviceN = ["Application UI", "SuiteCommerce - Websites", "SuiteCommerce - Checkout", "Asynchronous Services", "SuiteTalk", "SuiteAnswers", "Email", "SuiteAnalytics Connect"]
AUI = 0
SCW = 0
SCC = 0
AS = 0
ST = 0
SA = 0
E = 0
SC = 0

#--------------------------
#get today data from netsuite
browser = webdriver.Chrome(executable_path='/Users/Travishungry/nerd/scrape/chromedriver')
#browser = webdriver.Chrome()
browser.get('https://status.netsuite.com/#')
browser.maximize_window()
browser.implicitly_wait(60)


index = 2
while(index <= 11):
    soup_level1 = bs(browser.page_source, 'lxml')
    recentPosts = soup_level1.find("div", id = "recent-posts")
    if recentPosts.__len__() != 0 :
        posts = recentPosts.find_all("div", class_ = "post-day")
        for post in posts:
            timeParent = post.find("p", class_ = "timestamp")
            times = timeParent.find_all("span")
            idx = 0
            for timeC in times:
                if idx == 0:
                    start = ''.join(timeC.findAll(text=True)).strip()
                    print("start is " + start)
                elif idx == 1:
                    stop = ''.join(timeC.findAll(text=True)).split("-")[1].strip().split("(")[0].strip()
                    print("stop is " + stop)
                idx = idx + 1
            duraiton = conStr2Num(start, stop)
            AUI+=duraiton
            SCW+=duraiton
            SCC+=duraiton
            AS+=duraiton
            ST+=duraiton
            SA+=duraiton
            E+=duraiton
            SC+=duraiton
    # #click thru each one of the statuses
    #-----------------------------------
    # instancesTable = soup_level1.find('table', id ="weekly-status")
    # serviceParent = instancesTable.find("tbody")
    # services = serviceParent.find_all("tr")
    # row = 1
    # for service in services:
    #     col = 2
    #     statuses = service.find_all('td', class_ = 'status-cell')
    #     for status in statuses:
    #         error = status.find("svg", class_ = "icon icon-icon_messaging_available")
    #         print("-------")
    #         if error == None:
    #             browser.find_element_by_xpath(
    #                 '/html/body/div[2]/section[3]/table/tbody/tr[{}]/td[{}]/svg/use'.format(row,col)).click()
    #             print("it is not right here")
    #             browser.implicitly_wait(60)
    #             time.sleep(1)
    #         col = col + 1
    #     row = row + 1

    browser.execute_script("arguments[0].click();", WebDriverWait(browser, 20).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[3]/nav/ul/li[{}]/a'.format(index)))))
    index = index + 1
time.sleep(1)
#--------------
#get data from wayback machine
browser.get('https://web.archive.org/web/20200601000000*/https://status.netsuite.com/')
browser.implicitly_wait(60)
time.sleep(4)
soup_level1 = bs(browser.page_source, 'lxml')
browser.implicitly_wait(60)
time.sleep(2)
calendar = soup_level1.find("div", class_ = "calendar-grid")
browser.implicitly_wait(60)
time.sleep(4)
months = calendar.find_all("div", class_ = "month")
idx = 0
cc = 0

monCount = 1
for month in months:
    week = month.find_all("div", class_ = "month-week")
    weeCount = 1
    for day in week:
        dayE = day.find_all("div", {"class": ["month-day-container","month-blank-day-container"]})
        print("LENGTH " + str(dayE.__len__()))
        dayCount = 1
        for d in dayE:
            snap = d.find("div", class_ = "calendar-day")
            if snap != None:
                print(monCount, weeCount, dayCount)
                element = browser.find_element_by_xpath(
                    '/html/body/div[4]/div[4]/div[2]/div[{}]/div[2]/div[{}]/div[{}]/div'.format(monCount, weeCount, dayCount))
                action = ActionChains(browser);
                action.move_to_element(element).perform()
                browser.implicitly_wait(60)
                time.sleep(2)
                soup_level2 = bs(browser.page_source, 'lxml')
                popups = soup_level2.find("div", class_ = "popup-of-day-content")
                popup = popups.find_all("li")
                browser.implicitly_wait(60)
                time.sleep(2)

                #go to the page
                try:
                    print("Are there more than one snaps?")
                    browser.find_element_by_xpath('/html/body/div[4]/div[4]/div[3]/div/div[2]/ul/div/div/li/a').click()
                except NoSuchElementException as e:
                    print("There are more than one snap")
                    browser.find_element_by_xpath(
                        '/html/body/div[4]/div[4]/div[3]/div/div[2]/ul/div/div/li[1]/a').click()
                #go to the next page and wait forever
                browser.implicitly_wait(60)
                time.sleep(5)

                #try to get recent posts
                soup_level3 = bs(browser.page_source, 'lxml')
                recentPostsI = soup_level3.find("div", id="recent-posts")
                if recentPostsI.__len__() != 0:
                    postsI = recentPostsI.find_all("div", class_="post-day")
                    for postI in postsI:
                        timeParentI = postI.find("p", class_="timestamp")
                        timesI = timeParentI.find_all("span")
                        idxI = 0
                        for timeCI in timesI:
                            if idxI == 0:
                                startI = ''.join(timeCI.findAll(text=True)).strip()
                                print("start is " + start)
                            elif idxI == 1:
                                stopI = ''.join(timeCI.findAll(text=True)).split("-")[1].strip().split("(")[0].strip()
                                print("stop is " + stopI)
                            idxI = idxI + 1
                        duraitonI = conStr2Num(startI, stopI)
                        AUI += duraitonI
                        SCW += duraitonI
                        SCC += duraitonI
                        AS += duraitonI
                        ST += duraitonI
                        SA += duraitonI
                        E += duraitonI
                        SC += duraitonI

                browser.back()
                browser.implicitly_wait(60)
                time.sleep(3)

                cc+=1
            dayCount += 1
            idx = idx + 1
        weeCount += 1
    monCount += 1
print(idx)
print(cc)
print("-----")
print(AUI)
print(SCW)
print(SCC)
print(AS)
print(ST)
print(SA)
print(E)
print(SC)

browser.implicitly_wait(30)
browser.quit()

final = []
final.append("{0:.5g}".format((1 - (AUI / 8760))*100))
final.append("{0:.5g}".format((1 - (SCW / 8760))*100))
final.append("{0:.5g}".format((1 - (SCC / 8760))*100))
final.append("{0:.5g}".format((1 - (AS / 8760))*100))
final.append("{0:.5g}".format((1 - (ST / 8760))*100))
final.append("{0:.5g}".format((1 - (SA / 8760))*100))
final.append("{0:.5g}".format((1 - (E / 8760))*100))
final.append("{0:.5g}".format((1 - (SC / 8760))*100))

writer = pd.ExcelWriter('up_netsuite.xlsx', engine='openpyxl')
wb  = writer.book
df = pd.DataFrame({'Service Name': serviceN, "2020": final})
df.to_excel(writer, "2020")
wb.save('up_netsuite.xlsx')

#graph the table
fig = go.Figure(data=[go.Table(
    header=dict(values=['Service Name', '2020'],
                line_color='darkslategray',
                fill_color='lightskyblue',
                align='left'),
    cells=dict(values=[serviceN,final],
               line_color='darkslategray',
               fill_color='lightcyan',
               align='left'))
])

fig.show()