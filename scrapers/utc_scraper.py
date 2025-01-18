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
    

def run_script(queries):
    session = requests.Session()
    result_data = []
    for query in queries:
        print("Processing query:", query)
        init_url = f'https://people.utc.edu/eGuide/servlet/eGuide?User.context=qtlsRhrljmKm&Action=List.get&Object.uid=USER&max=10000&Search.attributes=,LASTNAME,EDUPERSONNICKNAME,EDUPERSONPRIMARYAFFILIATION&Primary.sortkey=LASTNAME&Secondary.sortkey=EDUPERSONNICKNAME'
        data = {"attr1": "LASTNAME",
                "crit1": "sw",
                "val1": query,
                "x": "68",
                "y": "14"}
        master_soup = make_request(init_url, "P", session, data)
        user_urls = extract_urls(master_soup)
        query_result = [parse_user_profile(make_request(url, "G", session)) for url in user_urls]
        result_data.extend(query_result)
        print("Finished processing query:", query)
    
    return result_data
        
        
        
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
    user_data = soup.find_all("td", {"class": "ValueText"})
    
    user_name = soup.find("td", {"class": "formhead2"}).get_text(strip=True).strip()
    user_name = " ".join(user_name.split())
    u_preferred_name = user_data[0].get_text().strip()
    u_email = user_data[1].get_text().strip()
    u_affiliation = user_data[2].get_text().strip()
    
    return {"Name": user_name, "Preferred Name": u_preferred_name, "Email": u_email, "Affiliation": u_affiliation}

def main():
    queries = ["a", "b"]
    result = run_script(queries)
    result_df = pd.DataFrame(result)
    result_df.to_excel("data.xlsx")
    
    return



if __name__ == "__main__":
    main()