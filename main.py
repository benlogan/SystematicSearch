import time

from parser import parse_file, save_file, create_new_lib
from bibtexparser.model import Entry, Field


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


def voting(data):

    vote_data = []

    breakout = False
    for entry in data.entries:
        if not breakout and 'vote' not in entry.fields_dict:
            print(entry.fields_dict['title'].value)

            keep = input("Vote Out? hit X :")

            fields_list = entry.fields
            value = 'IN'

            if keep == 'X' or keep == 'x':
                print('VOTING OUT')
                # let's add a new field...
                value = 'OUT'

            fields_list.append(Field('vote', value))

            if keep == 'q':
                breakout = True
            # i.e. you can just single-press enter to skip through quickly!

        # always append all - so you always output a complete dataset
        vote_data.append(entry)

    lib = create_new_lib(vote_data)

    timestamp = time.strftime("%d_%m_%Y_%H_%M_%S")
    filename = 'data/output/voted_' + timestamp + '.bib'
    save_file(lib, filename)


if __name__ == '__main__':
    # assuming you have some post-processed data, ready for analysis...
    # legacy main function - most code has since been split out
    # and individual stages of the pipeline can be executed independently

    # testing rapid manual exclusions (AKA voting in)
    #data = parse_file('data/output/cleaned_26_03_2024_15_09_14.bib')
    data = parse_file('data/output/voted_26_03_2024_19_17_50.bib')

    voting(data)