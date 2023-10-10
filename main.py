import glob
import re
import time
import datetime

import bibtexparser

import matplotlib.pyplot as plt

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

# function to add value labels
def add_labels(x, y):
    for i in range(len(x)):
        # plt.text(i, y[i] // 2, x[i], ha='center', rotation=90)
        plt.text(i, 2, x[i], ha='center', rotation=90)

def chart_publications():
    years = {}
    for entry in parsed_voted_data.entries:
        if 'year' in entry.fields_dict:
            year_string = entry.fields_dict['year'].value
            year = datetime.datetime.strptime(year_string, '%Y').date()
            if year in years:
                years[year] += 1
            else:
                years[year] = 1

    sorted_years = dict(sorted(years.items()))
    sorted_years.pop(datetime.date(2024, 1, 1), None)  # won't error if it doesn't exist

    plt.plot(list(sorted_years.keys()), list(sorted_years.values()), color='g')
    plt.title("Green IT Publications")
    plt.xlabel("Publication Year")
    plt.ylabel("Publication Count")
    plt.show()

def chart_journals():
    journals = {}
    for entry in parsed_voted_data.entries:
        # print(entry)
        if 'journal' in entry.fields_dict:
            journal_string = entry.fields_dict['journal'].value
            if journal_string in journals:
                journals[journal_string] += 1
            else:
                journals[journal_string] = 1
    sorted_journals = dict(sorted(journals.items()))

    from operator import itemgetter
    journal_list = sorted(sorted_journals.items(), key=itemgetter(1))
    journal_top10 = []
    count = 0
    while count < 10:
        journal_top10.append(journal_list[(len(journal_list) - 1) - count])
        count += 1
    sjt = {}
    for j in journal_top10:
        sjt[j[0]] = j[1]

    x = list(sjt.keys())
    y = list(sjt.values())

    add_labels(x, y)
    # plt.xticks(rotation=90)
    plt.xticks([])
    plt.bar(x, y, color='g')
    plt.title("Green IT Journals")
    plt.xlabel("Journal")
    plt.ylabel("Publication Count")
    plt.show()

# FIXME a lot of this code is common with top 10 journals
def chart_authors():
    authors = {}
    for entry in parsed_voted_data.entries:
        #print(entry)
        if 'author' in entry.fields_dict:
            author_string = entry.fields_dict['author'].value
            result = re.split(r'\s+and\s+', author_string)
            # simply count the occurrences of all names
            for author_individual in result:
                if author_individual in authors:
                    authors[author_individual] += 1
                else:
                    authors[author_individual] = 1

    sorted_authors_list = sorted(authors.items(), key=lambda item: item[1])
    authors_top10 = []
    count = 0
    while count < 10:
        authors_top10.append(sorted_authors_list[(len(sorted_authors_list) - 1) - count])
        count += 1
    sjt = {}
    for j in authors_top10:
        sjt[j[0]] = j[1]

    x = list(sjt.keys())
    y = list(sjt.values())

    add_labels(x, y)
    plt.xticks([])
    plt.bar(x, y, color='g')
    plt.title("Green IT Authors")
    plt.xlabel("Author")
    plt.ylabel("Publication Count")
    plt.show()

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
    #chart_publications()

    # popular journals
    chart_journals()

    # popular authors (e.g. Lago)
    #chart_authors()

    # FIXME - plot them all together, or at the same time in different windows
    # (useful to be able to save them individually)