import requests
from bs4 import BeautifulSoup

# Run script with a bunch of queries

# Retrieve information

# Parse response 


def main():
    session = requests.Session()
    url = 'https://people.utc.edu/eGuide/servlet/eGuide?User.context=hmoxQmrwimHi&Action=List.get&Object.uid=USER&max=1&Search.attributes=,LASTNAME,EDUPERSONNICKNAME,EDUPERSONPRIMARYAFFILIATION&Primary.sortkey=LASTNAME&Secondary.sortkey=EDUPERSONNICKNAME'
    data = {"attr1": "LASTNAME", "crit1": "sw", "val1": "b", "x": "43", "y": "23"}
    response = session.post(url, data=data)
    print(response.status_code)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    soup.find("table", {"id": "resultTable"})
    table_rows = soup.find_all("tr")
    print(table_rows)
    
    return



if __name__ == "__main__":
    main()