import glob
import re
from difflib import SequenceMatcher


def consolidate_files(path, output):
    #read_files = glob.glob(path + "cleaned*.bib")
    read_files = glob.glob(path + "*.bib")

    if len(read_files) > 0:
        print('consolidating ' + str(len(read_files)) + ' .bib files into ' + output)

        with open(output, "wb") as outfile:
            for f in read_files:
                with open(f, "rb") as infile:
                    outfile.write(infile.read())
    else:
        print('error : attempting to consolidate zero files')

    return len(read_files)

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
    for entry in search_lib:
        title = entry.fields_dict['title'].value.casefold()
        #title = title.replace('{', '').replace('}', '')
        title = re.sub('\{.*?\}', '', title)
        # FIXME can contain formatting in-between, so need to remove what's inside the braces too!
        title = title.replace('-', ' ')
        title = title.replace('\'', ' ')
        title = title.replace('/', '')
        title = title.replace('‘', ' ')
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

def remove_proceedings(search_lib):
    results = []

    proceedings_count = 0
    for entry in search_lib:
        if entry.entry_type != 'proceedings':
            results.append(entry)
        else:
            proceedings_count += 1
    print('found ' + str(proceedings_count) + ' proceedings')

    return results

def count_records(filename):
    num_articles = 0
    num_proceedings = 0
    num_thesis = 0
    num_book = 0
    num_collection = 0

    with open(filename, 'r') as f:
        for line in f:
            #if line.find('article') > 0: #707
            if re.search("@article", line) or\
                re.search("@ARTICLE", line):
                num_articles += 1
            if re.search("@proceedings", line) or\
                    re.search("@inproceedings", line) or\
                    re.search("@INPROCEEDINGS", line):
                num_proceedings += 1
            if re.search("@phdthesis", line):
                num_thesis += 1
            if re.search("@inbook", line) or \
                    re.search("@INBOOK", line) or \
                    re.search("@book", line):
                num_book += 1
            if re.search("@incollection", line):
                num_collection += 1

    #print('articles : ' + str(num_articles))
    #print('proceedings : ' + str(num_proceedings))
    #print('thesis : ' + str(num_thesis))
    #print('book : ' + str(num_book))
    #print('collection : ' + str(num_collection))

    total_count = num_articles + num_proceedings + num_thesis + num_book + num_collection
    print('count_records(' + filename + ') : count = ' + str(total_count))

    return total_count