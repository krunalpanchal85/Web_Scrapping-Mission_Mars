from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:\\Users\kruna\AppData\Local\Programs\Python\Python37\chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    # Visit visitcostarica.herokuapp.com
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the new titles
    news_titles  = soup.find('div', class_="content_title").a.text
    # Get the news teaser
    news_p = soup.find_all('div', class_="article_teaser_body")[0].text
#---------------------------------------------------------------------------------------------------------------------------
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(1)
    full_image_elem = browser.find_by_id("full_image")
    full_image_elem.click()
    browser.is_element_present_by_text("more info",wait_time = 1)
    more_info_elem = browser.find_link_by_partial_text("more info")
    more_info_elem.click()
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the image
    featured_image_url = soup.select_one("figure.lede a img").get("src")
    image_url = f'https://www.jpl.nasa.gov{featured_image_url}'
    #image_url

#--------------------------------------------------------------------------------------------------------------------------------
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    #Mars weather
    mars_weather= soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[0].text
#----------------------------------------------------------------------------------------------------------------------------------
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    time.sleep(1)
    
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    #weather details
    df = pd.read_html(url)
    mars_df = df[0]
    mars_df.columns = ['','Values']
    mars_info = mars_df.to_html(index= True)
    mars_info = mars_info.replace('/n',' ')
#------------------------------------------------------------------------------------------------------------------------------------
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    hem_image_urls = []
    links = browser.find_by_css("a.product-item h3")

    for i in range(len(links)):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[i].click()
        sample_elem=browser.find_link_by_text("Sample").first
        hemisphere["featured_image_url"]=sample_elem["href"]
        hemisphere["title"]=browser.find_by_css("h2.title").text
        hem_image_urls.append(hemisphere)
        browser.back()

        hem_image_urls
#---------------------------------------------------------------------------------------------------------------------------------
    # Store data in a dictionary
    mars_data = {
        "news_titles": news_titles,
        "news_p": news_p,
        "image_url": image_url,
        'mars_weather': mars_weather,
        'mars_info' : mars_info,
        'hem_image_urls' : hem_image_urls,
    }

    #print(mars_data)
    # Close the browser after scraping
    browser.quit()

    # Return results
    #print(mars_data)
    return mars_data
    