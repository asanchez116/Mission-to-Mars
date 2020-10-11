
# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site
# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')

slide_elem.find("div", class_='content_title')


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### JPL Space Images Featured Image
# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# ### Mars Facts
df = pd.read_html('http://space-facts.com/mars/')[0]
df.head()
df.columns = ['Description', 'Mars']
df.set_index('Description', inplace=True)
df

df.to_html()

#################################
#                               #
#    start of challenge code    #
#                               #
#                               #
#################################

# ### Mars Weather
# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# ### Hemispheres
# 1. Use browser to visit the URL
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
titles = []
# 3. Write code to retrieve the image urls and titles for each hemisphere.

html = browser.html
hem_html = soup(html, 'html.parser')
items = hem_html.find_all('h3')
for item in items:
    titles.append(item.text)

links = []
product_link = hem_html.find_all('a', class_='itemLink product-item')
for link in product_link:
    url = f"https://astrogeology.usgs.gov/{link.get('href')}"
    if url not in links:
        links.append(url)

hemisphere_image_urls = []
for link in range(len(links)):
    img_dict = {}
    browser.visit(links[link])
    # convert to html
    new_page = browser.html
    page = soup(new_page, 'html.parser')
    # isolate download section
    download = page.select_one('li')
    # isolate url
    image_url = download.find('a').get('href')
    img_dict['img_url'] = image_url
    img_dict['title'] = titles[link]
    hemisphere_image_urls.append(img_dict)
    browser.back()


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# 5. Quit the browser
browser.quit()
