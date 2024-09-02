from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests

from config import *

# Get Profile uuid of OctoBrowser
def fnGetUUID():
    response_octo = requests.request("GET", OCTO_SEARCH_URL, headers=OCTO_HEADER)
    data_uuid = response_octo.json()
    uuid = data_uuid.get('data')[0]['uuid']
    return uuid

# Get Debug Port
# Profile id is uuid from fnGetUUID()
def get_debug_port(profile_id):
    data = requests.post(
        f'{LOCAL_API}/start', json={'uuid': profile_id, 'headless': False, 'debug_port': True}
    ).json()
    print(data)
    return data['debug_port']

# Create webdriver
# port is from get_debug_port()
def get_webdriver(port):
    chrome_options = Options()
    chrome_options.add_experimental_option('debuggerAddress', f'127.0.0.1:{port}')
    # Use Service to specify the path to ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def fnGetElementXpath(driver, flag, xpath):
    try:
        ele = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        if flag == False:
            return ele
        else:
            ele.click()
    except:
        print(f"fnGetElementXpath() is error because {xpath} can't find")
        return False

def fnGetElementsClass(driver, ClassName):
    try:
        eles = WebDriverWait(driver, 60).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, ClassName)))
        return eles
    except:
        print(f"fnGetElementXpath() is error because {ClassName} can't find")
        return False

