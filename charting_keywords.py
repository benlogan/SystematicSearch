import charting

# FIXME try a word cloud;
# https://amueller.github.io/word_cloud/index.html

def chart_keywords(data, plt):
    keywords = {}
    for entry in data.entries:
        # keywords not populated for some data sources (e.g. DBLP)
        # look at titles instead (perhaps more accurate anyway?)
        if charting.FIELD_TITLE in entry.fields_dict:
            #result = entry.fields_dict[FIELD_TITLE].value.split(',')
            result = entry.fields_dict[charting.FIELD_TITLE].value.casefold().split()
            # simply count the occurrences of all keywords
            for keyword_individual in result:
                cleaned_keyword = keyword_individual.lower().strip()
                cleaned_keyword = cleaned_keyword.replace(':','')
                if cleaned_keyword in keywords:
                    keywords[cleaned_keyword] += 1
                else:
                    keywords[cleaned_keyword] = 1

    # exclusions (common words)
    with open('data/words/common_words.txt', 'r') as file:
        line = file.readline()
        while line:
            if line.strip() in keywords:
                keywords.pop(line.strip()) # strip() removes the newline character at the end
            line = file.readline()

    sorted_keywords_list = sorted(keywords.items(), key=lambda item: item[1])

    if len(sorted_keywords_list) > 0:
        top_keywords_dict = charting.top_x(sorted_keywords_list,30)

        x = list(top_keywords_dict.keys())
        y = list(top_keywords_dict.values())

        charting.add_labels_h(plt, x, y, len(data.entries))
        plt.yticks([])
        plt.barh(x, y, color=charting.CHART_COLOUR)
        plt.title("Green IT - Keywords")
        plt.ylabel("Keyword")
        plt.xlabel("Publication Count")
    else:
        print('No Keywords Found!')


def chart_actual_keywords(data, plt, field, title):
    keywords = {}
    total = 0
    for entry in data.entries:
        if field in entry.fields_dict:
            total = total + 1
            result = entry.fields_dict[field].value.casefold().split(',')
            # simply count the occurrences of all keywords
            for keyword_individual in result:
                cleaned_keyword = keyword_individual.strip().upper()
                if cleaned_keyword in keywords:
                    keywords[cleaned_keyword] += 1
                else:
                    keywords[cleaned_keyword] = 1

    sorted_keywords_list = sorted(keywords.items(), key=lambda item: item[1])

    if len(sorted_keywords_list) > 0:
        top_keywords_dict = charting.top_x(sorted_keywords_list,14)

        # manual chart exclusions (refactor this code)
        if '' in top_keywords_dict:
            del top_keywords_dict['']
        if 'LIT' in top_keywords_dict:
            del top_keywords_dict['LIT']
        if 'ACAD' in top_keywords_dict:
            del top_keywords_dict['ACAD']

        x = list(top_keywords_dict.keys())
        y = list(top_keywords_dict.values())

        charting.add_labels_h(plt, x, y, total)
        plt.yticks([])
        plt.barh(x, y, color=charting.CHART_COLOUR)
        plt.title(title)
        plt.ylabel("Keyword")
        plt.xlabel("Publication Count (total=" + str(total) + ')')
    else:
        print('No Keywords Found!')


# FIXME join this phrase count to the keyword count (e.g. single word search like 'cloud')
# FIXME would be good if I didn't have to list these manually!
# OpenAI/Azure - 1st experiment wasn't successful (key phrase extraction)
def extract_keyphrases(data):
    keyphrases = {}
    groups = []

    with open('data/words/phrases.txt', 'r') as file:
        line = file.readline()
        while line:
            line = line.strip()
            if ',' in line:
                groups.append(line)
                group_name = line.split(',')[0] + ' (*)'
                keyphrases[group_name] = 0
            else:
                keyphrases[line] = 0
            line = file.readline()

    for entry in data:
        if charting.FIELD_TITLE in entry.fields_dict:
            title = entry.fields_dict[charting.FIELD_TITLE].value.casefold()
            for keyphrase in keyphrases:
                if keyphrase in title:
                    keyphrases[keyphrase] += 1
            for grouped_line in groups:
                group_name = grouped_line.split(',')[0] + ' (*)'
                for grouped_keyphrase in grouped_line.split(','):
                    if grouped_keyphrase in title:
                        keyphrases[group_name] += 1
                        break # must avoid double counting here - break out once you've found one match in a group
            print(title)
            print(keyphrases) # this is the entire dictionary, each time (not unique for the given title)

    return keyphrases


# redundant - this code used to be used to extract key phrases at runtime, during charting
# categorisation is now done as a post-processing step, earlier in the data pipeline
def chart_keyphrases(data, plt):

    keywords = extract_keyphrases(data.entries)

    sorted_keywords_list = sorted(keywords.items(), key=lambda item: item[1])

    if len(sorted_keywords_list) > 0:
        top_keywords_dict = charting.top_x(sorted_keywords_list,20)

        x = list(top_keywords_dict.keys())
        y = list(top_keywords_dict.values())

        charting.add_labels_h(plt, x, y, len(data.entries))
        plt.yticks([])
        plt.barh(x, y, color=charting.CHART_COLOUR)
        plt.title("Green IT - Key Phrases")
        plt.ylabel("Key Phrase")
        plt.xlabel("Publication Count")
    else:
        print('No Key Phrases Found!')