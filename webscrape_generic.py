import json
import re
import time
import requests

from bibtexparser.model import Field
from bs4 import BeautifulSoup

from parser import parse_file, create_new_lib, save_file

FIELD_DOI = 'doi'
FIELD_ABSTRACT = 'abstract'
FIELD_KEYWORDS = 'keywords'
FIELD_TITLE = 'title'


# use something like https://curlconverter.com/
# to build the cookies and headers, to enable authentication (to IEEE)
# data also in local scratch file (4)...

cookies = {}

headers = {}

data = parse_file('data/enrichment/slr_enriched_11_06_2024_12_21_07.bib')

# Define the URL
#url = "https://ieeexplore.ieee.org/document/6735048/keywords#keywords"

# follow the DOI url instead - this approach should work for all IEEE papers in my dataset
#url = "https://doi.org/" + '10.1109/ICOS.2013.6735048'
url = "https://doi.org/"

# this is scraping the source of the article, as redirected to via the DOI url
# this is preferred over the GS approach (see webscrape_doi), as it;
# a, is less susceptible to anti-webscraping strategies employed by Google Scholar
# b, means we can source additional metadata fields (like keywords)


def scrape_springer(soup):
    abstract_scraped = soup.find(id='Abs1-content')

    print(abstract_scraped.get_text())

    return {'abstract': abstract_scraped.get_text(), 'keywords': None}


def scrape_ieee(soup):
    # IEEE keywords & abstract...

    script_tags = soup.find_all('script')

    json_text = None
    for script in script_tags:
        if script.string and 'xplGlobal.document.metadata' in script.string:
            match = re.search(r'xplGlobal\.document\.metadata\s*=\s*(\{.*?\});', script.string, re.DOTALL)
            if match:
                json_text = match.group(1)
                break

    if json_text:
        try:
            json_data = json.loads(json_text)
            # print(json.dumps(data, indent=2))  # Pretty print the JSON data
            return json_data
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
    else:
        print('JSON data not found in any script tag.')


def scrape(scrape_url):
    print(scrape_url)

    response = requests.get(scrape_url, cookies=cookies, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        scraped_data = None
        if 'ieeexplore.ieee.org' in response.request.url:
            print('IEEE article')
            scraped_data = scrape_ieee(soup)
        elif 'link.springer.com' in response.request.url:
            print('springer article')
            scraped_data = scrape_springer(soup)
        else:
            print('non-IEEE article')
            print(response.request.url)
        print('-----------------------------------------')
        return scraped_data
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        print(response)
        return None


new_data = []

for entry in data.entries:
    if FIELD_DOI in entry.fields_dict:
        doi = entry.fields_dict[FIELD_DOI].value
        doi = doi.replace('\\', '')

        if FIELD_ABSTRACT not in entry.fields_dict or FIELD_KEYWORDS not in entry.fields_dict:
            print(entry.fields_dict[FIELD_TITLE].value)
            data = scrape(url + doi)

            if data is not None:
                if FIELD_ABSTRACT not in entry.fields_dict:
                    abstract = data.get('abstract')
                    print('INSERTING THIS ABSTRACT INTO EMPTY ABSTRACT:')
                    print(abstract)
                    print("")

                    if abstract is not None:
                        entry.fields.append(Field(FIELD_ABSTRACT, abstract))

                if FIELD_KEYWORDS not in entry.fields_dict:
                    keywords = data.get('keywords', [])

                    # a bunch of dictionaries...
                    if keywords is not None:
                        for item in keywords:
                            if item['type'] == 'Author Keywords':
                                authorKeywords = item['kwd']
                                print('INSERTING THESE KEYWORDS INTO EMPTY KEYWORDS:')
                                print(authorKeywords)
                                print("")

                        if authorKeywords is not None:
                            entry.fields.append(Field(FIELD_KEYWORDS, authorKeywords))

            time.sleep(10)  # or you may be booted!
    new_data.append(entry)

lib = create_new_lib(new_data)
timestamp = time.strftime("%d_%m_%Y_%H_%M_%S")
cleaned_filename = 'data/enrichment/slr_enriched_' + timestamp + '.bib'
save_file(lib, cleaned_filename)
