from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
import urllib.request

EXTENSION_PATH = os.getcwd() + '\metamaskExtension.crx'
CHROME_DRIVER_PATH = os.getcwd() + '\chromedriver.exe'
EXTENSION_ID = 'nkbihfbeogaeaoehlefnkodbefgpgknn'

def downloadMetamaskExtension():
    print('Setting up metamask extension please wait...')

    url = 'https://xord-testing.s3.amazonaws.com/selenium/10.0.2_0.crx'
    urllib.request.urlretrieve(url, os.getcwd() + '/metamaskExtension.crx')

# def launchSeleniumWebdriver(driverPath):
def launchSeleniumWebdriver():
    print('path', EXTENSION_PATH)
    chrome_options = Options()
    chrome_options.add_extension(EXTENSION_PATH)
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--disable-notifications')
    chrome_service = Service(CHROME_DRIVER_PATH)
    global driver
    # driver = webdriver.Chrome(options=chrome_options, executable_path=driver)
    driver = webdriver.Chrome(options=chrome_options, service=chrome_service)
    time.sleep(15)
    print("Extension has been loaded")
    return driver


def metamaskSetup(recoveryPhrase, password):
    
    driver.switch_to.window(driver.window_handles[1])
    
    # element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Get Started"]'))).click
    element = driver.find_element(By.XPATH, '//button[text()="Get Started"]')
    driver.execute_script('arguments[0].click()', element) 

    element = driver.find_element(By.XPATH, '//button[text()="Import wallet"]')
    driver.execute_script('arguments[0].click()', element) 

    element = driver.find_element(By.XPATH, '//button[text()="No Thanks"]')
    driver.execute_script('arguments[0].click()', element) 

    # driver.find_element(By.XPATH, '//button[text()="Get Started"]').click()
    # driver.find_element(By.XPATH, '//button[text()="Import wallet"]').click()
    # driver.find_element(By.XPATH, '//button[text()="No Thanks"]').click()

    time.sleep(2)

    secret_recovery_phrase = driver.find_element(By.XPATH, '//input')
    secret_recovery_phrase.send_keys(recoveryPhrase)
    
    secret_recovery_phrase.send_keys(Keys.TAB)
    checkbox = driver.switch_to.active_element
    checkbox.send_keys(Keys.TAB)
    
    new_password = driver.switch_to.active_element
    new_password.send_keys(password)
    new_password.send_keys(Keys.TAB)

    confirm_password = driver.switch_to.active_element
    confirm_password.send_keys(password)
    confirm_password.send_keys(Keys.TAB)

    terms_of_use = driver.switch_to.active_element
    terms_of_use.send_keys(Keys.SPACE)
    # inputs = driver.find_element(By.XPATH, "//input")
    # inputs[0].send_keys(recoveryPhrase)
    # inputs[1].send_keys(password)
    # inputs[2].send_keys(password)

    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.first-time-flow__terms'))).click
    # driver.find_element_by_css_selector('.first-time-flow__terms').click()

    element = driver.find_element(By.XPATH, '//button[text()="Import"]')
    driver.execute_script('arguments[0].click()', element) 
    # driver.find_element(By.XPATH, '//button[text()="Import"]').click()

    time.sleep(2)

    element = driver.find_element(By.XPATH, '//button[text()="All Done"]')
    driver.execute_script('arguments[0].click()', element) 
    # driver.find_element(By.XPATH, '//button[text()="All Done"]').click()
    time.sleep(2)

    # closing the message popup after all done metamask screen
    element = driver.find_element(By.XPATH, '//*[@id="popover-content"]/div/div/section/header/div/button')
    driver.execute_script('arguments[0].click()', element) 
    # driver.find_element(By.XPATH, '//*[@id="popover-content"]/div/div/section/header/div/button').click()
    time.sleep(2)
    print("Wallet has been imported successfully")
    time.sleep(5)


