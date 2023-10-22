from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium_metamask_automation
import configparser
import asyncio
from mnemonic import Mnemonic

mnemo = Mnemonic("english")


# Read the settings file
while(1) :
    try:
        config = configparser.ConfigParser()
        # config.readfp(open('setting.ini'))

        # networkName = config.get('DEFAULT', 'network')
        # networkUrl = config.get('DEFAULT', 'network_url')
        networkUrl = 'ether'
        # poolAddress = config.get('DEFAULT', 'pool')
        poolAddress = '0x04f01db076c85ea9a27c84c83e13b166fe9db95c'
        driver = selenium_metamask_automation.launchSeleniumWebdriver()

        words = mnemo.generate(strength=128)
        # seed = mnemo.to_seed(words, passphrase="") 
        # entropy = mnemo.to_entropy(words)

        selenium_metamask_automation.metamaskSetup(words, "QWERasdf!@#$")

        # selenium_metamask_automation.changeMetamaskNetwork(networkName)

        selenium_metamask_automation.switch_window(0)
        selenium_metamask_automation.switch_window(1)
        driver.close()
        selenium_metamask_automation.switch_window(0)

        driver.get("https://dextools.io")

        selenium_metamask_automation.connectToWallet()
        selenium_metamask_automation.favouriteAction(networkUrl, poolAddress)
        driver.quit()
        
    except Exception as e:
        print('reloading', e)



