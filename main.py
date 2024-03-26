import time

from parser import parse_file, save_file, create_new_lib


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
    # assuming you have some post-processed data, ready for analysis...
    #data = parse_file('data/output/cleaned_dblp_1700557848.872979.bib')
    #data = parse_file('data/output/cleaned_acm_1700566901.6334422.bib')
    #data = parse_file('data/output/cleaned_ieee_1700571488.969132.bib')
    #data = parse_file('data/output/cleaned_sd_1700575595.28679.bib')

    # was being used for charting, but I've moved that code out
    data = parse_file('data/output/cleaned_all_1700576716.205068.bib')

    #reapply_search(parsed_voted_data)