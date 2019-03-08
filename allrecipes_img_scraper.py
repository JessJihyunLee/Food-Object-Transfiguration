import os
from pdb import set_trace as st

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

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
browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

# define webpage to scrape
brisket_url = "https://www.allrecipes.com/search/results/?wt=brisket&sort=re&page={}"
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

    #break
