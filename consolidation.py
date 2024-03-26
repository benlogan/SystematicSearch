import time

from parser import parse_file, save_file, create_new_lib
from utility import consolidate_files, find_duplicates, count_records


def consolidation(filename):
    file_count = consolidate_files("data/input/search/v2/", filename)

    if file_count > 0:
        # if I want to use a modified or manually cleaned consolidated file;
        # consolidated_filename = 'data/output/consolidated_cleaned.bib'

        #consolidated_filename = 'data/output/consolidated_all_' + str(time.time()) + '.bib'
        #consolidate_files("data/input/search/v3/", consolidated_filename)
        #consolidate_files("data/output/", consolidated_filename)

        # manual count (read file for certain strings)
        return count_records(filename)


def parse_consolidated_file(filename, timestamp):
    # parse file (the process of reading will remove some dupes)
    processed_lib = parse_file(filename)

    # FIXME - add a test to compare the pre-consolidated count with the final total
    # a manual check via loading the files in bibdesk is quite easy, in the mean time

    if len(processed_lib.failed_blocks) > 0:
        for failure in processed_lib.failed_blocks:
            print(failure.error)

        # you actually need to remove the failed (dupes) from the main block structure
        processed_lib.remove(processed_lib.failed_blocks)

        # remove duplicates by title
        # remove duplicates and return new, cleaned data structure
        # optional (could be left until post-processing)
        results = find_duplicates(processed_lib.entries)
        processed_lib = create_new_lib(results)

        # write the cleaned data back to a file
        cleaned_filename = 'data/output/deduped_' + timestamp + '.bib'
        save_file(processed_lib, cleaned_filename)


if __name__ == '__main__':

    timestamp = time.strftime("%d_%m_%Y_%H_%M_%S")

    consolidated_filename = 'data/output/consolidated_' + timestamp + '.bib'

    record_count = consolidation(consolidated_filename)

    if record_count > 0:
        parse_consolidated_file(consolidated_filename, timestamp)
    else:
        print('error : attempting to parse consolidated file with no entries')