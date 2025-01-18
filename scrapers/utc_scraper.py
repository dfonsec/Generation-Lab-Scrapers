import requests
from bs4 import BeautifulSoup
import re
import pandas as pd 
# Run script with a bunch of queries

# Retrieve information

# Parse response 



# For each query, retrieve the entire list of hrefs that lead us directly to user links
    # build a mass link of user links
    # retrieve the user info via get requests
    
    
    
def make_request(url, req_type, session, data=None):

    if req_type == "G":
        try:
            response = session.get(url)
        except Exception as e:
            print(f"Encountered error, {e}")
    elif req_type == "P":
        try:
            response = session.post(url, data=data)
        except Exception as e:
            print(f"Encountered error, {e}")
    
    response_soup = BeautifulSoup(response.text, 'html.parser')
    
    return response_soup
            
        
def extract_urls(soup):
    # Assuming soup is the entire html
    
    # Obtain only the rows that contain data
    links = []
    rows = soup.find_all('tr', {"id": re.compile(r'^F')})
    base_url = 'https://people.utc.edu/eGuide/servlet/'
    result = [base_url + parse_anchor(row) for row in rows]
    
    return result
  
def parse_anchor(row_soup):
    anchor_url = row_soup.get("onclick")
    match = re.search(r"getDetail\('([^']+)'", anchor_url)
    
    if match:
        anchor_link = match.group(1)
        
    return anchor_link

def parse_user_profile(soup):
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    user_data = soup.find_all("td", {"class": "ValueText"})
    
    user_name = soup.find("td", {"class": "formhead2"}).get_text(strip=True).strip()
    user_name = " ".join(user_name.split())
    u_preferred_name = user_data[0].get_text().strip()
    u_email = user_data[1].get_text().strip()
    u_affiliation = user_data[2].get_text().strip()
    
    return {"Name": user_name, "Preferred Name": u_preferred_name, "Email": u_email, "Affiliation": u_affiliation}

def main():
    session = requests.Session()
    url = 'https://people.utc.edu/eGuide/servlet/eGuide?User.context=qtlsRhrljmKm&Action=Detail.get&User.dn=cn%3djgs684%2cou%3dUsers%2co%3dutc&Directory.uid=people&Object.uid=USER'
    data = {"attr1": "LASTNAME", "crit1": "sw", "val1": "a", "x": "43", "y": "23"}
    print(parse_user_profile(url, session))
    
    data_example = [parse_user_profile(url, session)]
    data_df = pd.DataFrame(data_example)
    data_df.to_excel("data.xlsx")
    # soup = BeautifulSoup(response.text, 'html.parser')
    # rows = extract_urls(soup)
    # print(rows[:5])
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