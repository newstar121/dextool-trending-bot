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
    time.sleep(1)
    print("Extension has been loaded")
    return driver

def find_element_available(element_criteria):
    flag = 1
    while(flag):
        try:
            element = driver.find_element(By.XPATH, element_criteria)
            driver.execute_script('arguments[0].click()', element)
            flag = 0
        except Exception as e:
            flag = 1
            time.sleep(1)

def find_element_css(element_criteria):
    flag = 1
    while(flag):
        try:
            element = driver.find_element(By.CSS_SELECTOR, element_criteria)
            element.click()
            flag = 0
        except Exception as e:
            flag = 1
            time.sleep(1)
        
def find_element_keyboard(element_criteria, key):
    flag = 1
    element = ''
    while(flag):
        try:
            element = driver.find_element(By.XPATH, element_criteria)
            element.send_keys(key)
            flag = 0
        except Exception as e:
            flag = 1
            time.sleep(1)
    return element

def switch_window(index) :
    flag = 1
    while(flag):
        try:
            driver.switch_to.window(driver.window_handles[index])
            flag = 0
        except:
            time.sleep(1)
    time.sleep(0.5)

def metamaskSetup(recoveryPhrase, password):
    
    switch_window(1)
    
    find_element_available('//button[text()="Get Started"]')
    find_element_available('//button[text()="Import wallet"]')
    find_element_available('//button[text()="No Thanks"]')    

    secret_recovery_phrase = find_element_keyboard('//input', recoveryPhrase)
    
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
    
    find_element_available('//button[text()="Import"]')
    find_element_available('//button[text()="All Done"]')
    find_element_available('//*[@id="popover-content"]/div/div/section/header/div/button')
    
    print("Wallet has been imported successfully")

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
    # time.sleep(2)
    print("opening network dropdown")

    elem = driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div')
    driver.execute_script('arguments[0].click()', elem) 
    # elem = driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div')
    # time.sleep(2)

    change_network = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='" + networkName + "']"))
    )
    driver.execute_script('arguments[0].click()', change_network)
    # change_network.click()
    print(networkName, "is selected")
    # time.sleep(2)
    driver.switch_to.window(driver.window_handles[1])
    # time.sleep(2)
    
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
    # time.sleep(2)
    print("Please provide a valid network name")

    driver.switch_to.window(driver.window_handles[1])
    # time.sleep(3)

def favouriteAction(network_url, pool_address):
    time.sleep(1)
    try:
        
        driver.get("https://www.dextools.io/app/en/" + network_url + "/pair-explorer/" + pool_address)
        time.sleep(1)
        find_element_css(".favorite-button button")
        
        flag = 1
        while(flag):
            try:
                star_button1 = driver.find_elements(By.CSS_SELECTOR, ".popover-body fa-icon.ng-fa-icon.ng-star-inserted")
                star_button1[1].click()
                flag = 0
            except:
                flag = 1
                time.sleep(1)

        time.sleep(1)  
        flag = 1
        while(flag):
            try:
                copy_button = driver.find_elements(By.CSS_SELECTOR, "a.text-muted")
                copy_button[0].click()
                copy_button[1].click()
                flag = 0
            except:
                flag = 1
                time.sleep(1)

        time.sleep(1)  
        find_element_css("a.shared-button") 
        time.sleep(1)  
        find_element_css("a.btn-twitter")   
        time.sleep(1)  
        find_element_css("a.btn-telegram")   
        time.sleep(1)  
        find_element_css("a.btn-reddit")   
        
        driver.refresh()
        time.sleep(1)
        driver.refresh()

    except Exception as e:
        print(e)    

def connectToWallet():
    time.sleep(1)
    print('navigating dextools')
    flag = 1
    while(flag):
        try:

            modal = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.modal-header")))
            
            # find the close button inside the modal header
            close_button = modal.find_element(By.CSS_SELECTOR, "button[type='button'][class='close'][aria-label='Close']")

            close_button.click()
            flag = 0
            
        except:
            print("Failed to find or click the close button")
            time.sleep(1)

    flag = 1
    while(flag):    
        try:
            modal = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.sub-header")))
            # find the close button inside the modal header
            close_button = modal.find_element(By.CSS_SELECTOR, "button[type='button'][class='close'][aria-label='Close']")
            close_button.click()
            flag = 0
        except:
            print("Failed to find or click the close button")
            time.sleep(1)

    
    find_element_available('//button[text()="Connect"]')
    find_element_available('//button[text()=" Connect "]')
    time.sleep(10)
    
    modal = driver.switch_to.active_element
    
    modal.send_keys(Keys.TAB)
    element = driver.switch_to.active_element
    element.send_keys(Keys.TAB)

    element = driver.switch_to.active_element
    element.send_keys(Keys.TAB)

    element = driver.switch_to.active_element
    element.send_keys(Keys.TAB)

    element = driver.switch_to.active_element
    element.send_keys(Keys.ENTER)
    
    switch_window(1)
    
    find_element_available('//button[text()="Next"]')

    find_element_available('//button[text()="Connect"]')

    switch_window(0)

    find_element_available('//button[text()=" Verify wallet "]')
    
    switch_window(1)

    find_element_available('//button[text()="Sign"]')
    
    switch_window(0)

    print('wallet connection finished')
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
