import os
from pdb import set_trace as st

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

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
    options.add_argument(' — incognito')
    #options.add_argument('headless')

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

# define webpage to scrape
brisket_url = "https://www.allrecipes.com/search/results/?wt=brisket&sort=re&page={}"
#  for testing
brisket_url = "https://www.allrecipes.com/search/results/?wt=chicken&sort=re&page={}"
timeout = 10
page_num = 1
recipe_link_class_name = 'grid-card-image-container'

#while True:
browser.get(brisket_url.format(page_num))

try:
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((
        By.CLASS_NAME, recipe_link_class_name)))
except TimeoutException:
    print('Timed out waiting for page to load')
    browser.quit()

# grab the element with the recipe link
# links = [element.find_element_by_tag_name('a').get_attribute('a')
#          for element in article_elements]
links = []
article_elements = browser.find_elements_by_class_name(recipe_link_class_name)
for element in article_elements:
    link_holder = element.find_element_by_tag_name('a')
    links.append(link_holder.get_attribute('href'))

st()
    #break

