from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium_metamask_automation
import configparser
from mnemonic import Mnemonic

mnemo = Mnemonic("english")

# Read the settings file
while(1) :
    try:
        config = configparser.ConfigParser()
        config.readfp(open('setting.ini'))

        networkName = config.get('DEFAULT', 'network')
        networkUrl = config.get('DEFAULT', 'network_url')
        # poolAddress = config.get('DEFAULT', 'pool')
        poolAddress = '0x04f01db076c85ea9a27c84c83e13b166fe9db95c'
        driver = selenium_metamask_automation.launchSeleniumWebdriver()

        words = mnemo.generate(strength=128)
        # seed = mnemo.to_seed(words, passphrase="") 
        # entropy = mnemo.to_entropy(words)

        selenium_metamask_automation.metamaskSetup(words, "QWERasdf!@#$")

        # selenium_metamask_automation.changeMetamaskNetwork(networkName)

        driver.switch_to.window(driver.window_handles[0])
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        driver.get("https://dextools.io")

        selenium_metamask_automation.connectToWallet()
        # try:
        #     modal = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.modal-header")))
            
        #     # find the close button inside the modal header
        #     close_button = modal.find_element(By.CSS_SELECTOR, "button[type='button'][class='close'][aria-label='Close']")

        #     if close_button:
                
        #         print('Close button exists')
        #         close_button.click()

        #     else:
        #         print('Close button does not exist')

                
        # except:
        #     print("Failed to find or click the close button")

        #         #wait for bottom close button to appear and click it
        # try:

        #     modal = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.sub-header")))
            
        #     # find the close button inside the modal header
        #     close_button = modal.find_element(By.CSS_SELECTOR, "button[type='button'][class='close'][aria-label='Close']")

        #     if close_button:
                
        #         print('Close button exists')
        #         close_button.click()

        #     else:
        #         print('Close button does not exist')


            
        # except:
        #     print("Failed to find or click the close button")

        selenium_metamask_automation.favouriteAction(networkUrl, poolAddress)
        driver.quit()
        # selenium_metamask_automation.connectToWebsite()

        # selenium_metamask_automation.addToken("0xdAC17F958D2ee523a2206206994597C13D831ec7")
    except:
        print('reloading')
