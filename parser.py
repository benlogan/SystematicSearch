import bibtexparser

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