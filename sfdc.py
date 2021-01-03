from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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




#5 hours, 34 minutes
#1 day, 3 hours, 34 minutes
def convert(duration):
    total = 0
    minute = 0
    hour_minute = 0
    day_minute = 0
    rest_min = ''
    rest_hour = ''

    #handle day
    if "days" in duration:
        day_minute = int(duration.split(",")[0].strip().split("days")[0].strip()) * 1440
        #if its day, hour, min
        if duration.split(",").__len__() > 2:
            rest_hour = duration.split(",")[1].strip()
            rest_min = duration.split(",")[2].strip()
        #if it is day, hour
        elif duration.split(",").__len__() == 2:
            rest_hour = duration.split(",")[1].strip()

    elif "day" in duration:
        day_minute = int(duration.split(",")[0].strip().split("day")[0].strip()) * 1440
        # if its day, hour, min
        if duration.split(",").__len__() > 2:
            rest_hour = duration.split(",")[1].strip()
            rest_min = duration.split(",")[2].strip()
        # if it is day, hour
        elif duration.split(",").__len__() == 2:
            rest_hour = duration.split(",")[1].strip()

    #handle hour
    if "hours" in duration:
        #day, hour or day, hour, min
        if rest_hour != '':
            hour_minute = int(rest_hour.split("hours")[0].strip()) * 60
        #hour or hour, min
        else:
            #hour, min
            if duration.split(",").__len__() > 1:
                hour_minute = int(duration.split(",")[0].strip().split("hours")[0].strip()) * 60
                rest_min = duration.split(",")[1].strip()
            #hour
            elif duration.split(",").__len__() == 1:
                hour_minute = int(duration.split("hours")[0].strip()) * 60

    elif "hour" in duration:
        # day, hour or day, hour, min
        if rest_hour != '':
            hour_minute = int(rest_hour.split("hour")[0].strip()) * 60
        # hour or hour, min
        else:
            #hour, min
            if duration.split(",").__len__() > 1:
                hour_minute = int(duration.split(",")[0].strip().split("hour")[0].strip()) * 60
                rest_min = duration.split(",")[1].strip()
            #hour
            elif duration.split(",").__len__() == 1:
                hour_minute = int(duration.split("hour")[0].strip()) * 60


    if "minutes" in duration:
        if rest_min != '':
            minute = int(rest_min.split("minutes")[0].strip())
        else:
            minute = int(duration.split("minutes")[0].strip())
    elif "minute" in duration:
        # get rid of minute and get the minutes
        if rest_min != '':
            minute = int(rest_min.split("minute")[0].strip())
        else:
            minute = int(duration.split("minute")[0].strip())

    #add them together
    total = hour_minute + minute + day_minute
    if total > 0:
        print("the total is "+ str(total))
        return total
    else:
        print("THE VALUE IS NOT RIGHT")




#open the website
browser = webdriver.Chrome(executable_path='/Users/Travishungry/nerd/scrape/chromedriver')
#browser = webdriver.Chrome()
browser.get('https://status.salesforce.com/products/Salesforce_Services')
browser.maximize_window()
browser.implicitly_wait(60)


