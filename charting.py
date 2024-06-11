import datetime
import re
import matplotlib.pyplot as plt
import charting_keywords
import pandas as pd

from operator import itemgetter
from parser import parse_file

CHART_COLOUR = 'g'
FIELD_YEAR = 'year'
FIELD_JOURNAL = 'journal'
FIELD_AUTHOR = 'author'
FIELD_KEYWORDS = 'keywords'
FIELD_CATEGORIES = 'Categories_Extracted'
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
    total = 0
    for entry in data.entries:
        if FIELD_JOURNAL in entry.fields_dict:
            total = total + 1
            journal_string = entry.fields_dict[FIELD_JOURNAL].value.lower().strip()
            if journal_string in journals_dict:
                journals_dict[journal_string] += 1
            else:
                journals_dict[journal_string] = 1

    sorted_journal_list = sorted(journals_dict.items(), key=itemgetter(1))

    top_journals_dict = top_x(sorted_journal_list, 15)

    x = list(top_journals_dict.keys())
    y = list(top_journals_dict.values())

    add_labels_h(plt, x, y, total)
    plt.xticks(rotation=90)
    plt.yticks([])
    plt.barh(x, y, color=CHART_COLOUR)
    plt.title("Green IT - Popular Journals")
    plt.ylabel("Journal")
    plt.xlabel("Publication Count (total=" + str(total) + ')')

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

def increment_category(year, category):
    if year in category:
        category[year] = category[year] + 1
    else:
        category[year] = 1


if __name__ == '__main__':
    data = parse_file('data/enrichment/slr_enriched_cleaned_11_06_2024_17_22_22.bib')

    plt.figure(1, figsize=(6,5))
    chart_publications(data, plt)

    #plt.figure(2, figsize=(6,5))
    #chart_journals(data, plt)

    #plt.figure(3, figsize=(6,5))
    #chart_authors(data, plt)

    # limited value - may not include in final research...

    #plt.figure(4, figsize=(6,5))
    #chart_types(data, plt)

    #plt.figure(4, figsize=(6,10))
    #charting_keywords.chart_keywords(data, plt)

    plt.figure(4, figsize=(6,10))
    charting_keywords.chart_actual_keywords(data, plt, FIELD_KEYWORDS, "Green IT - Keywords")

    plt.figure(5, figsize=(6, 10))
    charting_keywords.chart_actual_keywords(data, plt, FIELD_CATEGORIES, "Green IT - Categories")

    # new data table; categories
    categories = []
    keywords = []
    with open('data/words/phrases.txt', 'r') as file:
        line = file.readline()
        while line:
            line = line.strip()

            categories.append(line.split(':')[0])
            keywords.append(line.split(':')[1].split(','))

            line = file.readline()

    table_data = {'Category':categories,'Keywords':keywords}
    df = pd.DataFrame(table_data, columns=['Category','Keywords'])

    fig, ax = plt.subplots(1, 1)
    ax.axis("tight")
    ax.axis("off")
    the_table = ax.table(cellText=df.values, colLabels=df.columns, loc="center", colWidths=[0.05,1])

    the_table.auto_set_font_size(False)
    the_table.set_fontsize(9)

    # new chart - categories by date
    # refactor this code before committing!!
    # I have the desired output, sort of
    # needs to be better use of data structures and
    # output needs to be comma seperated, and line seperated
    # (to prevent the need for further manipulation and enable direct use in excel)
    cloud = {}
    energy = {}
    alloc = {}
    vm = {}
    dc = {}
    sched = {}
    surv = {}
    ml = {}
    eng = {}
    green = {}
    hpc = {}
    lit = {}
    ent = {}

    for entry in data.entries:
        if FIELD_YEAR in entry.fields_dict:
            year_list = entry.fields_dict[FIELD_YEAR].value.casefold().split()
            year = year_list[0]
        if FIELD_CATEGORIES in entry.fields_dict:
            categories_list = entry.fields_dict[FIELD_CATEGORIES].value.casefold().split()
            if categories_list and categories_list[0]:
                categories = categories_list[0]
                if "cloud" in categories:
                    increment_category(year, cloud)
                if "energy" in categories:
                    increment_category(year, energy)
                if "alloc" in categories:
                    increment_category(year, alloc)
                if "vm" in categories:
                    increment_category(year, vm)
                if "dc" in categories:
                    increment_category(year, dc)
                if "sched" in categories:
                    increment_category(year, sched)
                if "surv" in categories:
                    increment_category(year, surv)
                if "ml" in categories:
                    increment_category(year, ml)
                if "eng" in categories:
                    increment_category(year, eng)
                if "green" in categories:
                    increment_category(year, green)
                if "hpc" in categories:
                    increment_category(year, hpc)
                if "lit" in categories:
                    increment_category(year, lit)
                if "ent" in categories:
                    increment_category(year, ent)
    print('cloud: ' + str(sorted(cloud.items())))
    print('energy: ' + str(sorted(energy.items())))
    print('alloc: ' + str(sorted(alloc.items())))
    print('vm: ' + str(sorted(vm.items())))
    print('dc: ' + str(sorted(dc.items())))
    print('sched: ' + str(sorted(sched.items())))
    print('surv: ' + str(sorted(surv.items())))
    print('ml: ' + str(sorted(ml.items())))
    print('eng: ' + str(sorted(eng.items())))
    print('green: ' + str(sorted(green.items())))
    print('hpc: ' + str(sorted(hpc.items())))
    print('lit: ' + str(sorted(lit.items())))
    print('ent: ' + str(sorted(ent.items())))

    plt.show()