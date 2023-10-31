import re
import time

from parser import parse_file, save_file, create_new_lib

FIELD_TITLE = 'title'

# post processor for executing the query a second time, in code
# this helps to clean the results and account for various problems with certain database searches
# this can be executed independently, or as part of the main code path

# SEARCH QUERY;
# (sustainab* OR green OR energy) AND (software OR "IT" OR computing OR cloud)

SEARCH_STRING = r'(?=.*(sustainab\w*|green|energy))(?=.*(software|IT|computing|cloud))'

# We want to NOT match on these exclusion terms...
SEARCH_EXCLUDE = r'^(?:(?!\bedge\b|\bwireless\b).)*$'

def reapply_search(data, search_query, debug):
    print('Executing Search : ' + search_query)
    count = 0
    search_results = []
    for entry in data:
        if FIELD_TITLE in entry.fields_dict:
            title_string = entry.fields_dict[FIELD_TITLE].value
            title_string = title_string.replace('\n', '')
            # strip the title of new line characters
            # FIXME and should really remove the whitespace, though this doesn't break the regex matching

            matches = re.findall(search_query, title_string, re.IGNORECASE)

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
input_data = parse_file('data/output/consolidated_dblp_1698748522.405845.bib')

# apply the search on that data and retrieve the results (matches)
results = reapply_search(input_data.entries, SEARCH_STRING, False)

# exclusion criteria...
results = reapply_search(results, SEARCH_EXCLUDE, True)

# build a new file containing the matches, ready for export
lib = create_new_lib(results)

# export your post processed data (a new file)
cleaned_filename = 'data/output/cleaned_dblp_' + str(time.time()) + '.bib'
save_file(lib, cleaned_filename)