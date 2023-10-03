import requests

# OK, this works - this is systematic search!!!

# Define the URL of the .bib file
url = "https://dblp.org/search/publ/api?q=sustainable+software+engineering&h=1000&format=bib1&rd=1a"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Define the path where you want to save the .bib file
    file_path = "data/downloads/dblp.bib"

    # Save the response content to the .bib file
    with open(file_path, 'wb') as bib_file:
        bib_file.write(response.content)

    print(f".bib file downloaded and saved as {file_path}")
else:
    print(f"Failed to download .bib file. Status code: {response.status_code}")