def changeMetamaskNetwork(networkName):
    # opening network
    print("Changing network")
    driver.switch_to.window(driver.window_handles[1])
    driver.get('chrome-extension://{}/home.html'.format(EXTENSION_ID))
    print("closing popup")
    time.sleep(2)

    element = driver.find_element(By.XPATH, '//*[@id="popover-content"]/div/div/section/header/div/button')
    driver.execute_script('arguments[0].click()', element) 
    # driver.find_element(By.XPATH, '//*[@id="popover-content"]/div/div/section/header/div/button').click()

    element = driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[1]/div/div[2]/div[1]/div/span')
    driver.execute_script('arguments[0].click()', element) 
    # driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[1]/div/div[2]/div[1]/div/span').click()
    time.sleep(2)
    print("opening network dropdown")

    elem = driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div')
    driver.execute_script('arguments[0].click()', elem) 
    # elem = driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div')
    time.sleep(2)

    change_network = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='" + networkName + "']"))
    )
    driver.execute_script('arguments[0].click()', change_network)
    # change_network.click()
    print(networkName, "is selected")
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(2)
    
    # all_li = elem.find_elements(By.TAG_NAME, 'li')
    # # all_li = elem.find_elements_by_tag_name("li")
    # time.sleep(2)
    # for li in all_li:
    #     text = li.text
    #     if (text == networkName):
    #         li.click()
    #         print(text, "is selected")
    #         time.sleep(2)
    #         driver.switch_to.window(driver.window_handles[0])
    #         time.sleep(3)
    #         return
    time.sleep(2)
    print("Please provide a valid network name")

    driver.switch_to.window(driver.window_handles[1])
    # time.sleep(3)

def favouriteAction(network_url, pool_address):
    driver.get("https://www.dextools.io/app/en/" + network_url + "/pair-explorer/" + pool_address)
    time.sleep(20)
    star_button = driver.find_element(By.CSS_SELECTOR, "button[placement='auto'][class='ng-star-inserted']")
    star_button.click()

    share_button = driver.find_element(By.CSS_SELECTOR, "a.shared-button")
    share_button.click()
    time.sleep(1)
    
    twitter_button = driver.find_element(By.CSS_SELECTOR, "a.btn-twitter")
    twitter_button.click()
    time.sleep(1)
    telegram_button = driver.find_element(By.CSS_SELECTOR, "a.btn-telegram")
    telegram_button.click()
    time.sleep(1)
    reddit_button = driver.find_element(By.CSS_SELECTOR, "a.btn-reddit")
    reddit_button.click()
    time.sleep(1)
    driver.refresh()
    time.sleep(1)
    driver.refresh()

def connectToWallet():
    try:

        modal = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.modal-header")))
        
        # find the close button inside the modal header
        close_button = modal.find_element(By.CSS_SELECTOR, "button[type='button'][class='close'][aria-label='Close']")

        if close_button:
            
            print('Close button exists')
            close_button.click()

        else:
            print('Close button does not exist')

        
    except:
        print("Failed to find or click the close button")

        #wait for bottom close button to appear and click it
    try:

        modal = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.sub-header")))
        
        # find the close button inside the modal header
        close_button = modal.find_element(By.CSS_SELECTOR, "button[type='button'][class='close'][aria-label='Close']")

        if close_button:
            
            print('Close button exists')
            close_button.click()

        else:
            print('Close button does not exist')

    
        
    except:
        print("Failed to find or click the close button")

    try:
        element = driver.find_element(By.XPATH, '//button[text()="Connect"]')
        driver.execute_script('arguments[0].click()', element) 
    except:
        print("Failed to find or click the connect button")
    time.sleep(2)
    try:
        element = driver.find_element(By.XPATH, '//button[text()=" Connect "]')
        driver.execute_script('arguments[0].click()', element) 
    except:
        print("Failed to find or click the connect button")
    time.sleep(5)

    modal = driver.switch_to.active_element
    
    
    # metamask_button = modal.find_element(By.XPATH, "/button")
    # driver.execute_script('arguments[0].click()', metamask_button) 
    
    time.sleep(3)

    # modal = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.modal-content")))
    
    modal.send_keys(Keys.TAB)
    element = driver.switch_to.active_element
    element.send_keys(Keys.TAB)

    element = driver.switch_to.active_element
    element.send_keys(Keys.TAB)

    element = driver.switch_to.active_element
    element.send_keys(Keys.TAB)

    element = driver.switch_to.active_element
    element.send_keys(Keys.ENTER)
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[1])
    # element = driver.switch_to.active_element
    # element.send_keys(Keys.TAB)
    # element = driver.switch_to.active_element
    # element.send_keys(Keys.TAB)
    # element = driver.switch_to.active_element
    # element.send_keys(Keys.TAB)
    # element.send_keys(Keys.ENTER)
    try:
        element = driver.find_element(By.XPATH, '//button[text()="Next"]')
        driver.execute_script('arguments[0].click()', element) 
    except:
        print("Failed to find or click the connect button")
    time.sleep(1)

    try:
        element = driver.find_element(By.XPATH, '//button[text()="Connect"]')
        driver.execute_script('arguments[0].click()', element) 
    except:
        print("Failed to find or click the connect button")
    time.sleep(2)
    
    driver.switch_to.window(driver.window_handles[0])
    try:
        element = driver.find_element(By.XPATH, '//button[text()=" Verify wallet "]')
        driver.execute_script('arguments[0].click()', element) 
    except:
        print("Failed to find or click the connect button")
    time.sleep(15)

    driver.switch_to.window(driver.window_handles[1])

    try:
        element = driver.find_element(By.XPATH, '//button[text()="Sign"]')
        driver.execute_script('arguments[0].click()', element) 
    except:
        print("Failed to find or click the connect button")
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[0])
    
