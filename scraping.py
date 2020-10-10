#!/usr/bin/env python
# coding: utf-8
# import splinter and Beautiful Soup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
# Set the executable path and initalize the chrome browser in splinter
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)
# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'


browser.visit(url)


# Delay for loading the page


browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


slide_elem.find('div', class_='content_title').get_text()


news_title = slide_elem.find('div', class_='')


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').text
news_p


# ## Featured Impages


# visit image website
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
page = browser.visit(url)


# Find and click the full image
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)


more_info_elem = browser.links.find_by_partial_text('more info')


more_info_elem.click()


# Parse the resulting html with soup

html = browser.html
img_soup = soup(html, 'html.parser')


img_url_rel = img_soup.select_one('figure.lede a img').get('src')
img_url_rel


# Use the base URL to create an absolute link
img_url = f"https://www.jpl.nasa.gov{img_url_rel}"


# ## Mars Facts


url = 'https://space-facts.com/mars/'
browser.visit(url)
html = browser.html
mars_facts = soup(html, 'html.parser')


table = mars_facts.find(
    'table', id='tablepress-p-mars', class_='tablepress tablepress-id-p-mars')


df = pd.read_html('http://space-facts.com/mars/')[0]
df.head()

df.columns = ['Description', 'Mars']
df.set_index('Description', inplace=True)
df
df.to_html()

browser.quit()
