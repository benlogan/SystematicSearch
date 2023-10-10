import glob
import time

import bibtexparser

import matplotlib.pyplot as plt

from charting import *

def consolidate_files(path, output):
    read_files = glob.glob(path + "*.bib")
    print('Consolidating ' + str(len(read_files)) + ' .bib files')

    with open(output, "wb") as outfile:
        for f in read_files:
            with open(f, "rb") as infile:
                outfile.write(infile.read())

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
    print('Manual Entry Count : ' + str(num_articles + num_proceedings + num_thesis + num_book + num_collection))

def parse_file(filename):
    # read individual records (citations) - using a bibtex library
    # using v2 of the bibtex library
    # it will remove some duplicates (by ID) on initial parse

    parsed_lib = bibtexparser.parse_file(filename)

    print('(' + filename + ') entries : ' + str(len(parsed_lib.entries)))
    if len(parsed_lib.failed_blocks) > 0:
        print("Some blocks failed to parse. Check the entries of `library.failed_blocks`.")
    else:
        print("All blocks parsed successfully")

    return parsed_lib

def save_file(lib, filename):
    # write out the new cleaned file
    bibtexparser.write_file(filename, lib)

def find_duplicates(search_lib):
    unique = set()
    removal_list = []

    # what about duplicates on title?
    # I need to ignore casing {}
    # e.g. Xsorb: {A} software for...
    # = Xsorb: A software for...
    # this might be a little aggressive - it's finding a few more than bibdesk - check later (FIXME)
    # also not dealing properly with 'emph{'
    title_duplicate_count = 0
    for entry in search_lib.entries:
        title = entry.fields_dict['title'].value.casefold()
        title = title.replace('{', '').replace('}', '')
        if title not in unique:
            unique.add(title)
        else:
            #print('duplicate title ' + title)
            title_duplicate_count += 1
            removal_list.append(entry)
    print('found ' + str(title_duplicate_count) + ' duplicates by Title')
    print('sorted entries (removing duplicates by Title) : ' + str(len(unique)))

    return removal_list

def analysis():
    # FIXME this code is now broken and needs fixing, to run the gap analysis properly
    search_set = parse_file("data/output/consolidated.bib")

    manual_set = parse_file("data/input/MendeleyExport.bib")

    # parse_file("data/input/MendeleyExport.bib")

    # what do I have in my search set that I don't have in my manual set?

    # what do I have in my manual set that I don't have in my search set?
    not_in_search = 0
    for citation in manual_set:
        if citation not in search_set:
            print('cant find this in the search set : ' + citation.title())
            not_in_search += 1
        # else print('MATCH : ' + citation.title())

    # this is the search gap - I need to get the number down
    # (while ensuring the search results themselves don't go through the roof with false positives)
    print('NEED TO ADJUST SEARCH TO FIND MORE DOCS : ' + str(not_in_search))

def process_raw_data():
    time_sec = time.time()

    consolidated_filename = 'data/output/consolidated_' + str(time_sec) + '.bib'

    consolidate_files("data/input/search/v2/", consolidated_filename)

    # if I want to use a modified or manually cleaned consolidated file;
    # consolidated_filename = 'data/output/consolidated_cleaned.bib'

    # manual count (read file for certain strings)
    count_records(consolidated_filename)

    # parse file (process of reading will remove some dupes)
    processed_lib = parse_file(consolidated_filename)

    # FIXME - add a test to compare the pre-consolidated count with the final total
    # a manual check via loading the files in bibdesk is quite easy, in the mean time

    # you actually need to remove the failed (dupes) from the main block structure
    processed_lib.remove(processed_lib.failed_blocks)

    # remove duplicates by title
    title_duplicates = find_duplicates(processed_lib)
    processed_lib.remove(title_duplicates)

    # write the cleaned data back to a file, to facilitate voting in bibdesk?
    cleaned_filename = 'data/output/deduped_' + str(time.time()) + '.bib'
    save_file(processed_lib, cleaned_filename)

if __name__ == '__main__':
    #process_raw_data()

    # or we could do the voting here? (pop up with Y/N - could be rapid)

    # with voting in bibdesk, using the 'read' checkbox to indicate voted in...
    lib = bibtexparser.library.Library()
    blocks = []
    parsed_voted_data = parse_file('data/output/deduped_1696368991.44827_voting.bib')
    for entry in parsed_voted_data.entries:
        if 'read' in entry.fields_dict and entry.fields_dict['read'].value == '1':
            #print('FOUND SOMETHING VOTED IN')
            blocks.append(entry)

    # build a whole new library for exporting clean...
    lib.add(blocks)
    filename = 'data/output/voted_' + str(time.time()) + '.bib'
    save_file(lib, filename)

    # let's do some visualisation/analysis!
    #chart_publications(parsed_voted_data, plt)

    # popular journals
    #chart_journals(parsed_voted_data, plt)

    # popular authors (e.g. Lago)
    #chart_authors(parsed_voted_data, plt)

    # keyword cloud? or table to start
    chart_keywords(parsed_voted_data, plt)

    # FIXME - plot them all together, or at the same time in different windows
    # (useful to be able to save them individually)