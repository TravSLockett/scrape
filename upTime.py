from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs
from requests import get
from lxml import html

browser = webdriver.Chrome()
browser.get('https://status.cloud.google.com/summary')
browser.maximize_window()
browser.implicitly_wait(10)


#find all the xpath value
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

#testing for one
browser.find_element_by_xpath('/html/body/div/div[3]/table/tbody/tr[1]/th/a').click()
browser.implicitly_wait(10)
soup_level1 = bs(browser.page_source, 'lxml')
num = 0

for idx in soup_level1.find_all('td', class_ = 'description'):
        num = num + 1
        print(idx.text)
print(num)


#to click all the buttons
# for pos in xpathV:
#     try:
#         #go to the second page
#         browser.implicitly_wait(10)
#         print('/html/body/div/div[3]/table/tbody/tr[{}]/th/a'.format(pos))
#         browser.find_element_by_xpath('/html/body/div/div[3]/table/tbody/tr[{}]/th/a'.format(pos)).click()
#         browser.implicitly_wait(10)
#
#     except:
#         print("clicking has an error at position "+ str(pos))
#     else:
#         index = index + 1
#         browser.back()
#         browser.implicitly_wait(10)
#         print(index)

#browser.quit()