def connectToWebsite():
    time.sleep(3)

    # driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    time.sleep(5)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(3)
    element = driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[4]/div[2]/button[2]').click()
    # driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[4]/div[2]/button[2]')
    driver.execute_script('arguments[0].click()', element)
    time.sleep(1)
    element = driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div[2]/footer/button[2]').click()
    # driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div[2]/footer/button[2]')
    driver.execute_script('arguments[0].click()', element)
    time.sleep(3)
    print('Site connected to metamask')
    print(driver.window_handles)
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(3)


def confirmApprovalFromMetamask():
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    time.sleep(10)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(10)
    # confirm approval from metamask
    driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[4]/footer/button[2]').click()
    time.sleep(12)
    print("Approval transaction confirmed")

    # switch to dafi
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)


def rejectApprovalFromMetamask():
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    time.sleep(10)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(10)
    # confirm approval from metamask
    driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[4]/footer/button[1]').click()
    time.sleep(8)
    print("Approval transaction rejected")

    # switch to dafi
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)
    print("Reject approval from metamask")


def confirmTransactionFromMetamask():
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    time.sleep(10)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(10)

    # # confirm transaction from metamask
    driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[3]/div[3]/footer/button[2]').click()
    time.sleep(13)
    print("Transaction confirmed")

    # switch to dafi
    driver.switch_to.window(driver.window_handles[0])

    time.sleep(3)


def rejectTransactionFromMetamask():
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    time.sleep(5)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(5)
    # confirm approval from metamask
    driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[3]/div[3]/footer/button[1]').click()
    time.sleep(2)
    print("Transaction rejected")

    # switch to web window
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)

def addToken(tokenAddress):
    # opening network
    print("Adding Token")
    driver.switch_to.window(driver.window_handles[1])
    driver.get('chrome-extension://{}/home.html'.format(EXTENSION_ID))
    print("closing popup")
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="popover-content"]/div/div/section/header/div/button').click()

    # driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[1]/div/div[2]/div[1]/div/span').click()
    # time.sleep(2)

    print("clicking add token button")
    driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[4]/div/div/div/div[3]/div/div[3]/button').click()
    time.sleep(2)
    # adding address
    driver.find_element_by_id("custom-address").send_keys(tokenAddress)
    time.sleep(10)
    # clicking add
    driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[4]/div/div[2]/div[2]/footer/button[2]').click()
    time.sleep(2)
    # add tokens
    driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[4]/div/div[3]/footer/button[2]').click()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)

def signConfirm():
    print("sign")
    time.sleep(3)

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    time.sleep(5)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(3)
    driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[3]/button[2]').click()
    time.sleep(1)
    # driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div[2]/footer/button[2]').click()
    # time.sleep(3)
    print('Sign confirmed')
    print(driver.window_handles)
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)


def signReject():
    print("sign")
    time.sleep(3)

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    time.sleep(5)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(3)
    driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[3]/button[1]').click()
    time.sleep(1)
    # driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div[2]/footer/button[2]').click()
    # time.sleep(3)
    print('Sign rejected')
    print(driver.window_handles)
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)
