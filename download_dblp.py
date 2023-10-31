import requests
import time

from utility import consolidate_files

# This is the preferred approach for downloading from dblp (not web scraping)

# Due to problems with dblp search (e.g. can't limit to title), the result count will be high
# To work around the 1000 result limit, we refine the query by year and collate the results later
# Due to the large number of false positives, the results will need secondary search cleaning

# Define the URL of the .bib file
#url = "https://dblp.org/search/publ/api?q=sustainable+software+engineering&h=1000&format=bib1&rd=1a" (basic URL for testing only)
url = "https://dblp.org/search/publ/api?q=(sustainab*%20%7C%20green%24%20%7C%20energy%24)%20(software%24%20%7C%20%20IT%24%20%20%7C%20computing%24%20%7C%20cloud%24)%20year%3A1995%3A&h=1000&format=bib1&rd=1a"

year = 1995
while year <= 2023:

    url = "https://dblp.org/search/publ/api?q=(sustainab*%20%7C%20green%24%20%7C%20energy%24)%20(software%24%20%7C%20%20IT%24%20%20%7C%20computing%24%20%7C%20cloud%24)%20year%3A"
    url += str(year) + "%3A&h=1000&format=bib1&rd=1a"
    print(url)
    response = requests.get(url)

    if response.status_code == 200:
        # Define the path where you want to save the .bib file
        file_path = "data/downloads/dblp_" + str(year) + "_" + str(time.time()) + ".bib"

        # Save the response content to the .bib file
        with open(file_path, 'wb') as bib_file:
            bib_file.write(response.content)

        print(f".bib file downloaded and saved as {file_path}")
    else:
        print(f"Failed to download .bib file. Status code: {response.status_code}")

    year += 1

consolidated_filename = 'data/output/consolidated_dblp_' + str(time.time()) + '.bib'

consolidate_files("data/downloads/", consolidated_filename)