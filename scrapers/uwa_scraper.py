import requests
from bs4 import BeautifulSoup
import pandas as pd
from multiprocessing import Pool

FIRST_ROW = 0
LAST_ROW = 11

LETTERS = ['a', 'b', 'c', 'd', 'e', 
           'f', 'g', 'h', 'i', 'j', 
           'k', 'l', 'm', 'n', 'o', 
           'p', 'q', 'r', 's', 't', 
           'u', 'v', 'w', 'x', 'y', 'z']



def run_script():
    data = []
      
    with Pool(processes=6) as pool:
        data = pool.map(scrape_all_pages_for_letter, LETTERS)
    
    return [item for sublist in data for item in sublist]

def scrape_all_pages_for_letter(letter):
    print("Beginning to scrape letter:", letter)
    target_url = f'https://directory.uwa.edu/searchstudent.aspx?searchName={letter}'
    return scrape_all_pages(target_url)
        
 
def scrape_all_pages(target_url):
    
    session = requests.Session()
    html_init = get_page_html(target_url, session=session)
    soup = BeautifulSoup(html_init, 'html5lib')
    
    # Get pagination links
    data = []
    for i in range(1, 1000):
        if i == 1:
            data.extend(scrape_page_data(soup, session))
        else:
            try:
                page_data = get_form_data(soup, i)
                response = session.post(target_url, data=page_data)
                
                if response.status_code != 200:
                    break
                soup = BeautifulSoup(response.text, 'html5lib')
                data.extend(scrape_page_data(soup, session))
                
            except Exception as e:
                print("Error Encountered:", e)
                break
   
    return data
        

def scrape_page_data(soup, session):

    data = []
    table_rows = parse_html(soup, 'tr')

    for i, row in enumerate(table_rows):
        if i == FIRST_ROW:
            continue
        elif i == LAST_ROW:
            break
        
        try:
            row_data = get_row_data(row)
            data.append({"Name": row_data[0].text, 
                         "Class": row_data[1].text, 
                         "Email": get_email(row_data[2], session)})
            
        except Exception as e: 
            print(f"Error processing row {i}: {e}")
            break    

    return data

def get_email(email_element, session):
    email_tag = email_element.find_all("a")
    email_link = email_tag[0].get("href")
    response = session.get(f'https://directory.uwa.edu/{email_link}')
    
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        td_elements = soup.find_all('td')
        
        email_text = td_elements[1].text
        return email_text
    else:
        print(f"GET EMAIL Failed to fetch the page. Status code {response.status_code}")
        
def get_form_data(soup, page_num):
      
    event_target = 'ctl00$ContentPlaceHolder1$GridViewStudent'
    event_argument = f'Page${page_num}'
    view_state = soup.find("input", {"name": "__VIEWSTATE"})["value"]
    vs_gen = soup.find("input", {"name": "__VIEWSTATEGENERATOR"})["value"]
    event_val = soup.find("input", {"name": "__EVENTVALIDATION"})["value"]
    
    data = {
        "__EVENTTARGET": event_target,
        "__EVENTARGUMENT": event_argument,
        "__VIEWSTATE": view_state,
        "__VIEWSTATEGENERATOR": vs_gen,   
        "__EVENTVALIDATION": event_val,
    }
    return data

        
def get_page_html(url, session=None, data=None):
    if session is None:
        session = requests.Session()  
    
    if data:
        response = session.post(url, data=data)  
    else:
        response = session.get(url)  

    if response.status_code == 200:
        return response.text
    else:
        print(f"GET PAGE HTML Failed to fetch the page. Status code {response.status_code}")
        return None

    
def parse_html(soup, element):
    elements = soup.find_all(f'{element}')
        
    return elements

def get_row_data(row_html):
    row_data = row_html.find_all("td")
    return row_data

def main():
    
    final_data = run_script()
    final_df = pd.DataFrame(final_data, columns=['Name', 'Class', 'Email'])
    final_df.to_excel("UWA_DATA.xlsx")
    return 

if __name__ == "__main__":
    main()



    
    
        





