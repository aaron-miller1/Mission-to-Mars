

# Import Splinter and BS

from splinter import Browser

from bs4 import BeautifulSoup as soup

import pandas as pd

import datetime as dt

import lxml

from webdriver_manager.chrome import ChromeDriverManager



def scrape_all():
    # Initiate headless driver for deployment

    executable_path = {'executable_path': ChromeDriverManager().install()}

    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)

    hemisphere_image_urls = hemi_scrape(browser)

    # run all scraping

    data = {
            'news_title': news_title,
            'news_paragraph': news_paragraph,
            'featured_image': featured_image(browser),
            'facts': mars_facts(),
            'last_modified': dt.datetime.now(),
            'hemispheres': hemisphere_image_urls
    }

    # Stop webdriver and return

    browser.quit()
    return data


def mars_news(browser):

    # Mars Nasa Site

    url = 'https://redplanetscience.com'

    browser.visit(url)

    # Load Delay

    browser.is_element_present_by_css('div.list_text', wait_time=1)



    html = browser.html

    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')

    slide_elem.find('div', class_='content_title')



    news_title =  slide_elem.find('div', class_='content_title').get_text()

    news_title


    # paragraph text

    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    news_p


    # add try/except

    try:

        slide_elem = news_soup.select_one('div.list_text')

        news_title = slide_elem.find('div', class_='content_title').get_text()

        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None


    
    return news_title, news_p


# ### Featured Images


def featured_image(browser):

    # Visit URL

    url = 'https://spaceimages-mars.com'

    browser.visit(url)





    # Find and click full image button

    full_image_elem = browser.find_by_tag('button')[1]

    full_image_elem.click()



    # Parse the resulting html

    html = browser.html

    img_soup = soup(html, 'html.parser')


    #   Find the relative image url

    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    img_url_rel


    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:

        return None

    # base url

    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

def mars_facts():

    try:

        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    df.columns =['description','Mars','Earth']

    df.set_index('description', inplace=True)
    


    return df.to_html()



def hemi_scrape(browser):

    # Visit URL
    url = 'https://marshemispheres.com/'

    browser.visit(url)


    hemisphere_image_urls = []


    for i in range(4):
    
        hemi = {}
        browser.find_by_css("a.product-item img")[i].click()
        elem = browser.links.find_by_text('Sample').first
        img = elem['href']
        title = browser.find_by_css('h2.title').text
        hemi['img_url'] = img
        hemi['title'] = title
        hemisphere_image_urls.append(hemi)
        
        
        browser.back()

    return hemisphere_image_urls


if __name__ == "__main__":

    print(scrape_all())
