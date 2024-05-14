import time

from bibtexparser.model import Field

import charting
from parser import parse_file, save_file, create_new_lib


input_data = parse_file('data/enrichment/voted_14_04_2024_21_52_28.bib')

def categorise(data):
    groups = []
    new_data = []

    # note this code was originally taken from the keyphrases charting code,
    # but it has since been modified quite significantly

    with open('data/words/phrasesNew.txt', 'r') as file:
        line = file.readline()
        while line:
            line = line.strip()
            if ',' in line:
                groups.append(line)
            line = file.readline()

    for entry in data:
        if charting.FIELD_TITLE in entry.fields_dict:
            title = entry.fields_dict[charting.FIELD_TITLE].value.casefold()
            tags = ''
            for grouped_line in groups:
                group_name = grouped_line.split(':')[0]
                for grouped_keyphrase in grouped_line.split(':')[1].split(','):
                    if grouped_keyphrase in title:
                        if not tags:
                            tags = group_name
                        else:
                            tags = tags + ',' + group_name
                        break # must avoid double counting here - break out once you've found one match in a group
            # add the tags to the data (for persistence back to file later)
            entry.fields.append(Field('Categories_Extracted', tags))

            matches = ["ENT", "SIM", "MEAS"]
            if any(x in tags for x in matches):
                entry.fields.append(Field('SLR', 'YES'))

            new_data.append(entry)

            print(title)
            print(tags)

    return new_data


results = categorise(input_data.entries)

# build a new file, ready for export
lib = create_new_lib(results)

# export processed data (to a new file)
timestamp = time.strftime("%d_%m_%Y_%H_%M_%S")
cleaned_filename = 'data/output/categorised_' + timestamp + '.bib'
save_file(lib, cleaned_filename)