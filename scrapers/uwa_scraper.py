import requests
from bs4 import BeautifulSoup
import pandas as pd

FIRST_ROW = 0
LAST_ROW = 10

letter = 'a'
target_url = f'https://directory.uwa.edu/searchstudent.aspx?searchName={letter}'

def scrape_page_data(target_url):

    data = []
    table_rows = parse_html(target_url, 'tr')
    for i, row in enumerate(table_rows):
        if i == FIRST_ROW:
            continue
        elif i == LAST_ROW:
            break
        
        try:
            row_data = get_row_data(row)
            data.append({"Name": row_data[0].text, 
                         "Class": row_data[1].text, 
                         "Email": get_email(row_data[2])})
            
        except Exception as e: 
            print(f"Error processing row {i}: {e}")
            break    

    return data

def get_email(email_element):
    email_tag = email_element.find_all("a")
    email_link = email_tag[0].get("href")
    response = requests.get(f'https://directory.uwa.edu/{email_link}')
    
    if response.status_code == 200:
        html_content = response.text
        
        soup = BeautifulSoup(html_content, 'html.parser')
        td_elements = soup.find_all('td')
        
        email_text = td_elements[1].text
        return email_text
    else:
        print(f"Failed to fetch the page. Status code {response.status_code}")
        
def get_page_html(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        html_content = response.text
        
        return html_content
    else:
        print(f"Failed to fetch the page. Status code {response.status_code}")
        return None
    
def parse_html(url, element):
    
    html = get_page_html(url)
    soup = BeautifulSoup(html, 'html5lib')
    elements = soup.find_all(f'{element}')
        
    return elements

def get_row_data(row_html):
    row_data = row_html.find_all("td")
    return row_data

def get_page_links():
    content = get_page_html(target_url)
    soup = BeautifulSoup(content, 'html5lib')
    element_tr = soup.find("tr", {"class": "GridPager"})
    page_buttons = element_tr.find_all("a")
    print(page_buttons)
    
    return
    

def main():
    
    return

if __name__ == "__main__":
    main()

    
    
        





