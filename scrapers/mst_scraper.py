import requests
from bs4 import BeautifulSoup
import pandas as pd
from multiprocessing import Pool
import re



queries = ["zal"]

def run_script(queries):
    session = requests.Session()
    data = []
    for query in queries:
        init_url = f'https://campdir.apps.mst.edu/cgi-bin/cgiwrap/campdir/directory.pl'
        response = get_data(init_url, "P", session, query)
        anchors = get_profile_links(response)

    

def get_data(url, req_type, session, query=None):
    
    if req_type == "G":
        response = session.get(url)
        
    elif req_type == "P":
        data = configure_data(query)
        response = session.post(url, data=data)
    
    return response

def configure_data(query):
    
    data = {"name": query,
            "submit": "Search"
            }
    
    return data

def get_profile_links(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    
    pattern = re.compile(r'^directory\.pl\?mode=detail(&amp;|&)id=\w+\s*$')

    
    anchors = soup.find_all('a', href=pattern)
    
    return anchors

def get_user_data(anchors, session):
    
    result = []
    base_url = "https://campdir.apps.mst.edu/cgi-bin/cgiwrap/campdir/"
    for anchor in anchors:
        
        href = anchor.get("href")
        curr_url = base_url + href
        user_response = get_data(curr_url, "G", session, None)
        result.append(parse_user_data(user_response))
        
    return result

def parse_user_data(user_response):
    
    soup = BeautifulSoup(user_response.text, 'html.parser')
    table = soup.find("table")
    fonts = table.find_all("font")

    name = fonts[0].get_text
    
    email = fonts[-1].find("a").get_text()
    
    user_data = {"Name": name,
                 "Email": email}
    
    return user_data
    


def main():
    
    session = requests.Session()
    url = 'https://campdir.apps.mst.edu/cgi-bin/cgiwrap/campdir/directory.pl'
    
    response = session.post(url, data=data)
    anchors = get_profile_links(response)
    anchor = anchors[0]
    curr_url = "https://campdir.apps.mst.edu/cgi-bin/cgiwrap/campdir/directory.pl?mode=detail&amp;id=mia5xb" 
    user_response = get_data(curr_url, "G", session, None)
    data = BeautifulSoup(user_response.text, 'html.parser')
    table = data.find("table")
    fonts = table.find_all("font")
    print(fonts[0].get_text())
    print(fonts[-1].find("a").get_text())

    return 

if __name__ == "__main__":
    main()