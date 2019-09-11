import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
import time

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():

    browser = init_browser()

    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    nasa_title = soup.find("div",class_="content_title").text
    nasa_p = soup.find("div", class_="article_teaser_body").text
    
    featured_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(featured_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    main_url = 'https://www.jpl.nasa.gov'
    img_url = soup.find("a", class_='button fancybox')["data-fancybox-href"]
    featured_image_url = main_url + img_url
    
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather = soup.find('p', class_ = 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    
    table_url = 'https://space-facts.com/mars/'
    mars_table = pd.read_html(table_url)

    mars_df = mars_table[1]
    mars_df.columns = ['Mars Planet Profile', '']
    mars_df.set_index('Mars Planet Profile', inplace=True)

    mars_html_table = mars_df.to_html()
    mars_html_table = mars_html_table.replace('\n', '')
    
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    stock_url = 'https://astrogeology.usgs.gov'
    img_links = soup.find_all('div', class_= "description")
    hemisphere_image_urls = []

    for img in img_links:
        hemi = img.find('h3').text
        i_url = img.find('a', class_="itemLink product-item")['href']
        img_url = stock_url + i_url
        browser.visit(stock_url + i_url)
        img_html = browser.html
        soup = BeautifulSoup(img_html, 'html.parser')
        imgs_url = stock_url + soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({"title" : hemi, "img_url" : imgs_url})
    
    
    scrape_data = {
        "Nasa_Title": nasa_title,
        "Nasa_Paragraph": nasa_p,
        "Featured_Image": featured_image_url,
        "Mars_Weather": mars_weather,
        "Mars_Table": mars_html_table,
        "Hemispheres": hemisphere_image_urls
    }
    
    browser.quit()
    return scrape_data
    
    

