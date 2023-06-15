import requests
import bs4
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import time
import json


def creds(source):
    loginCreds= {}
    with open("/home/shadarien/programming/pythonTools/destiny2_bots/scripts/browserAutomation/login_credentials.json",'r') as f:
        loginDetails = json.load(f)
    
    #setting a dictionary for logins so that i can expand upon this later
    loginCreds["Xbox"] = loginDetails["Xbox"]

    return loginCreds

def login(email,password):
    current_email = email
    current_password = password
    xbox_panel = "//*[@id=\"user-container\"]/div/div[3]/a[2]/div"
    try:
        engine.find_element(by=By.XPATH, value = (xbox_panel)).click()
        engine.find_element(by=By.NAME,value= "loginfmt").send_keys(email)
        engine.find_element(by=By.ID,value="idSIButton9").click()
        engine.find_element(by=By.NAME,value="passwd").send_keys(password)
        time.sleep(1)
        engine.find_element(by=By.ID,value="idSIButton9").click()
        time.sleep(8)
    except:
        login(current_email,current_password)

def navigate_roll_appraisal():
    counter = 0 
    previousMessage =""
    executed = True
    engine.get("https://www.light.gg/god-roll/roll-appraiser/")
    filter = "//*[@id=\"new-sidebar\"]/ul[1]/li[2]/i"
    engine.find_element(by=By.XPATH,value=filter).click()

    time.sleep(5)
        #   Best Possible Rank
    for i in range(3,5):
        engine.find_element(by=By.XPATH,value=f"//*[@id=\"filters-list\"]/ul/li[8]/ul/li[5]/div/span[{i}]").click()

#    Equipped Popularity Rank # 
    for i in range(3,5):
        engine.find_element(by=By.XPATH,value=f"//*[@id=\"filters-list\"]/ul/li[8]/ul/li[3]/div/span[{i}]").click()

    while (executed):
        #open each panel
        weaponBreakdowns = engine.find_elements(by=By.CSS_SELECTOR, value="h2.collapsed")
        for i in weaponBreakdowns:
            i.click()

        all_locked_weapons = engine.find_elements(by=By.CSS_SELECTOR, value='i.fa.pull-right.fa-unlock')
        for weapons in all_locked_weapons:
            try:
                weapons.click()
                counter+=1
            except:
                if (previousMessage != f"Items Locked: {counter}"):
                    previousMessage = f"Items Locked: {counter}"
                    print(previousMessage)
                #at the end, click the sync button and do it again
                syncButton = engine.find_element(by=By.CSS_SELECTOR, value="i.fa.fa-refresh")
            try:
                syncButton.click()
            except:
                pass
    




chromePath = "/usr/bin/google-chrome"
chromeDriver = "/home/shadarien/programming/pythonTools/destiny2_bots/scripts/browserAutomation/chromedriver" 
site = "https://www.light.gg/signin/bungie/?returnURL=%2f"
options = Options()
options.add_argument("--headless")
engine = webdriver.Chrome(executable_path=chromeDriver,options=options)

engine.get(site)
time.sleep(2)
login_credentials = creds("Xbox")
email = login_credentials["Xbox"]["email"]
passwd = login_credentials["Xbox"]["password"]

login(email,passwd)
time.sleep(10)
navigate_roll_appraisal()
time.sleep(90)

engine.close()