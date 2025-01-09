from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

URL = 'https://www.depts.ttu.edu/english/about/people/_graduate_students/index.php'

def scrape_page_data():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome()
    driver.get(URL)

    data= []
    table_rows = driver.find_elements(By.TAG_NAME, "tr")
    
    
    for i, row in enumerate(table_rows):
        if i == 0:
            continue
        row_data = row.find_elements(By.TAG_NAME, "td")
        data.append({"Name": row_data[0].text, "Email": row_data[1].text, "Area": row_data[2].text})
                    
    return data
    
        
def main():
    student_data = scrape_page_data()
    student_df = pd.DataFrame(student_data, columns=['Name', 'Email', 'Area'])
    student_df.to_excel("TTU_DATA.xlsx", index=False)
    

    return

if __name__ == "__main__":
    main()