#choose America
browser.execute_script("arguments[0].click();", WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/div/div[2]/div/div/div/div/div[2]/div[1]/div/div[1]/div[1]/div/label[1]/input'))))
# #EMEA
# browser.execute_script("arguments[0].click();", WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/div/div[2]/div/div/div/div/div[2]/div[1]/div/div[1]/div[1]/div/label[2]/input'))))
# #AP
# browser.execute_script("arguments[0].click();", WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div/div/div[2]/div[1]/div/div[1]/div[1]/div/label[3]/input'))))
browser.implicitly_wait(60)

#get how many instances to click on
soup_level1 = bs(browser.page_source, 'lxml')
instancesParent = soup_level1.find('div', class_="sc-ikXwZx hwCNyq" )
browser.implicitly_wait(60)
time.sleep(1)
instances = instancesParent.find_all('span', class_='sc-uxeQQ jHEhAp')
print("Instances amount: "+ str(instances.__len__()))

col =[]
core_Service_arr =[]
search_arr = []
analytics_arr = []
live_Agent_arr = []
cpqb_arr = []
einstein_Bots_arr = []
communities_arr = []
c3a_arr = []
core_Service = 0
search = 0
analytics = 0
live_Agent = 0
cpqb = 0
einstein_Bots = 0
communities = 0
c3a = 0


instanceNum = 1
#go to each instance
for instance in instances:
    core_Service_cur = 0
    search_cur = 0
    analytics_cur = 0
    live_Agent_cur = 0
    cpqb_cur = 0
    einstein_Bots_cur = 0
    communities_cur = 0
    c3a_cur = 0
    #add to the name col
    nameLabel =instance.find('label', class_ = "sc-WZYaI hciJwR")
    name = nameLabel.find('span').text
    #add to all the instances names coloum
    col.append(str(name))

    #go to the instance
    browser.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div/div/div/div/div[2]/div[1]/div/div[2]/span[{}]/a'.format(instanceNum)).click()
    browser.implicitly_wait(10)
    time.sleep(0.5)

    #hit history tab
    browser.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div[1]/ul/li[2]/a').click()
    browser.implicitly_wait(10)
    time.sleep(0.5)

    # hit 7 days tab
    browser.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[1]/div/div[1]/button[1]').click()
    browser.implicitly_wait(10)
    time.sleep(0.5)


    for i in range(4):
        #check this page

        # grab all lines
        soup_level1 = bs(browser.page_source, 'lxml')
        lineParent = soup_level1.find_all('div', class_='slds-col slds-size--1-of-1')
        nameInstanceP = soup_level1.find('div', class_ = 'sc-cVJhCs emwOlS')
        nameI = nameInstanceP.find('span').text
        print(str(nameI) + " instance's number of services is " + str(lineParent.__len__()))
        curName = ''
        lineIdx = 3
        for line in lineParent:
            # find if there are any incidents in this particular time line
            incidents = line.find_all('div', class_='timeline-row-item')
            print(incidents.__len__())
            if incidents.__len__() != 0:
                # get the current service name
                serviceName = line.find('div', class_='slds-col timeline-row-label')
                curName = serviceName.find('span').text

                # grab each incident on this line
                totalDurations = 0
                incidentIdx = 3
                for incident in incidents:
                    #check if it is a real incident or not
                    svg = incident.find('svg', class_ = 'slds-icon slds-icon--small')
                    if svg != None:
                        print("line index is " + str(lineIdx))
                        print("incident index is " + str(incidentIdx))
                        # click on the incident
                        browser.execute_script("arguments[0].click();", WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div[{}]/div/div[1]/div/div[{}]/div[2]'.format(lineIdx, incidentIdx)))))
                        # browser.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div[{}]/div/div[1]/div/div[{}]/div[2]'.format(lineIdx, incidentIdx)).click()
                        browser.implicitly_wait(20)
                        time.sleep(2)

                        # grab the info off the pop up
                        soup_level1 = bs(browser.page_source, 'lxml')
                        browser.implicitly_wait(20)
                        time.sleep(1)

                        sections = soup_level1.find('div', class_ = "slds-col slds-size_1-of-3 slds-p-left--medium slds-border_left")
                        print("Section is "+ str(sections))
                        #for maintainance
                        if sections == None:
                            print("It was none")
                            sections = soup_level1.find('div',class_="sc-jLMuHf eLztnl")
                            print("The new sections is "+ str(sections))
                            browser.implicitly_wait(20)
                            time.sleep(2)
                        browser.implicitly_wait(20)
                        time.sleep(2)
                        count = 0
                        for section in sections:
                            if count == 2:
                                durationParent = section.find('p')
                                # for maintainance
                                if durationParent != None:
                                    duration = durationParent.text
                                    totalDurations = totalDurations + convert(duration)
                                else:
                                    durationParent = section.find('div', class_="sc-ddviEe lidJGG")
                                    duration = durationParent.text
                                    totalDurations = totalDurations + convert(duration)
                            count = count + 1

                        # click cancel to exist the incident window
                        try:
                            print("trying the regular way to exit the window")
                            browser.find_element_by_xpath('/html/body/div[4]/div/div/section/div/header/button').click()
                        except NoSuchElementException as e:
                            print("the regular cancel button did not work")
                            browser.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div[2]/div[2]/div[1]/span').click()


                        browser.implicitly_wait(10)
                        time.sleep(2)

                        incidentIdx = incidentIdx + 1

                # check what service this is and add to that service
                if totalDurations > 0:
                    if curName == "Core Service":
                        core_Service = core_Service + totalDurations
                        core_Service_cur = core_Service_cur + totalDurations
                    elif curName == "Search":
                        search = search + totalDurations
                        search_cur = search_cur + totalDurations
                    elif curName == "Analytics":
                        analytics = analytics + totalDurations
                        analytics_cur = analytics_cur + totalDurations
                    elif curName == "Live Agent":
                        live_Agent = live_Agent + totalDurations
                        live_Agent_cur = live_Agent_cur + totalDurations
                    elif curName == "CPQ and Billing":
                        cpqb = cpqb + totalDurations
                        cpqb_cur = cpqb_cur + totalDurations
                    elif curName == "Einstein Bots":
                        einstein_Bots = einstein_Bots + totalDurations
                    elif curName == "Communities":
                        communities = communities + totalDurations
                        communities_cur = communities_cur + totalDurations
                    elif curName == "Customer 360 Audiences":
                        c3a = c3a + totalDurations
                        c3a_cur = c3a_cur + totalDurations
                    else:
                        print("THIS IS A SERVICE THAT IS NOT RECOGNIZED")
            lineIdx = lineIdx + 1
        #hit backward
        browser.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div[2]/button[1]').click()
        browser.implicitly_wait(10)
        time.sleep(1)
    #update each service row
    core_Service_arr.append(core_Service_cur)
    search_arr.append(search_cur)
    analytics_arr.append(analytics_cur)
    live_Agent_arr.append(live_Agent_cur)
    cpqb_arr.append(cpqb_cur)
    einstein_Bots_arr.append(einstein_Bots_cur)
    communities_arr.append(communities_cur)
    c3a_arr.append(c3a_cur)

    print(col)
    print(core_Service_arr)
    print(search_arr)
    print(analytics_arr)
    print(live_Agent_arr)
    print(cpqb_arr)
    print(einstein_Bots_arr)
    print(communities_arr)
    print(c3a_arr)

    #go back last level procedure
    browser.get('https://status.salesforce.com/products/Salesforce_Services')
    browser.implicitly_wait(10)
    time.sleep(0.5)
    #America
    browser.execute_script("arguments[0].click();", WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div/div/div[2]/div[1]/div/div[1]/div[1]/div/label[1]/input'))))
    # #EMEA
    # browser.execute_script("arguments[0].click();", WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div/div/div[2]/div[1]/div/div[1]/div[1]/div/label[2]/input'))))
    # #AP
    # browser.execute_script("arguments[0].click();", WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div/div/div[2]/div[1]/div/div[1]/div[1]/div/label[3]/input'))))

    browser.implicitly_wait(10)
    time.sleep(0.5)
    instanceNum = instanceNum + 1

#convert data into uptime score
core_Service_arrF =[]
search_arrF = []
analytics_arrF = []
live_Agent_arrF = []
cpqb_arrF = []
einstein_Bots_arrF = []
communities_arrF = []
c3a_arrF = []


for i in range(col.__len__()):
    core_Service_arrF.append("{0:.5g}".format((1 - (core_Service_arr[i] / 8760))*100))
    search_arrF.append("{0:.5g}".format((1 - (search_arr[i] / 8760)) * 100))
    analytics_arrF.append("{0:.5g}".format((1 - (analytics_arr[i] / 8760)) * 100))
    live_Agent_arrF.append("{0:.5g}".format((1 - (live_Agent_arr[i] / 8760)) * 100))
    cpqb_arrF.append("{0:.5g}".format((1 - (cpqb_arr[i] / 8760)) * 100))
    einstein_Bots_arrF.append("{0:.5g}".format((1 - (einstein_Bots_arr[i] / 8760)) * 100))
    communities_arrF.append("{0:.5g}".format((1 - (communities_arr[i] / 8760)) * 100))
    c3a_arrF.append("{0:.5g}".format((1 - (c3a_arr[i] / 8760)) * 100))

#write the data to excel
writer = pd.ExcelWriter('up_sfdc_a.xlsx', engine='openpyxl')
wb  = writer.book
df = pd.DataFrame({'Service Name': col,
                  'Core Service': core_Service_arrF,'Search': search_arrF, "Analytics": analytics_arrF, "Live Agen": live_Agent_arrF, "CPQ and Billing": cpqb_arrF, "Einstein Bots": einstein_Bots_arrF, "Communities": communities_arrF, "Customer 360 Audiences": c3a_arrF})
df.to_excel(writer, "America")
wb.save('up_sfdc_a.xlsx')

#graph the table
fig = go.Figure(data=[go.Table(
    header=dict(values=['Instance Name', 'Core Service', 'Search', 'Analytics', 'Live Agent', 'CPQ and Billing', 'Einstein Bots', 'Communities', 'Customer 360 Audiences'],
                line_color='darkslategray',
                fill_color='lightskyblue',
                align='left'),
    cells=dict(values=[col,
                       core_Service_arrF,search_arrF, analytics_arrF, live_Agent_arrF, cpqb_arrF, einstein_Bots_arrF, communities_arrF, c3a_arrF ],
               line_color='darkslategray',
               fill_color='lightcyan',
               align='left'))
])

fig.show()

browser.implicitly_wait(30)
browser.quit()


#if there are 2 items
#div 3 and div 4



# /html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div[1]
# /html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div[2]
#first line
# /html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div[3]/div/div[1]/div/div[1]
# /html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div[3]/div/div[1]/div/div[2]
# /html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div[3]/div/div[1]/div/div[3]/div[2]
# /html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div[3]/div/div[1]/div/div[4]/div[2]

# NA107
# /html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div[3]/div/div[1]/div/div[3]/div[2]
# /html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div[3]/div/div[1]/div/div[4]/div[2]

#second line
# /html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div[4]/div/div[1]/div/div[1]
# /html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div[4]/div/div[1]/div/div[2]
#thrid line
# /html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div[5]/div/div[1]/div/div[1]
# /html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div[5]/div/div[1]/div/div[2]

#if there are 1 item
# /html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div[3]/div/div[1]/div/div[3]/div[2]





#############

# #testing testing
# browser.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div/div/div/div/div[2]/div[1]/div/div[2]/span[265]/a').click()
# browser.implicitly_wait(10)
# time.sleep(0.5)
#
# #hit history tab
# browser.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div[1]/ul/li[2]/a').click()
# browser.implicitly_wait(10)
# time.sleep(0.5)
#
# # hit 7 days tab
# browser.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[1]/div/div[1]/button[1]').click()
# browser.implicitly_wait(10)
# time.sleep(0.5)
#
# # hit left tab
# for i in range(4):
#
#     #grab all lines
#     soup_level1 = bs(browser.page_source, 'lxml')
#     lineParent = soup_level1.find_all('div', class_ = 'slds-col slds-size--1-of-1')
#     print("This instance's number of services " + str(lineParent.__len__()))
#     curName = ''
#     lineIdx = 3
#     for line in lineParent:
#         #find if there are any incidents in this particular time line
#         incidents = line.find_all('div', class_ = 'timeline-row-item')
#         print(incidents.__len__())
#         if incidents.__len__() != 0:
#             # get the current service name
#             serviceName = line.find('div', class_='slds-col timeline-row-label')
#             curName = serviceName.find('span').text
#
#             #grab each incident on this line
#             totalDurations = 0
#             incidentIdx = 3
#             for incident in incidents:
#                 print("line index is "+ str(lineIdx))
#                 print("incident index is "+ str(incidentIdx))
#                 #click on the incident
#                 browser.execute_script("arguments[0].click();", WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div[{}]/div/div[1]/div/div[{}]/div[2]'.format(lineIdx, incidentIdx)))))
#                 #browser.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div[{}]/div/div[1]/div/div[{}]/div[2]'.format(lineIdx, incidentIdx)).click()
#                 browser.implicitly_wait(60)
#                 time.sleep(3)
#
#                 #grab the info off the pop up
#                 soup_level1 = bs(browser.page_source, 'lxml')
#                 sections = soup_level1.find('div', class_ = "slds-col slds-size_1-of-3 slds-p-left--medium slds-border_left")
#                 #for maintainance
#                 if sections == None:
#                     sections = soup_level1.find('div',class_="sc-jLMuHf eLztnl")
#                 count = 0
#                 for section in sections:
#                     if count == 2:
#                         durationParent = section.find('p')
#                         #for maintainance
#                         if durationParent != None:
#                             duration = durationParent.text
#                             totalDurations = totalDurations + convert(duration)
#                         else:
#                             durationParent = section.find('div', class_ = "sc-ddviEe lidJGG")
#                             duration = durationParent.text
#                             totalDurations = totalDurations + convert(duration)
#                     count = count + 1
#
#                 #click cancel
#                 try:
#                     print("trying the regular way")
#                     browser.find_element_by_xpath('/html/body/div[4]/div/div/section/div/header/button').click()
#                 except NoSuchElementException as e:
#                     print("the regular cancel button did not work")
#                     browser.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div[2]/div[2]/div[1]/span').click()
#
#                 browser.implicitly_wait(10)
#                 time.sleep(3)
#
#                 incidentIdx = incidentIdx + 1
#             print("the total duration is "+ str(totalDurations))
#             #check what service this is and add to that service
#             # if totalDurations > 0:
#             #     if curName == "Core Service":
#             #         core_Service = core_Service + totalDurations
#             #     elif curName == "Search":
#             #         search = search + totalDurations
#             #     elif curName == "Analytics":
#             #         analytics = analytics + totalDurations
#             #     elif curName == "Live Agent":
#             #         live_Agent= live_Agent+ totalDurations
#             #     elif curName == "CPQ and Billing":
#             #         cpqb = cpqb + totalDurations
#             #     elif curName == "Einstein Bots":
#             #         einstein_Bots= einstein_Bots+ totalDurations
#             #     elif curName == "Communities":
#             #         communities= communities + totalDurations
#             #     elif curName == "Customer 360 Audiences":
#             #         c3a = c3a + totalDurations
#             #     else:
#             #         print("THIS IS A SERVICE THAT IS NOT RECOGNIZED")
#             # print("Core Service down time is "+ str(core_Service))
#         lineIdx = lineIdx + 1
#     browser.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div[2]/button[1]').click()
#     browser.implicitly_wait(10)
#     time.sleep(0.5)