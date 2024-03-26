# we want to NOT match on these exclusion terms...
# SEARCH_EXCLUDE = (r'^(?i)(?:(?!\bedge\b|\bwireless\b).)*$')

def build_exclusion_query():
    # construct programmatically from file...
    search_exclude = r'^(?i)(?:(?!'
    with open('data/words/exclusions.txt', 'r') as file:
        line = file.readline()
        while line:
            search_exclude += '''\\b'''
            search_exclude += line.strip()
            search_exclude += '''\\b|'''
            line = file.readline()
        search_exclude = search_exclude[:-1]  # remove last character, the trailing pipe
        search_exclude += ').)*$'
    return search_exclude