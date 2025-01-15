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
        print("Beginning to scrape:", query)
        init_url = f'https://campdir.apps.mst.edu/cgi-bin/cgiwrap/campdir/directory.pl'
        response = get_data(init_url, "P", session, query)
        anchors = get_profile_links(response)
        page_data = get_user_data(anchors, session)
        
        data.extend(page_data)
    
    return data
        


def get_data(url, req_type, session, query=None):
    
    try:
        if req_type == "G":
            response = session.get(url)
        elif req_type == "P":
            data = configure_data(query)
            response = session.post(url, data=data)
    except:
        print("Response failed:", response.status_code)
        
    
    return response

def configure_data(query):
    return {"name": query, "submit": "Search"}

def get_profile_links(response):
    
    soup = BeautifulSoup(response.text, 'html.parser')
    pattern = re.compile(r'^directory\.pl\?mode=detail(&amp;|&)id=\w+\s*$')
    anchors = soup.find_all('a', href=pattern)
    return anchors

def get_user_data(anchors, session):
    
    result = []
    base_url = "https://campdir.apps.mst.edu/cgi-bin/cgiwrap/campdir/"
    for anchor in anchors:
        href = anchor.get("href").strip()
        curr_url = base_url + href
        user_response = get_data(curr_url, "G", session, None)
        soup = BeautifulSoup(user_response.text, 'html.parser')
        
        if not is_student(soup):
            continue
        parsed_response = parse_user_data(soup)
        result.append(parsed_response)
        
    return result

def parse_user_data(soup):
    table = soup.find("table")
    fonts = table.find_all("font")
    
    try:
        name = fonts[0].get_text()
    except:
        name = None
        
    try:
        email = fonts[-1].find("a").get_text()
    except:
        email = None

    return {"Name": name, "Email": email}


def is_student(soup):
    
    div = soup.find("table")
    category_elem = div.find("u")
    elem_text = category_elem.get_text()
    print(elem_text)
    
    if elem_text[0] !=  "S":
        return False
    else:
        return True
    
    


def main():
    final = run_script(queries)
    print(final)
    print(len(final))
    return 

if __name__ == "__main__":
    main()