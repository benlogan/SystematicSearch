import time

from bibtexparser.model import Field

from parser import save_file, create_new_lib


def voting(data):

    vote_data = []

    breakout = False
    count = 0
    for entry in data.entries:
        count += 1
        if not breakout and 'vote' not in entry.fields_dict:
            print('')
            print('count : ' + str(count) + '/' + str(len(data.entries)))
            print(entry.fields_dict['title'].value)
            if 'journal' in entry.fields_dict:
                print(entry.fields_dict['journal'].value)

            keep = input("Vote Out? hit X :")
            # you can single-press enter to skip through quickly!
            # i.e. you are selectively excluding, not including

            fields_list = entry.fields
            value = 'IN'

            if keep == 'X' or keep == 'x':
                print('VOTING OUT')
                # let's add a new field...
                value = 'OUT'

            if keep == 'q':
                breakout = True
                #break - you can't just break out here, you need to process the full data set
            else:
                fields_list.append(Field('vote', value))

        # always append all - so that you always output a complete dataset
        vote_data.append(entry)

    lib = create_new_lib(vote_data)

    timestamp = time.strftime("%d_%m_%Y_%H_%M_%S")
    filename = 'data/output/voted_' + timestamp + '.bib'
    save_file(lib, filename)