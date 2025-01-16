import requests
from bs4 import BeautifulSoup

# Run script with a bunch of queries

# Retrieve information

# Parse response 


def replace_amp(input_string):
    """
    Replaces all occurrences of '&amp;' in the input string with '&'.

    Parameters:
        input_string (str): The input string to be processed.

    Returns:
        str: The processed string with '&amp;' replaced by '&'.
    """
    return input_string.replace("&amp;", "&")


def main():
    session = requests.Session()
    anchor = "eGuide?User.context=onjsQmtnmgJu&amp;Action=Detail.get&amp;User.dn=cn%3dzql389%2cou%3dUsers%2co%3dutc&amp;Directory.uid=people&amp;Object.uid=USER"
    user_url = f"https://people.utc.edu/eGuide/servlet/{replace_amp(anchor)}" 
    print(user_url)
    data = {"attr1": "LASTNAME", "crit1": "sw", "val1": "b", "x": "43", "y": "23"}
    # response = session.post(user_url, data=data)
    response_user = session.get(user_url)
    print(response_user.status_code)
    
    soup = BeautifulSoup(response_user.text, 'html.parser')
    name = soup.find("td", {"class": "formhead2"})
    values = soup.find_all("td", {"class": "ValueText"})
    data = []
    data.append(' '.join(name.get_text().split()))
    data.extend([value.get_text().strip() for value in values])
    
    print(data)
    
    
    return



if __name__ == "__main__":
    main()