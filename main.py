import time

import matplotlib.pyplot as plt

from charting import *
from charting_keywords import chart_keywords, chart_actual_keywords, chart_keyphrases
from parser import parse_file, save_file, create_new_lib
from utility import consolidate_files, find_duplicates


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

    consolidated_filename = 'data/output/consolidated_' + str(time.time()) + '.bib'

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
    # FIXME this will now remove duplicates and return cleaned data structure
    #title_duplicates = find_duplicates(processed_lib)
    #processed_lib.remove(title_duplicates)
    processed_lib = find_duplicates(processed_lib.entries) # untested code!

    # write the cleaned data back to a file, to facilitate voting in bibdesk?
    cleaned_filename = 'data/output/deduped_' + str(time.time()) + '.bib'
    save_file(processed_lib, cleaned_filename)

def voting():
    # moving this code out, not currently using, come back to it later...

    # we could do the voting here? (pop up with Y/N - could be rapid)

    # with voting in bibdesk, using the 'read' checkbox to indicate voted in...
    vote_data = []

    parsed_voted_data = parse_file('data/output/deduped_1696368991.44827_voting.bib')
    for entry in parsed_voted_data.entries:
        if 'read' in entry.fields_dict and entry.fields_dict['read'].value == '1':
            #print('FOUND SOMETHING VOTED IN')
            vote_data.append(entry)

    lib = create_new_lib(vote_data)

    filename = 'data/output/voted_' + str(time.time()) + '.bib'
    save_file(lib, filename)

if __name__ == '__main__':
    #process_raw_data()

    #consolidated_filename = 'data/output/consolidated_all_' + str(time.time()) + '.bib'
    #consolidate_files("data/input/search/v3/", consolidated_filename)
    #consolidate_files("data/output/", consolidated_filename)

    # assuming you have some post-processed data, ready for analysis...
    #data = parse_file('data/output/cleaned_dblp_1700557848.872979.bib')
    #data = parse_file('data/output/cleaned_acm_1700566901.6334422.bib')
    #data = parse_file('data/output/cleaned_ieee_1700571488.969132.bib')
    #data = parse_file('data/output/cleaned_sd_1700575595.28679.bib')
    data = parse_file('data/output/cleaned_all_1700576716.205068.bib')

    # charting...

    plt.figure(1, figsize=(6,5))
    chart_publications(data, plt)

    plt.figure(2, figsize=(6,5))
    chart_journals(data, plt)

    plt.figure(3, figsize=(6,5))
    chart_authors(data, plt)

    plt.figure(4, figsize=(6,5))
    chart_types(data, plt)

    plt.figure(5, figsize=(6,10))
    chart_keywords(data, plt)

    plt.figure(6, figsize=(6,10))
    chart_actual_keywords(data, plt)

    plt.figure(7, figsize=(6,10))
    chart_keyphrases(data, plt)

    plt.show()

    #reapply_search(parsed_voted_data)