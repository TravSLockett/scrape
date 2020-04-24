from selenium import webdriver
from bs4 import BeautifulSoup as bs

browser = webdriver.Chrome()
browser.get('https://hofstraonline.hofstra.edu/pls/HPRO/bwckschd.p_disp_dyn_sched')
browser.maximize_window()
browser.implicitly_wait(10)
browser.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/div/div[2]/form/div/table/tbody/tr/td/select').click()
browser.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/div/div[2]/form/div/table/tbody/tr/td/select/option[4]').click()
browser.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/div/div[2]/form/button[1]').click()
browser.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/div/div[3]/form/button[1]').click()

web = bs(browser.page_source, 'html.parser')
test = web.find_all('tr', id = 'section_row')
print(len(test))
browser.quit()