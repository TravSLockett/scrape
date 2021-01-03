from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs
from requests import get
from lxml import html
import plotly.graph_objects as go
import pandas as pd
import csv


serviceN =[]
data20 = []
data19 =[]
data18 = []
data17 = []
data16 = []

#convertion function
def conStr2Num(item):
    down = 0
    try:
        # check if it has hour in it
        idx_hour = item.index("hour")
        length_h = int(item[idx_hour - 3].strip() + item[idx_hour - 2].strip())
        # check the minutes
        idx_min = item.index("minute")
        length_m = int(item[idx_min - 3].strip() + item[idx_min - 2].strip())
        # convert minutes to hours
        length_m = length_m / 60
        length_h = length_h + length_m
        down = length_h

    except:
        # record the minutes since there is no hour in the record
        idx_min = item.index("minute")
        length_m = int(item[idx_min - 3].strip() + item[idx_min - 2].strip())
        # convert minutes to hours
        length_m = length_m / 60
        down = length_m
    finally:
        return down


#open the website
browser = webdriver.Chrome(executable_path='/Users/Travishungry/nerd/scrape/chromedriver')
#browser = webdriver.Chrome()
browser.get('https://status.cloud.google.com/summary')
browser.maximize_window()
browser.implicitly_wait(10)


#find all the xpath position value
xpathV = []
soup_level1 = bs(browser.page_source, 'lxml')
count = 1
for idx in soup_level1.find_all('tr'):
        if(idx.find(text= "Historic")):
                print("FOUND it at" + str(count))
                xpathV.append(count)
        count = count + 1
print(count)


#click on each xpath
print("how many historics are there? "+ str(xpathV.__len__()))
index = 1

#to click all the buttons
for pos in xpathV:
    try:
        print("The Current Position is "+ str(pos))
        #get the name of the service
        soup_level1 = bs(browser.page_source, 'lxml')
        name = ""
        for idx in soup_level1.select('#maia-main > table > tbody > tr:nth-child({}) > th > h1 > a'.format(pos)):
            name = idx.text
        serviceN.append(name)
        #go to the second page
        browser.implicitly_wait(10)
        browser.find_element_by_xpath('/html/body/div/div[3]/table/tbody/tr[{}]/th/a'.format(pos)).click()
        browser.implicitly_wait(10)
        soup_level1 = bs(browser.page_source, 'lxml')

        #find all the records and add them to a list
        num = 0
        thisOne = []
        for idx in soup_level1.find_all('td', class_='description'):
            num = num + 1
            thisOne.append(idx.text.strip())
        print("there are " + str(num) + " records in "+ name )
        print(thisOne)

        if thisOne.__len__() != 0:
            #convert into uptime
            down20 = 0
            down19 = 0
            down18 = 0
            down17 = 0
            down16 = 0
            down15 = 0
            arr20 = []
            arr19 = []
            arr18 = []
            arr17 = []
            arr16 = []
            arr15 = []
            for item in thisOne:
                if "2020" in item:
                    arr20.append(item)
                    value20 = conStr2Num(item)
                    down20 = down20 + value20

                elif "2019" in item:
                    arr19.append(item)
                    value19 = conStr2Num(item)
                    down19 = down19 + value19
                elif "2018" in item:
                    arr18.append(item)
                    value18 = conStr2Num(item)
                    down18 = down18 + value18
                elif "2017" in item:
                    arr17.append(item)
                    value17 = conStr2Num(item)
                    down17 = down17 + value17
                elif "2016" in item:
                    arr16.append(item)
                    value16 = conStr2Num(item)
                    down16 = down16 + value16
                elif "2015" in item:
                    arr15.append(item)
                    value15 = conStr2Num(item)
                    down15 = down15 + value15
            print("Number of items in 2020 " + str(arr20.__len__()))
            print("Number of items in 2019 " + str(arr19.__len__()))
            print("Number of items in 2018 " + str(arr18.__len__()))
            print("Number of items in 2017 " + str(arr17.__len__()))
            print("Number of items in 2016 " + str(arr16.__len__()))

            up20 = "{0:.5g}".format((1 - (down20 / 8760))*100)
            up19 = "{0:.5g}".format((1 - (down19 / 8760))*100)
            up18 = "{0:.5g}".format((1 - (down18 / 8760))*100)
            up17 = "{0:.5g}".format((1 - (down17 / 8760))*100)
            up16 = "{0:.5g}".format((1 - (down16 / 8760))*100)
            print("2020 up time is " + str(up20))
            print("2019 up time is " + str(up19))
            print("2018 up time is " + str(up18))
            print("2017 up time is " + str(up17))
            print("2016 up time is " + str(up16))

            #add the data to the list
            if arr20.__len__() != 0:
                data20.append(up20)
            else:
                data20.append("100.00")
            if arr19.__len__() != 0:
                data19.append(up19)
            else:
                data19.append("100.00")
            if arr18.__len__() != 0:
                data18.append(up18)
            else:
                data18.append("100.00")
            if arr17.__len__() != 0:
                data17.append(up17)
            else:
                data17.append("100.00")
            if arr16.__len__() != 0:
                data16.append(up16)
            else:
                data16.append("100.00")
        else:
            #there is no record in this service, add NA to table
            data20.append("100.00")
            data19.append("100.00")
            data18.append("100.00")
            data17.append("100.00")
            data16.append("100.00")


    except:
        print("There is an error at position "+ str(pos))
        break
    else:
        browser.implicitly_wait(30)
        index = index + 1
        browser.back()
        browser.implicitly_wait(10)
        print("This is the "+ str(index)+ "th click/services")
    finally:
        print("IT IS DONE SUCCESSFULLY")

browser.quit()
#graph the data to the table
print("length of serviceName is " + str(len(serviceN)))
print("length of 2020 is " + str(len(data20)))
print("length of 2019 is " + str(len(data19)))
print("length of 2018 is " + str(len(data18)))
print("length of 2017 is " + str(len(data17)))
print("length of 2016 is " + str(len(data16)))

#write the data to excel
writer = pd.ExcelWriter('up_google.xlsx', engine='openpyxl')
wb  = writer.book
df = pd.DataFrame({'Service Name': serviceN,
                  '2020': data20, '2019': data19, '2018':data18, '2017': data17, '2016':data16})
df.to_excel(writer, "Google Cloud")
wb.save('up_google.xlsx')

fig = go.Figure(data=[go.Table(
    header=dict(values=['Service Name', '2020', '2019', '2018', '2017', '2016'],
                line_color='darkslategray',
                fill_color='lightskyblue',
                align='left'),
    cells=dict(values=[serviceN, # 1st column
                       data20,data19, data18,data17,data16], # 2nd column
               line_color='darkslategray',
               fill_color='lightcyan',
               align='left'))
])

fig.show()


