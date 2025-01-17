import requests
from bs4 import BeautifulSoup
import re



def main():
    session = requests.Session()
    data = {
        "search": "aa",
        "action": "Search",
        "searchtype": "basic",
        "activetab": "basic"
    }
    request_url = 'https://directory.andrew.cmu.edu/index.cgi'
    response = requests.post(request_url, data=data)
    print("The status code is:", response.status_code)
    
    print(response.text)
    return

if __name__ == "__main__":
    main()