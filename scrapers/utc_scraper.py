import requests
from bs4 import BeautifulSoup
import re

# Run script with a bunch of queries

# Retrieve information

# Parse response 



# For each query, retrieve the entire list of hrefs that lead us directly to user links
    # build a mass link of user links
    # retrieve the user info via get requests
    


def extract_urls(soup):
    # Assuming soup is the entire html
    
    # Obtain only the rows that contain data
    links = []
    rows = soup.find_all('tr', {"id": re.compile(r'^F')})
    base_url = 'https://people.utc.edu/eGuide/servlet/'
    result = [base_url + parse_anchor(row) for row in rows]
    
    return result
  
def parse_anchor(row):
    anchor_url = row.get("onclick")
    match = re.search(r"getDetail\('([^']+)'", anchor_url)
    
    if match:
        anchor_link = match.group(1)
        
    return anchor_link

def main():
    session = requests.Session()
    url = 'https://people.utc.edu/eGuide/servlet/eGuide?User.context=qtlsRhrljmKm&Action=List.get&Object.uid=USER&max=400&Search.attributes=,LASTNAME,EDUPERSONNICKNAME,EDUPERSONPRIMARYAFFILIATION&Primary.sortkey=LASTNAME&Secondary.sortkey=EDUPERSONNICKNAME'
    data = {"attr1": "LASTNAME", "crit1": "sw", "val1": "a", "x": "43", "y": "23"}
    response = session.post(url, data=data)
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = extract_urls(soup)
    print(rows[:5])
    # soup = BeautifulSoup(response_user.text, 'html.parser')
    # name = soup.find("td", {"class": "formhead2"})
    # values = soup.find_all("td", {"class": "ValueText"})
    # data = []
    # data.append(' '.join(name.get_text().split()))
    # data.extend([value.get_text().strip() for value in values])
    
    # print(data)
    
    
    return



if __name__ == "__main__":
    main()