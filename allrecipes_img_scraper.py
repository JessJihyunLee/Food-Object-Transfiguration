import os
import re
import requests
import signal
import sys
from pdb import set_trace as st

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def signal_handler(sig, frame):
    """Catch SIGINTS and terminate gracefully."""
    global driver
    print('Ctrl-C caught. Terminating Chrome instance...')
    driver.quit()
    print('Exiting...')
    sys.exit()

def create_webdriver(incognito:bool=True, headless:bool=True):
    """Instantiate and return a selenium chrome webdriver.

    Args:
        incognito: A flag to set the browser to surf in incognito mode.
        headless: A flag to tell the driver to not render a visible browser to
            avoid the resource overhead associated with rendering.

    Returns: a Chrome WebDriver object to use for automated browsing.
    """
    # add webdriver options
    options = webdriver.ChromeOptions()
    if incognito:
        options.add_argument(' — incognito')
    if headless:
        options.add_argument('headless')

    # initialize chrome instance
    driver_path = os.environ.get('CHROME_DRIVER_PATH')
    if not driver_path:
        one_time_path = input('No CHROME_DRIVER_PATH environment variable set. '
                              'Would you like to specify a path to your '
                              'Chrome driver now? (note: this will not set your '
                              'environment variable for future runs) [y/N]: ')
        if one_time_path == 'y' or one_time_path == 'Y':
            driver_path = input('Please specify the path to your Chrome driver: ')
        else:
            raise RuntimeError('No CHROME_DRIVER_PATH environment variable set. '
                               'Please use `export CHROME_DRIVER_PATH={path to '
                               'chromedriver file}` in your shell to point to a '
                               'chrome driver')
    return webdriver.Chrome(executable_path=driver_path, chrome_options=options)

def get_page(driver:webdriver.chrome.webdriver.WebDriver,
             url:str, by_type:str, wait_ele:str, timeout:int=20,
             attempt:int=1) -> None:
    """Retrieve a page and wait until a certain element has been loaded.

    Args:
        driver: Chrome driver object used to scrape data.
        url: Url for the Chrome driver to load.
        timeout: Number of seconds to wait for the page to load.
        by_type: Attribute of element to wait for chosen from constants defined
            in `selenium.webdriver.common.by.By`.
        wait_ele: Specified parameter for to wait for defined by by_type.
        attempt: Number of times the driver has tried to request a page.

    Raises:
        TimeoutException: If page doesn't load in a specified amount of seconds
    """
    driver.get(url)

    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((
            by_type, wait_ele)))
    except TimeoutException:
        attempt += 1
        driver.quit()
        if attempt <= 3:
            print('Timed out waiting for page to load. Retrying...')
            # TODO: reinitialize webdriver with defined options
            driver = create_webdriver()
            get_page(driver, url, by_type, wait_ele, timeout, attempt)
        else:
            print('Third timeout encountered. Exiting...')
            sys.exit()

print('Initializing...')

# we make a strict regex rule to ensure we don't get other links that the
# photo grid might; we only want the photos
RE_RECIPE_PHOTOS = r'https:\/\/www\.allrecipes\.com\/recipe\/\d*\/.*\/photos\/\d*\/'
IMG_LINK_DOMAIN = 'https://images.media-allrecipes.com/'

driver = create_webdriver()
signal.signal(signal.SIGINT, signal_handler)

# define webpage to scrape
search_url = 'https://www.allrecipes.com/search/results/?wt=chicken%20wings&sort=re&page={}'
timeout = 20
page_num = 1
photo_id = 1

# class names for elements to find
recipe_link_class = 'grid-card-image-container'
photo_strip_class = 'photo-strip__items'
photos_band_class = 'photos--band'


if not os.path.isdir('img'):
    print('img directory not found. Making img directory at run path.')
    os.mkdir('img')
else:
    print('img directory found at run path. Using that directory.')

print('Initialization complete.')

while True:
    print('\nCollecting recipes on page {}'.format(page_num))
    get_page(driver, search_url.format(page_num), By.CLASS_NAME,
             recipe_link_class, timeout)

    # grab the element with the recipe link
    # links = [element.find_element_by_tag_name('a').get_attribute('a')
    #          for element in article_elements]
    # TODO: Running with O(2n) right now; consolidate to not need to postproc links
    links_to_recipes = []
    article_elements = driver.find_elements_by_class_name(recipe_link_class)
    for element in article_elements:
        link_holder = element.find_element_by_tag_name('a')
        links_to_recipes.append(link_holder.get_attribute('href'))

    # now process each recipe and get the the link to the photos
    print('{} recipes found. Collecting links to photos page for each recipe.'
          .format(len(links_to_recipes), end=' '))
    links_to_photos = []
    for recipe_link in links_to_recipes:
        # retrieve the page
        get_page(driver, recipe_link, By.CLASS_NAME, photo_strip_class, timeout)
        # photo strip has the link to the photos
        photo_strip = driver.find_element_by_class_name('photo-strip__items')
        # <a> elements have the links to the photos
        a_elements = photo_strip.find_elements_by_tag_name('a')
        while a_elements:
            link_holder = a_elements.pop()
            link = link_holder.get_attribute('href')
            if re.match(RE_RECIPE_PHOTOS, link):
                # we found a valid link; stop since they all link to the same photos
                links_to_photos.append(link)
                break
        print('.', end=' ')  # hinting on the progress it's making

    # the element holding all of the photos is a <ul> element, but the <li> elements
    # are holding <img> elements with the 'src' attribute that holds the link to the
    # images want
    print('{} photo links found. Collecting individual photo links.'
          .format(len(links_to_photos), end=' '))
    photo_links = []
    for link_to_photo in links_to_photos:
        get_page(driver, link_to_photo, By.CLASS_NAME, photos_band_class, timeout)
        photos_band = driver.find_element_by_class_name(photos_band_class)
        img_elements = photos_band.find_elements_by_tag_name('img')
        for img in img_elements:
            link = img.get_attribute('data-original-src')
            if type(link) == str:
                if link.startswith(IMG_LINK_DOMAIN):
                    photo_links.append(link)
        print('.', end=' ')

    print('Saved photo', end=' ')
    for photo_link in photo_links:
        res = requests.get(photo_link)
        with open('img/chicken_wing_{}.jpg'.format(photo_id), 'wb') as in_file:
            in_file.write(res.content)
        print(photo_id, end=' ')
        photo_id += 1

    print()
    page_num += 1
driver.quit()
