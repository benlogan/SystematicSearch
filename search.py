import requests
from bs4 import BeautifulSoup

# Define the URL
url = "https://dblp.org/search/publ?q=sustainable%20software%20engineering"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract and print the titles of the publications
    titles = soup.find_all('span', class_='title')
    print("found results : " + str(len(titles)))
    for title in titles:
        print(title.text)

    # Extract and print the number from the paragraph with id=completesearch-info-matches
    matches_paragraph = soup.find('p', id='completesearch-info-matches')
    if matches_paragraph:
        matches_text = matches_paragraph.get_text()
        # Extract the number using regular expressions
        import re

        matches_number = re.search(r'(\d+) matches', matches_text)
        if matches_number:
            print("Number of matches:", matches_number.group(1))
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
