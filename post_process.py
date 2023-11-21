import re
import time

from utility import find_duplicates, remove_proceedings
from parser import parse_file, save_file, create_new_lib

FIELD_TITLE = 'title'

# post processor for executing the query a second time, in code
# this helps to clean the results and account for various problems with certain database searches
# this can be executed independently, or as part of the main code path

# SEARCH QUERY;
# (sustainab* OR green OR energy) AND (software OR "IT" OR computing OR cloud)

#SEARCH_STRING = r'(?=.*(sustainab\w*|green|energy))(?=.*(software|\bIT\b|computing|cloud))'
# adding case insensitivity for everything other than IT!
SEARCH_STRING = r'(?i)(?=.*(sustainab\w*|green|energy))(?=(?i:.*(?!(?i:\bIT\b))(software|\bIT\b|computing|cloud)))'

# We want to NOT match on these exclusion terms...
# SEARCH_EXCLUDE = (r'^(?i)(?:(?!\bedge\b|\bwireless\b).)*$')

# construct programmatically from file...
SEARCH_EXCLUDE = r'^(?i)(?:(?!'
with open('data/words/exclusions.txt', 'r') as file:
    line = file.readline()
    while line:
        SEARCH_EXCLUDE += '''\\b'''
        SEARCH_EXCLUDE += line.strip()
        SEARCH_EXCLUDE += '''\\b|'''
        line = file.readline()
    SEARCH_EXCLUDE = SEARCH_EXCLUDE[:-1] # remove last character, the trailing pipe
    SEARCH_EXCLUDE += ').)*$'

#FIXME - group these later, so they are easier to edit/update/extend
#FIXME - could I move to wildcard search on some of these similar terms?

def reapply_search(data, search_query, debug):
    print('Executing Search : ' + search_query)
    count = 0
    search_results = []
    for entry in data:
        if FIELD_TITLE in entry.fields_dict:
            title_string = entry.fields_dict[FIELD_TITLE].value
            title_string = title_string.replace('\n', '')
            # strip the title of new line characters
            # should really remove the whitespace, though this doesn't break the regex matching
            title_string = re.sub('\s+', ' ', title_string)

            matches = re.findall(search_query, title_string) # re.IGNORECASE (case sensitivity is handled in the expression)

            if not matches:
                if debug:
                    print(title_string)
                    print('no match, dropping it')
                    print('---------------------------')
                count += 1
            else:
                search_results.append(entry)
    print('original count ' + str(len(data)))
    print('suggest dropping ' + str(count))

    return search_results

# take a consolidated data file, that you will search across
#input_data = parse_file('data/output/consolidated_dblp_1698748522.405845.bib')
#input_data = parse_file('data/input/search/v3/acm.bib')
#input_data = parse_file('data/output/consolidated_ieee_1700571258.360456.bib')
#input_data = parse_file('data/output/consolidated_sd_1700575505.5411599.bib')
input_data = parse_file('data/output/consolidated_all_1700575903.58812.bib')

# apply the search on that data and retrieve the results (matches)
results = reapply_search(input_data.entries, SEARCH_STRING, False)

# exclusion criteria...
results = reapply_search(results, SEARCH_EXCLUDE, False)

results = find_duplicates(results)

results = remove_proceedings(results)

# build a new file containing the matches, ready for export
lib = create_new_lib(results)

# export your post processed data (a new file)
#cleaned_filename = 'data/output/cleaned_dblp_' + str(time.time()) + '.bib'
#cleaned_filename = 'data/output/cleaned_acm_' + str(time.time()) + '.bib'
#cleaned_filename = 'data/output/cleaned_ieee_' + str(time.time()) + '.bib'
#cleaned_filename = 'data/output/cleaned_sd_' + str(time.time()) + '.bib'
cleaned_filename = 'data/output/cleaned_all_' + str(time.time()) + '.bib'
save_file(lib, cleaned_filename)