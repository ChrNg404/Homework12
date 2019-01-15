# Dependencies
import pandas as pd
from bs4 import BeautifulSoup
import requests
import pymongo
import os
import time
from splinter import Browser

def scrape():
    executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    mars_info={}

    # URL of the pages to be scraped
    nasaurl = 'https://mars.nasa.gov/news/'
    #browser
    browser.visit(nasaurl)
    #define the html
    time.sleep(1)
    #define the soup
    html=browser.html
    #soup=bs(html,'html.parser')
    # Retrieve page with requests module
    nasaresponse = requests.get(nasaurl)

    #Create BeautifulSOup object; parse with 'lxml'

    nasasoup = BeautifulSoup(nasaresponse.text,'lxml')

    # Retrieve data from Nasa website
    mars_info['news_title']=nasasoup.find('div',class_='content_title').text
    mars_info['news_para']=nasasoup.find('div',class_='rollover_description_inner').text

    # Scrape JPL website
    # URL of the pages to be scraped
    JPLurl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    #browser
    browser
    browser.visit(JPLurl)
    #define the html
    time.sleep(1)
    #define the soup
    html=browser.html
    #soup=bs(html,'html.parser')
    # Retrieve page with requests module
    JPLresponse = requests.get(JPLurl)

    #Create BeautifulSOup object; parse with 'lxml'

    JPLsoup = BeautifulSoup(JPLresponse.text,'lxml')

    # Retrieve data from JPL website
    feat_image = JPLsoup.find('h2',class_='brand_title').text
    JPLimg = JPLsoup.find('a',class_='button fancybox')['data-fancybox-href']

    mars_info['featured_image']=("https://www.jpl.nasa.gov"+JPLimg)

    # Scrape Mars weather website
    # URL of the pages to be scraped
    Weatherurl = 'https://twitter.com/marswxreport?lang=en'
    #browser
    browser.visit(Weatherurl)
    #define the html
    time.sleep(1)
    #define the soup
    html=browser.html
    #soup=bs(html,'html.parser')
    # Retrieve page with requests module
    Weatherresponse = requests.get(Weatherurl)

    #Create BeautifulSOup object; parse with 'lxml'

    Weathersoup = BeautifulSoup(Weatherresponse.text,'lxml')

    # Retrieve data from Weather website
    mars_info['mars_weather']=Weathersoup.find('div',class_='js-tweet-text-container').text
    
    # Scrape mars facts website
    Factsurl = 'https://space-facts.com/mars/'
    browser.visit(Factsurl)
    time.sleep(1)
    html=browser.html
    #soup=bs(html,'html.parser')
    Factsresponse = requests.get(Factsurl)

    # Create delicious soup

    Factssoup = BeautifulSoup(Factsresponse.text,'lxml')

    tables = pd.read_html(Factsurl)

    df = tables[0]
    df.columns = ['Description', 'Value']
    mars_df = df.set_index('Description')

    mars_info['mars_facts'] = mars_df.to_html()

    return mars_info


