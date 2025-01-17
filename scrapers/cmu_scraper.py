import requests
from bs4 import BeautifulSoup
import re



def submit_query(query, session):
    
    data = {"search": query,
            "action": "Search",
            "searchtype": "basic",
            "activetab": "basic"}
    response = session.post(query, data)
    
    if response.status_code == 200:
        return response
    else:
        print("Error getting response, status code:", response.status_code)
        
    return

def get_user_links(response):
    
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find("div", {"class": "table-container"})
    table_anchors = table.find_all("a")
    
    user_links = [anchor.get("href").strip() for anchor in table_anchors]
    base_url = 'https://directory.andrew.cmu.edu/'
    user_links =  [base_url + anchor for anchor in user_links]
    
    return user_links
    
def get_user_data(links, session):
    data = []
    
    for link in links:
        response = session.get(link)
        data.extend(parse_user_data(response))
        

        
    
    return
    
def parse_user_data(user_page):
    soup = BeautifulSoup(user_page.text, 'html_parser')

    # Get the name
    content_div = soup.find("div", {"style":"padding-top: 50px;"})
    
    user_name = content_div.find("h1", {"id": "listing"}).get_text()
    # Get the email
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    email = re.findall(email_pattern, user_page.text)[0]
    
    # Get Departmental Affiliations
    
    # Get Student Class Level
    
    return

def extract_email(soup):
    return
    
    
    

def main():
    session = requests.Session()
    data = {
        "search": "aa",
        "action": "Search",
        "searchtype": "basic",
        "activetab": "basic"
    }
    request_url = f'https://directory.andrew.cmu.edu/'
    response = requests.post(request_url, data=data)
    print("The status code is:", response.status_code)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find("div", {"class": "table-container"})
    table_data = table.find_all("td")
    table_anchors = table.find_all("a")
    table_links = [anchor.get("href").strip() for anchor in table_anchors]
    example_anchor = table_links[0]
    request_url = f'https://directory.andrew.cmu.edu/{example_anchor}'
    response = requests.get(request_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, response.text)[0]
    print(emails)

    return

if __name__ == "__main__":
    main()