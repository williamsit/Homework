import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path)

mars_dict = {}

#NASA Mars News

def scrape_mars_news():
    try:
        browser = init_browser()
        news_paragraph_url = "https://mars.nasa.gov/news/"
        browser.visit(news_paragraph_url)

        news_paragraph_html = browser.html
        news_paragraph_soup = bs(news_paragraph_html, "html.parser")

        news_title = news_paragraph_soup.find("div", class_="content_title").find("a").text
        news_p = news_paragraph_soup.find("div", class_="article_teaser_body").text

        mars_dict["news_title"] = news_title 
        mars_dict["news_p"] = news_p

        return mars_dict
    
    finally:
        browser.quit()

#JPL Mars Space Images

def scrape_mars_image():
    try:
        browser = init_browser()
        space_images_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(space_images_url)

        space_images_html = browser.html
        featured_image_soup = bs(space_images_html, "html.parser")
        featured_image_link = featured_image_soup.find("article")["style"].replace("background-image: url('", "").replace("');", "")

        web_link = "https://www.jpl.nasa.gov"
        featured_image_url = web_link + featured_image_link

        mars_dict["featured_image_url"] = featured_image_url 

        return mars_dict

    finally:
        browser.quit()

#Mars Weather

def scrape_mars_weather():
    try:
        browser = init_browser()
        mars_weather_url = "https://twitter.com/marswxreport?lang=en"
        browser.visit(mars_weather_url)

        mars_weather_html = browser.html
        mars_weather_soup = bs(mars_weather_html, "html.parser")

        mars_weather_tweets = mars_weather_soup.find_all("div", class_="js-tweet-text-container")
        for each_tweet in mars_weather_tweets:
            tweet_text = each_tweet.find("p").text
            if "pic.twitter.com" not in tweet_text:
                mars_weather = each_tweet.find("p").text
                break
            else:
                pass

        mars_dict["mars_weather"] = mars_weather 

        return mars_dict

    finally:
        browser.quit()

#Mars Facts

def scrape_mars_facts():
    try:
        mars_facts_url = "http://space-facts.com/mars/"

        mars_facts_df = pd.read_html(mars_facts_url)[0]
        mars_facts_df.columns = ["description", "value"]
        mars_facts_df.set_index("description", inplace=True)

        mars_facts_html = mars_facts_df.to_html()
        mars_dict["mars_facts"] = mars_facts_html

        return mars_dict
    except:
        print("error")

#Mars Hemispheres

def scrape_mars_hemispheres():
    try:
        browser = init_browser()
        mars_hemispheres_link = "https://astrogeology.usgs.gov"
        mars_hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(mars_hemispheres_url)

        mars_hemispheres_html = browser.html
        mars_hemispheres_soup = bs(mars_hemispheres_html, "html.parser")

        hemisphere_image_urls = []

        mars_hemispheres_list = mars_hemispheres_soup.find_all("div", class_="item")

        for each_hemisphere in mars_hemispheres_list:
            title = each_hemisphere.find("h3").text
            
            mars_hemispheres_image_link = each_hemisphere.find("a", class_="itemLink product-item")["href"]
            mars_hemispheres_download_url = mars_hemispheres_link + mars_hemispheres_image_link
            
            browser.visit(mars_hemispheres_download_url)
            mars_hemispheres_download_html = browser.html
            mars_hemispheres_download_soup = bs(mars_hemispheres_download_html, "html.parser")
            
            mars_hemispheres_full_image_link = mars_hemispheres_download_soup.find("img", class_="wide-image")["src"]
            mars_hemispheres_image_url = mars_hemispheres_link + mars_hemispheres_full_image_link

            hemisphere_image_urls.append({"title" : title, "img_url" : mars_hemispheres_image_url})
        
        mars_dict["hemisphere_image_urls"] = hemisphere_image_urls

        return mars_dict

    finally:
        browser.quit()


