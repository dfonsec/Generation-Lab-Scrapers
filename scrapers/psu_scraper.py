from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import re
import undetected_chromedriver as uc
import pandas as pd
import time


SEARCH_BUTTON = '//*[@id="app-root"]/main/div/dir-directory/section/mat-card/mat-card-content/dir-search-bar/section/mat-form-field/div[1]/div/div[3]/button[2]'
NEXT_BUTTON = '//*[@id="app-root"]/main/div/dir-directory/section/mat-card/mat-card-content/div/div[2]/pagination-controls/pagination-template/nav/ul/li[10]/a'
LETTERS = ['a', 'b', 'c', 'd', 'e', 
           'f', 'g', 'h', 'i', 'j', 
           'k', 'l', 'm', 'n', 'o', 
           'p', 'q', 'r', 's', 't', 
           'u', 'v', 'w', 'x', 'y', 'z']
URL = "https://directory.psu.edu/"




def obtain_data():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("start-maximized")
    driver = uc.Chrome(Options=chrome_options)
    driver.get(URL)
    
    time.sleep(5)
    
    
    
    
    return

def input_text(driver, text):
    
    search_field = driver.find_element(By.XPATH, SEARCH_BUTTON)
    search_field.send_keys(text)
    
    return

def click_button(driver, path):
    button_element = driver.find_element(By.XPATH, path)
    button_element.click()
    
    return

def get_info_panels(driver):
    info_panels = driver.find_elements(By.TAG_NAME, "dir-info-panel")
    return info_panels
    
    
    
    












# def main():
#     return
    
    
# if __name__ == "__main__":
#     main()