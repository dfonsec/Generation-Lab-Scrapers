from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import re
import pandas as pd
import time

SEARCH_FIELD = '//*[@id="mat-input-0"]'
SEARCH_BUTTON = '//*[@id="app-root"]/main/div/dir-directory/section/mat-card/mat-card-content/dir-search-bar/section/mat-form-field/div[1]/div/div[3]/button[2]'
NEXT_BUTTON = '//pagination-controls//li/a[contains(text(), "Next")]'
LETTERS = ['a', 'b', 'c', 'd', 'e', 
           'f', 'g', 'h', 'i', 'j', 
           'k', 'l', 'm', 'n', 'o', 
           'p', 'q', 'r', 's', 't', 
           'u', 'v', 'w', 'x', 'y', 'z']
URL = "https://directory.psu.edu/"


def crawler():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(URL)
    
    result= []
    time.sleep(8)
    for letter in LETTERS:
        print(f"Scraping data for letter: {letter}")
        data = scrape_page_data(driver, letter)
        result.extend(data)  

    return result
    

def scrape_page_data(driver, input):

    result_list = []

    input_text(driver, input)
    click_button(driver, SEARCH_BUTTON)
    
    time.sleep(5)
    
    panel_idx = 0
    while True:
        try:
            time.sleep(2)
            current_panels = get_info_panels(driver)
            for panel in current_panels:
                if not is_student(panel):
                    panel_idx += 1
                    continue
                
                dropdown_button = panel.find_element(By.XPATH, './/span[contains(@class, "mat-expansion-indicator")]')
                dropdown_button.click()
                time.sleep(1)
                data = get_panel_data(panel, panel_idx)
                result_list.append(data)
                panel_idx += 1
            try:
                next_button = driver.find_element(By.XPATH, NEXT_BUTTON)
                if next_button.is_enabled():
                    click_button(driver, NEXT_BUTTON)
                    time.sleep(2) 
                else:
                    print("No more pages.")
                    break
            except TimeoutError:
                print("Timeout Error")
                break
            except NoSuchElementException:
                print("Next button not found on page, terminating process.")
                return result_list
    
        except Exception as e:
                print(f"Unexpected error: {e}")
                break
    
    return result_list

def input_text(driver, text):
    search_field = driver.find_element(By.XPATH, SEARCH_FIELD)
    search_field.clear()  # Clear the text field
    search_field.send_keys(text)  # Enter the new text
    return

def click_button(driver, path):
    button_element = driver.find_element(By.XPATH, path)
    button_element.click()
    
    return

def get_info_panels(driver):
    info_panels = driver.find_elements(By.TAG_NAME, "dir-info-panel")
    return info_panels

def get_page_lim(driver):
    return driver.find_element(By.XPATH, '//*[@id="app-root"]/main/div/dir-directory/section/mat-card/mat-card-content/div/div[2]/pagination-controls/pagination-template/nav/ul/li[9]/a/span[2]').text

def is_student(panel):
    panel_type = panel.find_element(By.CLASS_NAME, "description-sublabel").text
    
    if panel_type[0] == "S":
        return True
    
    return False
    

def get_panel_data(panel, panel_idx):
    panel_name = panel.find_element(By.CLASS_NAME, "description-label").text
    panel_email = panel.find_element(By.XPATH, './/div/section[1]/div[1]/dir-row-display[3]/section/div/a').text
    panel_title = panel.find_element(By.XPATH, './/div/section[1]/div[2]/dir-row-display[1]/section/div/span').text
    panel_campus = panel.find_element(By.XPATH, './/div/section[1]/div[2]/dir-row-display[3]/section/div/span').text
    
    return {'Name': panel_name, 'Email': panel_email, 'Title': panel_title, 'Campus': panel_campus}

def main():
    data_list = crawler()
    if data_list:
        data_df = pd.DataFrame(data_list, columns=['Name', 'Email', 'Title', 'Campus'])
        data_df.to_excel('PSU_DATA.xlsx')
    else:
        print("No data scraped.")
    return 
    
    
if __name__ == "__main__":
    main()