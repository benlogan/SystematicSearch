import time

import requests
from bs4 import BeautifulSoup
from parser import parse_file, save_file
from bibtexparser.model import Field

FIELD_DOI = 'doi'
FIELD_ABSTRACT = 'abstract'
FIELD_TITLE = 'title'

# DOI - identifier

# the DOI site will redirect to the appropriate journal/search engine
# from there, I can extract the keywords or abstract (or whatever else I need)

# Define the URL
url = "https://doi.org/"
# e.g. https://doi.org/10.1007/978-3-031-15559-8_5
# note; for this to work, I needed to trim the end of the URL - remove the last \

# Google Scholar might be better for this (only dealing with a single format)
url = "https://scholar.google.co.uk/scholar?hl=en&as_sdt=0%2C5&q="

doi = "10.1007/978-3-031-15559-8\_5"
doi = "10.1007/978-3-031-40843-4\_18"
doi = "10.5220/0011984700003464"
doi = "10.1145/2664591.2664609"

data = parse_file('data/enrichment/slr_edited.bib')

missing_abstracts = 0

# isn't making any difference, presumably IP blocked
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def scrape_abstract(scrape_url):
    print(scrape_url)

    # Send an HTTP GET request to the URL
    response = requests.get(scrape_url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # print(soup)

        # Springer
        # abstract = soup.find(id='Abs1-content')
        # print(abstract)

        # if abstract:
        #    abstract_text = abstract.get_text()
        #    print(abstract_text)

        # Google Scholar
        abstract = soup.find_all('div', class_='gs_fma_abs')
        # print(abstract)

        for text in abstract:
            print(text.get_text())
            return text.get_text()
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        print(response)


new_data = []

for entry in data.entries:
    if FIELD_DOI in entry.fields_dict:
        doi = entry.fields_dict[FIELD_DOI].value
        if FIELD_ABSTRACT not in entry.fields_dict:
            print(entry.fields_dict[FIELD_TITLE].value)
            print(doi)

            doi = doi.replace('\\', '')

            abstract = scrape_abstract(url + doi)
            time.sleep(10) # or you will receive 429 response (too many requests), from GS

            entry.fields.append(Field(FIELD_ABSTRACT, abstract))
            new_data.append(entry)

            missing_abstracts = missing_abstracts + 1

print(missing_abstracts)

timestamp = time.strftime("%d_%m_%Y_%H_%M_%S")
cleaned_filename = 'data/enrichment/slr_enriched_' + timestamp + '.bib'
save_file(new_data, cleaned_filename)
