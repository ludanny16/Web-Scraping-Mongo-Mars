
#Dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from selenium import webdriver
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
# URL of page to be scraped
    url = "https://mars.nasa.gov/news/"
# Retrieve page with the requests module
    response = requests.get(url)
# Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')

    news_title = soup.find("div", class_="content_title").text
#print(news_title)
    

    news_p = soup.find('div', class_='rollover_description_inner').text
#print(news_p)
    


    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    time.sleep(2)
    html = browser.html
    soup = bs(html, "html.parser")
    browser.find_by_css("div.carousel_container div.carousel_items a.button").first.click()

# Design an XPATH selector to grab the image
    xpath = '//*[@id="fancybox-lock"]/div/div[2]/div/div[1]/a[2]'

    time.sleep(2)
    browser.find_by_xpath(xpath).click()

    time.sleep(2)
    html = browser.html
    soup = bs(html, 'html.parser')
    img_url = soup.find("img", class_="main_image")["src"]
#img_url
    featured_image = 'https://www.jpl.nasa.gov/' + img_url
#print(featured_image)
    

# Scrape the latest Mars weather tweet from the page
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(weather_url)
    weather_soup = bs(response.text,'html.parser')
    mars_weather_tweet = weather_soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})

    mars_weather=mars_weather_tweet.find('p',class_='TweetTextSize').text
# use Pandas to scrape the table containing facts 
# about the planet including Diameter, Mass, etc.
    Mars_Facts = 'https://space-facts.com/mars/'
    data = pd.read_html(Mars_Facts,skiprows=1)[0]
    table = data.to_html(header=True, index=False) 
#table

# Mars Hemisphere/obtain high resolution images
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html,'html.parser')
    hemispheres = soup.find('div',class_='collapsible results')
    results = hemispheres.find_all('a')

    hemisphere_image_urls = []
    for result in results: 
        if result.h3:
            title = result.h3.text
            link = 'https://astrogeology.usgs.gov' + result['href']
            print(title,link)
            browser.visit(link)
            time.sleep(2)
            image_html = browser.html
            soup = bs(image_html,'html.parser')
            soup_image = soup.find('div', class_='downloads').find('li').a['href']
            print(soup_image)
            mars_images = {'title':title, 'img_url':soup_image}
            hemisphere_image_urls.append(mars_images)

    mission_to_mars = {
        "id": 1,
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image,
        "mars_weather": mars_weather,
        "fact_table": table,
        "hemisphere_images": hemisphere_image_urls
    }

    return mission_to_mars
