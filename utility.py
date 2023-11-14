import glob
import re
from difflib import SequenceMatcher


def consolidate_files(path, output):
    read_files = glob.glob(path + "*.bib")
    print('Consolidating ' + str(len(read_files)) + ' .bib files')

    with open(output, "wb") as outfile:
        for f in read_files:
            with open(f, "rb") as infile:
                outfile.write(infile.read())

# FIXME not catching;

# Dynamic semantic-based green bio-inspired approach for optimizing energy and cloud services qualities
# Dynamic semantic-based green bio-inspired approach for optimizing energy and cloud services qualities. (Dynamic semantic-based green bio-inspired approach for optimizing energy and cloud services qualities)
# would be caught by dropping phd thesis

def find_duplicates(search_lib):
    unique = set()
    search_results = []

    # what about duplicates on title?
    # I need to ignore casing {}
    # e.g. Xsorb: {A} software for...
    # = Xsorb: A software for...
    # this might be a little aggressive - it's finding a few more than bibdesk - check later (FIXME)
    # also not dealing properly with 'emph{'
    title_duplicate_count = 0
    #for entry in search_lib.entries: #FIXME other use needs correcting
    for entry in search_lib:
        title = entry.fields_dict['title'].value.casefold()
        title = title.replace('{', '').replace('}', '')
        title = title.replace('-', ' ')
        title = title.replace(':', '')
        title = title.replace(',', '')
        title = title.replace('\n', '')
        #title = re.sub('\s{2,}', ' ', title) # remove double whitespace
        title = title.replace(" ", "") # just remove all whitespace for the equality check

        similar_title = False
        # sequence matching, for close matches
        # this requires a comparison against every other title
        # this logic dramatically increases processing time
        for compare_title in unique:
            ratio = SequenceMatcher(a=title, b=compare_title).quick_ratio() # ratio() is too slow
            # note that this value requires careful tuning, even at 0.97 it is catching some false positives
            # e.g. where the only change is the year, for conference proceedings
            if ratio > 0.97 and ratio != 1:
                #print('*********************')
                #print('similar!? ' + str(ratio))
                #print('title')
                #print(title)
                #print('compare title')
                #print(compare_title)
                #print('*********************')
                similar_title = True

        #print(title)
        if title not in unique and not similar_title:
            unique.add(title)
            search_results.append(entry)
        else:
            #print('duplicate title; \n' + title)
            title_duplicate_count += 1
    print('found ' + str(title_duplicate_count) + ' duplicates by Title')
    print('sorted entries (removing duplicates by Title) : ' + str(len(unique)))

    return search_results