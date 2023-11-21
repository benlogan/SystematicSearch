import datetime
import re

from operator import itemgetter

CHART_COLOUR = 'g'
FIELD_YEAR = 'year'
FIELD_JOURNAL = 'journal'
FIELD_AUTHOR = 'author'
FIELD_KEYWORDS = 'keywords'
FIELD_TITLE = 'title'
CHART_LABEL_OFFSET = 0.02

def add_labels(plt, x, y):
    # plt.text is using data coordinates here
    # (so stating 5, for example, will result in different placement for different charts!)
    # we could go to relative positioning using transform=ax.transAxes, but then Y pos will get more complicated!
    # instead, let's take a percentage (2%) of the max value of Y - should result in a consistent position for different charts
    offset = max(y) * CHART_LABEL_OFFSET
    for i in range(len(x)):
        plt.text(i, offset, x[i], ha='center', rotation=90)

# for horizontal bar charts...
def add_labels_h(plt, x, y, total):
    offset = max(y) * CHART_LABEL_OFFSET
    for i in range(len(x)):
        #plt.text(offset, i, x[i], ha='left', va='center')
        # add the percentage of the total population
        plt.text(offset, i, x[i] + ' ' + str(round(y[i]/total*100,2)) + '%', ha='left', va='center')

# retrieve the top X elements from a sorted list (for charting a subset)
def top_x(sorted_list, x):
    top_x_list = []
    count = 0
    while count < x and count < len(sorted_list):
        top_x_list.append(sorted_list[(len(sorted_list) - 1) - count])
        count += 1

    top_x_dict = {}
    for t in top_x_list:
        top_x_dict[t[0]] = t[1]

    return top_x_dict

def chart_publications(data, plt):
    years_dict = {}
    for entry in data.entries:
        if FIELD_YEAR in entry.fields_dict:
            year_string = entry.fields_dict[FIELD_YEAR].value
            year = datetime.datetime.strptime(year_string, '%Y').date()
            if year in years_dict:
                years_dict[year] += 1
            else:
                years_dict[year] = 1

    sorted_years_dict = dict(sorted(years_dict.items()))
    sorted_years_dict.pop(datetime.date(2024, 1, 1), None)  # won't error if it doesn't exist

    plt.plot(list(sorted_years_dict.keys()), list(sorted_years_dict.values()), color=CHART_COLOUR)
    plt.title("Green IT - Publications Over Time")
    plt.xlabel("Publication Year")
    plt.ylabel("Publication Count")

def chart_journals(data, plt):
    journals_dict = {}
    for entry in data.entries:
        if FIELD_JOURNAL in entry.fields_dict:
            journal_string = entry.fields_dict[FIELD_JOURNAL].value.lower().strip()
            if journal_string in journals_dict:
                journals_dict[journal_string] += 1
            else:
                journals_dict[journal_string] = 1

    sorted_journal_list = sorted(journals_dict.items(), key=itemgetter(1))

    top10_journals_dict = top_x(sorted_journal_list, 10)

    x = list(top10_journals_dict.keys())
    y = list(top10_journals_dict.values())

    add_labels_h(plt, x, y, len(data.entries))
    plt.xticks(rotation=90)
    plt.yticks([])
    plt.barh(x, y, color=CHART_COLOUR)
    plt.title("Green IT - Popular Journals")
    plt.ylabel("Journal")
    plt.xlabel("Publication Count")

def chart_authors(data, plt):
    authors = {}
    for entry in data.entries:
        if FIELD_AUTHOR in entry.fields_dict:
            author_string = entry.fields_dict[FIELD_AUTHOR].value
            result = re.split(r'\s+and\s+', author_string)

            # simply count the occurrences of all names
            for author_individual in result:
                if author_individual == '':
                    # ignore (skip) blanks!
                    continue

                # deal with the fact that some names are formatted differently
                if ',' in author_individual:
                    split_name = author_individual.split(',')
                    second_name = split_name[0]
                    first_name = split_name[1]
                    author_individual = first_name.strip() + ' ' + second_name.strip()

                if author_individual in authors:
                    authors[author_individual] += 1
                else:
                    authors[author_individual] = 1

    sorted_authors_list = sorted(authors.items(), key=lambda item: item[1])

    top10_authors_dict = top_x(sorted_authors_list, 10)

    x = list(top10_authors_dict.keys())
    y = list(top10_authors_dict.values())

    add_labels(plt, x, y)
    plt.xticks([])
    plt.bar(x, y, color=CHART_COLOUR)
    plt.title("Green IT - Authors")
    plt.xlabel("Author")
    plt.ylabel("Publication Count")

def chart_types(data, plt):
    types = {}
    for entry in data.entries:
        type = entry.entry_type
        if type in types:
            types[type] += 1
        else:
            types[type] = 1

    sorted_types_list = sorted(types.items(), key=lambda item: item[1])

    top10_types_dict = top_x(sorted_types_list, 10)

    x = list(top10_types_dict.keys())
    y = list(top10_types_dict.values())

    add_labels(plt, x, y)
    plt.xticks([])
    plt.bar(x, y, color=CHART_COLOUR)
    plt.title("Green IT - Publication Types")
    plt.xlabel("Type")
    plt.ylabel("Publication Count")