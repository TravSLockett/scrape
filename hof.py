from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs
from requests import get


browser = webdriver.Chrome()
browser.get('https://hofstraonline.hofstra.edu/pls/HPRO/bwckschd.p_disp_dyn_sched')
browser.maximize_window()
browser.implicitly_wait(10)
browser.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/div/div[2]/form/div/table/tbody/tr/td/select').click()
browser.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/div/div[2]/form/div/table/tbody/tr/td/select/option[3]').click()
browser.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/div/div[2]/form/button[1]').click()
browser.implicitly_wait(10)
browser.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/div/div[3]/form/button[1]').click()

#soup_level1 = bs(browser.page_source, 'lxml')
#for idx in soup_level1.find_all('div', class_ = 'cues style-scope ytd-transcript-body-renderer'):
#    print(idx)
#/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[2]/div/div[1]/ytd-engagement-panel-section-list-renderer[2]/div[1]/ytd-engagement-panel-title-header-renderer/div[2]/div[4]/ytd-menu-renderer

#trans = browser.find_elements_by_css_selector('#body > ytd-transcript-body-renderer > div:nth-child(1)')
#browser.quit()

