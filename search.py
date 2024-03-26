import re


FIELD_TITLE = 'title'

# original search query;
# (sustainab* OR green OR energy) AND (software OR "IT" OR computing OR cloud)

SEARCH_STRING = r'\b(?:sustainab\w*|green|energy)\b.*?\b(?:software|(?-i:\bIT\b)\b|computing|cloud)|\b(?:software|(?-i:\bIT\b)\b|computing|cloud)\b.*?\b(?:sustainab\w*|green|energy)'
# note - use python IGNORE_CASE for case insensitivity, but protect 'IT' in the pattern itself!

#FIXME this is broken. e.g. 'Managing Green IT' being dropped

def reapply_search(data, search_query, debug):
    print('executing search : ' + search_query)
    count = 0
    search_results = []
    for entry in data:
        if FIELD_TITLE in entry.fields_dict:
            title_string = entry.fields_dict[FIELD_TITLE].value
            title_string = title_string.replace('\n', '')
            # strip the title of new line characters
            # should really remove the whitespace, though this doesn't break the regex matching
            title_string = re.sub('\s+', ' ', title_string)

            regex = re.compile(search_query, re.IGNORECASE) # had tried solving case sensitivity in the pattern, but it's quite complicated!
            matches = regex.findall(title_string)

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