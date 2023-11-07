import re
import time

from utility import find_duplicates
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
SEARCH_EXCLUDE = (r'^(?i)(?:(?!\bedge\b|\bwireless\b|\bmobile\b|\bneural network\b|\biot\b|\bnetworks\b|\bnetworking\b|\bwearable\b'
                  r'|\bcircuit\b|\bcircuits\b|\bvehicular\b|\bvehicle\b|\buav\b|\bbattery\b|\b5g\b|\bgrid\b|\bradio\b|\bfog\b'
                  r'|\bphysics\b|\bquantum\b|\bdrones\b|\bradios\b|\bsocial\b|\bbuildings\b|\bhome\b|\boffice\b|\bsmartphone\b'
                  r'|\bandroid\b|\bportable\b|\bmolecular\b|\bnano\b|\bneuro\b|\bvehicles\b|\bprotocol\b|\bpersonal\b'
                  r'|\bembedded\b|\bcrypto\b|\bcryptography\b|\bcryptographic\b|\bblockchain\b|\brobotics\b|\brobot\b|\brobots\b'
                  r'|\beducation\b|\bchemical\b|\bbiochemical\b|\bbluetooth\b|\braspberry\b|\bvoltage\b|\bsmartphones\b|\bvideo\b'
                  r'|\bcyber\b|\bcrystals\b|\bspeech recognition\b|\bcorrection to\b|\bnanoscale\b|\bwave\b|\bcodec\b|\bmultiphysics\b).)*$')

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
input_data = parse_file('data/output/consolidated_dblp_1698748522.405845.bib')

# apply the search on that data and retrieve the results (matches)
results = reapply_search(input_data.entries, SEARCH_STRING, False)

# exclusion criteria...
results = reapply_search(results, SEARCH_EXCLUDE, False)

results = find_duplicates(results)

# build a new file containing the matches, ready for export
lib = create_new_lib(results)

# export your post processed data (a new file)
cleaned_filename = 'data/output/cleaned_dblp_' + str(time.time()) + '.bib'
save_file(lib, cleaned_filename)