#Import dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pymongo
import pandas as pd
import requests

# Setup connection to mongodb
# conn = "mongodb://localhost:27017"
# client = pymongo.MongoClient(conn)

# # Select database and collection to use
# db = client.mars_data
# collection = db.mars_data

def scrape():
    #Activate chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    #Get request
    url = ('https://mars.nasa.gov/news/')

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #Scrape News Titles under: "title" variable
    news_titles = soup.find_all('div', class_="content_title")

    #Scrape News Text under variable: "news_text"
    news_text = soup.find_all('div', class_='rollover_description')

    titles_list = []
    news_texts_list = []

    # Collect News Title & Text in results
    results = soup.find_all('div', class_="slide")
    for result in results:
        news_title = result.find('div', class_="content_title")
        titles = news_title.find('a').text
        news_text = result.find('div', class_="rollover_description")
        news_texts = news_text.find('div', class_="rollover_description_inner").text
        titles_list.append(titles)
        news_texts_list.append(news_texts)

    #Get request for image url
    images_url = ('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')

    response = requests.get(images_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #Scrape Space Images from site
    images = soup.find_all('a', class_="fancybox")

    #Scrape current Featured Mars Image link
    picture_srcset = []
    for image in images:
        picture = image['data-fancybox-href']
        picture_srcset.append(picture)

    featured_image_url = 'https://www.jpl.nasa.gov' + picture

    #Get request for image url
    url = ('https://twitter.com/marswxreport?lang=en')

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #Scrape Tweet Text from site
    tweet_contents = soup.find_all('div', class_="content")

    #Scrape Mars Weather Info from Recent Tweet --> 
    #Mars currently in solar conjuction, no weather reading for two weeks!
    weatherContents = []
    for content in tweet_contents:
        tweet = content.find('div', class_="js-tweet-text-container").text
        weatherContents.append(tweet)

    mars_weather = weatherContents[5]

    #Converting facts table from html to pandas dataframe
    mars_facts_url = "https://space-facts.com/mars/"
    table = pd.read_html(mars_facts_url)

    #Rename Comparison to transform table to mars only facts
    df = table[0]
    df = df.rename(columns={'Mars - Earth Comparison':'Facts'})

    #Drop Earth Facts
    df = df.drop(columns='Earth')

    #Set Index to Facts
    df = df.set_index(['Facts'])

    #Convert 
    mars_facts_html = df.to_html()

    hemisphere_image_urls = []
    #Get request for image url
    url = ('https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg')

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #Find Hemisphere Image Tag
    valles_marineris_img = soup.find_all('div', class_="wide-image-wrapper")

    #Scrape image and details in the hemisphere webpage & append to dictionary
    for img in valles_marineris_img:
        pic = img.find('li')
        full_img = pic.find('a')['href']
    valles_marineris_title = soup.find('h2', class_='title').text
    valles_marineris_hem = {"Title": valles_marineris_title, "url": full_img}

    hemisphere_image_urls.append(valles_marineris_hem)

    #Get request for image url
    url = ('https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg')

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #Find Hemisphere Image Tag
    cerberus_img = soup.find_all('div', class_="wide-image-wrapper")

    #Scrape image and details in the hemisphere webpage
    for img in cerberus_img:
        pic = img.find('li')
        full_img = pic.find('a')['href']
    cerberus_title = soup.find('h2', class_='title').text
    cerberus_hem = {"Title": cerberus_title, "url": full_img}

    hemisphere_image_urls.append(cerberus_hem)

    url = ('https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg')

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #Find Hemisphere Image Tag
    shiaparelli_img = soup.find_all('div', class_="wide-image-wrapper")

    #Scrape image and details in the hemisphere webpage
    for img in shiaparelli_img:
        pic = img.find('li')
        full_img = pic.find('a')['href']
    shiaparelli_title = soup.find('h2', class_='title').text
    shiaparelli_hem = {"Title": shiaparelli_title, "url": full_img}

    hemisphere_image_urls.append(shiaparelli_hem)

    #Get request for image url
    url = ('https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg')

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #Find Hemisphere Image Tag
    syrtris_img = soup.find_all('div', class_="wide-image-wrapper")

    #Scrape image and details in the hemisphere webpage
    for img in syrtris_img:
        pic = img.find('li')
        full_img = pic.find('a')['href']
    syrtris_title = soup.find('h2', class_='title').text
    syrtris_hem = {"Title": syrtris_title, "url": full_img}

    hemisphere_image_urls.append(syrtris_hem)

    # Store data in a dictionary
    mars_data = {
        "titles": titles_list,
        "news_texts_list": news_texts_list,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "facts_table": mars_facts_html,
        "hemisphere_image_urls":hemisphere_image_urls
    }

    return mars_data


if __name__ == '__main__':
    hemisphere_image_urls = scrape()
