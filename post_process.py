import time

from exclusions import build_exclusion_query
from search import reapply_search, SEARCH_STRING
from utility import find_duplicates, remove_proceedings
from parser import parse_file, save_file, create_new_lib

SEARCH_EXCLUDE = build_exclusion_query()

#FIXME - group these later, so they are easier to edit/update/extend
#FIXME - could I move to wildcard search on some of these similar terms?

# take a consolidated data file, that you will search across
input_data = parse_file('data/output/deduped_26_03_2024_11_44_09.bib')

# apply the search on that data and retrieve the results (matches)
results = reapply_search(input_data.entries, SEARCH_STRING, False)

# exclusion criteria...
#results = reapply_search(results, SEARCH_EXCLUDE, False)

# you may have already executed this on the raw data (toggle)
# if you have, this is a waste of time (and it's quite resource intensive)
#results = find_duplicates(results)

results = remove_proceedings(results)

# build a new file containing the matches, ready for export
lib = create_new_lib(results)

# export your post-processed data (to a new file)
timestamp = time.strftime("%d_%m_%Y_%H_%M_%S")
cleaned_filename = 'data/output/cleaned_' + timestamp + '.bib'
save_file(lib, cleaned_filename)