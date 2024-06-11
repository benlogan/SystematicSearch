import ast
import csv
import io
import json
import time

from bibtexparser.model import Field

from parser import parse_file, save_file, create_new_lib


FIELD_KEYWORDS = 'keywords'
FIELD_TITLE = 'title'

# DQ cleaning (misc)

data = parse_file('data/enrichment/slr_enriched_11_06_2024_12_51_57_manual.bib')

new_data = []

for entry in data.entries:
    if FIELD_KEYWORDS in entry.fields_dict:
        keywords = entry.fields_dict[FIELD_KEYWORDS].value
        if keywords[0] is '[':
            parsed_list = ast.literal_eval(keywords)

            print(entry.fields_dict[FIELD_TITLE].value)
            print(parsed_list)

            # Create an in-memory file-like string buffer
            output = io.StringIO()

            # Create a CSV writer object
            csv_writer = csv.writer(output)

            # Write the list as a single row in the CSV file
            csv_writer.writerow(parsed_list)

            # Get the CSV string
            csv_string = output.getvalue()

            # Close the StringIO object
            output.close()

            # not an append! the field already exists, if you append this will create a duplicate
            entry.fields_dict[FIELD_KEYWORDS].value = csv_string

    new_data.append(entry)


# build a new file containing the matches, ready for export
lib = create_new_lib(new_data)

# export your post-processed data (to a new file)
timestamp = time.strftime("%d_%m_%Y_%H_%M_%S")
cleaned_filename = 'data/enrichment/slr_enriched_cleaned_' + timestamp + '.bib'
save_file(lib, cleaned_filename)