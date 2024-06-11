from parser import parse_file

from voting import voting


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


if __name__ == '__main__':
    # assuming you have some post-processed data, ready for analysis...
    # legacy main function - most code has since been split out
    # and individual stages of the pipeline can be executed independently

    # testing rapid manual exclusions (AKA voting in)
    data = parse_file('data/output/voted_14_04_2024_21_51_43.bib')

    voting(data)