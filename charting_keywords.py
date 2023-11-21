from charting import FIELD_TITLE, FIELD_KEYWORDS, top_x, CHART_COLOUR, add_labels_h

# FIXME try a word cloud;
# https://amueller.github.io/word_cloud/index.html

def chart_keywords(data, plt):
    keywords = {}
    for entry in data.entries:
        # keywords not populated for some data sources (e.g. DBLP)
        # look at titles instead (perhaps more accurate anyway?)
        if FIELD_TITLE in entry.fields_dict:
            #result = entry.fields_dict[FIELD_TITLE].value.split(',')
            result = entry.fields_dict[FIELD_TITLE].value.casefold().split()
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
        top_keywords_dict = top_x(sorted_keywords_list,30)

        x = list(top_keywords_dict.keys())
        y = list(top_keywords_dict.values())

        add_labels_h(plt, x, y, len(data.entries))
        plt.yticks([])
        plt.barh(x, y, color=CHART_COLOUR)
        plt.title("Green IT - Keywords")
        plt.ylabel("Keyword")
        plt.xlabel("Publication Count")
    else:
        print('No Keywords Found!')

def chart_actual_keywords(data, plt):
    keywords = {}
    for entry in data.entries:
        if FIELD_KEYWORDS in entry.fields_dict:
            result = entry.fields_dict[FIELD_KEYWORDS].value.casefold().split(',')
            # simply count the occurrences of all keywords
            for keyword_individual in result:
                cleaned_keyword = keyword_individual.strip()
                if cleaned_keyword in keywords:
                    keywords[cleaned_keyword] += 1
                else:
                    keywords[cleaned_keyword] = 1

    sorted_keywords_list = sorted(keywords.items(), key=lambda item: item[1])

    if len(sorted_keywords_list) > 0:
        top_keywords_dict = top_x(sorted_keywords_list,30)

        x = list(top_keywords_dict.keys())
        y = list(top_keywords_dict.values())

        add_labels_h(plt, x, y, len(data.entries))
        plt.yticks([])
        plt.barh(x, y, color=CHART_COLOUR)
        plt.title("Green IT - Actual Keywords")
        plt.ylabel("Keyword")
        plt.xlabel("Publication Count")
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
        if FIELD_TITLE in entry.fields_dict:
            title = entry.fields_dict[FIELD_TITLE].value.casefold()
            for keyphrase in keyphrases:
                if keyphrase in title:
                    keyphrases[keyphrase] += 1
            for grouped_line in groups:
                group_name = grouped_line.split(',')[0] + ' (*)'
                for grouped_keyphrase in grouped_line.split(','):
                    if grouped_keyphrase in title:
                        keyphrases[group_name] += 1
                        break # must avoid double counting here - break out once you've found one match in a group

    return keyphrases

def chart_keyphrases(data, plt):

    keywords = extract_keyphrases(data.entries)

    sorted_keywords_list = sorted(keywords.items(), key=lambda item: item[1])

    if len(sorted_keywords_list) > 0:
        top_keywords_dict = top_x(sorted_keywords_list,20)

        x = list(top_keywords_dict.keys())
        y = list(top_keywords_dict.values())

        add_labels_h(plt, x, y, len(data.entries))
        plt.yticks([])
        plt.barh(x, y, color=CHART_COLOUR)
        plt.title("Green IT - Key Phrases")
        plt.ylabel("Key Phrase")
        plt.xlabel("Publication Count")
    else:
        print('No Key Phrases Found!')