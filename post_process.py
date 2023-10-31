import re

from parser import parse_file

FIELD_TITLE = 'title'

# post processor for executing the query a second time, in code
# this helps to clean the results and account for various problems with certain database searches
# this can be executed independently, or as part of the main code path

# SEARCH QUERY;
# (sustainab* OR green OR energy) AND (software OR "IT" OR computing OR cloud)

def reapply_search(data):
    count = 0
    for entry in data.entries:
        if FIELD_TITLE in entry.fields_dict:
            title_string = entry.fields_dict[FIELD_TITLE].value

            search_query = r'(?=.*(sustainab\w*|green|energy))(?=.*(software|IT|computing|cloud))'

            matches = re.findall(search_query, title_string, re.IGNORECASE)

            if not matches:
                print(title_string)
                print('no match, dropping it')
                print('---------------------------')
                count += 1
    print('original count ' + str(len(data.entries)))
    print('suggest dropping ' + str(count))

data = parse_file('data/output/consolidated_dblp_1698748522.405845.bib')

reapply_search(data)