import glob
import re
import time

import bibtexparser

from citation import Citation


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

    print('articles : ' + str(num_articles))
    print('proceedings : ' + str(num_proceedings))
    print('thesis : ' + str(num_thesis))
    print('book : ' + str(num_book))
    print('collection : ' + str(num_collection))
    print('TOTAL : ' + str(num_articles + num_proceedings + num_thesis + num_book + num_collection))

def parse_file(filename):
    # load into data frame?
    # identify an individual record (citation) - must be a library for this?
    with open(filename) as bibtex_file:
        library = bibtexparser.load(bibtex_file)
        # this is a list of dicts
    print("mendeley entries : " + str(len(library.entries)))
    return library

def find_duplicates(filename):
    print('processing file : ' + filename)
    # load into data frame?
    # identify an individual record (citation) - must be a library for this?
    with open(filename) as bibtex_file:
        library = bibtexparser.load(bibtex_file)
        # this is a list of dicts
    print("entries : " + str(len(library.entries)))

    #unique = list(set(library.entries))
    #print("sorted entries : " + str(len(unique.entries)))

    unique = set()

    for entry in library.entries:
        #print(entry)
        #print(entry["ID"]) # this is the cite-key - should be unique, but we might have duplicates
        #print(entry["ENTRYTYPE"])
        #print(entry["year"])
        #print(entry["title"])
        #print('------------------------------------')
        citation = Citation()
        citation.key = entry["ID"]
        citation.title = entry["title"]
        if citation not in unique:
            unique.add(citation)
            # else print('not adding suspected duplicate : ' + citation.key)

    print("sorted entries (removing duplicates by ID) : " + str(len(unique)))

    #what about duplicates on title?
    truly_unique = set()
    for citation in unique:
        if citation.title.casefold() not in truly_unique:
            truly_unique.add(citation.title.casefold())
        # else print('not adding suspected duplicate : ' + citation.title.casefold())
    print("sorted entries (removing duplicates by Title) : " + str(len(truly_unique)))

    return truly_unique

def whatisthis():
    search_set = find_duplicates("data/output/consolidated.bib")

    manual_set = find_duplicates("data/input/MendeleyExport.bib")
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

if __name__ == '__main__':

    time_sec = time.time()

    output_filename = "data/output/consolidated_" + str(time_sec) + ".bib"

    consolidate_files("data/input/search/v2/", output_filename)

    count_records(output_filename)

    # FIXME - add a test to compare the pre-consolidated count with the final total
    # a manual check via loading the files in bibdesk is quite easy, in the mean time