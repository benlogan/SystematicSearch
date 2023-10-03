import requests

# to work properly, would need a pre-search, to identify the record IDs!

# Define the URL of the .bib file
url = "https://ieeexplore.ieee.org/rest/search/citation/format?recordIds=9675938,8128977,8112107,6254546,8409215,8705852,6008495,9690260,9690205,7155006,9004283,6118899,6728926,7724226,8449825,6139638,6227030,7169671,8816873,9679832,9604527,8449016,9585139,8796529,8966710,6017871,8796633,5167271,6353405,5708281,5601682,5601679,6391808,6109215,5735595,5070049,8780408,6139095,4760631,5234398,5543346,5427382,6357172,6260858,5493359,6721885,7975693,7005931,7829853,9141166,4738046,8674050,6477253,6716716,4458787,6061300,8024729,7030217,5156744,5657681,7359627,9170668,6735048,5283542,8548095,6613456,7280132,7878441,6197783,6169664,6360438,5310123,7818722,6263127,8326827,6663313,6716161,5676331,8168446,6360539,9821719,9300767,9791830,6576756,4782221,5659717,5346051,6061328,1180358,5718554,6047009,9210362,9717357,10172842,7516827,5704342,6662597,5876124,8797634,6032566&download-format=download-bibtex&lite=true"

#getting a 418, need to send headers

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Define the path where you want to save the .bib file
    file_path = "data/downloads/ieee.bib"

    # Save the response content to the .bib file
    with open(file_path, 'wb') as bib_file:
        bib_file.write(response.content)

    print(f".bib file downloaded and saved as {file_path}")
else:
    print(f"Failed to download .bib file. Status code: {response.status_code}")
