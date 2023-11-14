from charting import FIELD_TITLE, top_x, CHART_COLOUR, add_labels_h

# FIXME try a word cloud;
# https://amueller.github.io/word_cloud/index.html

def chart_keywords(data, plt):
    keywords = {}
    for entry in data.entries:
        #if FIELD_KEYWORDS in entry.fields_dict:
        # keywords not populated for DBLP, look at titles instead (probably more accurate anyway)
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
            keywords.pop(line.strip()) # strip() removes the newline character at the end
            line = file.readline()

    sorted_keywords_list = sorted(keywords.items(), key=lambda item: item[1])

    if len(sorted_keywords_list) > 0:
        top_keywords_dict = top_x(sorted_keywords_list,40)

        x = list(top_keywords_dict.keys())
        y = list(top_keywords_dict.values())

        add_labels_h(plt, x, y)
        plt.yticks([])
        plt.barh(x, y, color=CHART_COLOUR)
        plt.title("Green IT Keywords")
        plt.ylabel("Keyword")
        plt.xlabel("Publication Count")
        plt.show()
    else:
        print('No Keywords Found!')

# FIXME join this phrase count to the keyword count (e.g. single word search like 'cloud')
# FIXME would be good if I didn't have to list these manually!
# OpenAI/Azure - 1st experiment wasn't successful (key phrase extraction)
def extract_keyphrases(data):
    keywords = {}
    groups = []

    with open('data/words/phrases.txt', 'r') as file:
        line = file.readline()
        while line:
            line = line.strip()
            if ',' in line:
                groups.append(line)
                # we still process them seperately, but group later...
                for grouped_keyphrase in line.split(','):
                    keywords[grouped_keyphrase] = 0
            else:
                keywords[line] = 0
            line = file.readline()

    for entry in data.entries:
        if FIELD_TITLE in entry.fields_dict:
            title = entry.fields_dict[FIELD_TITLE].value.casefold()
            for keyphrase in keywords:
                if keyphrase in title:
                    keywords[keyphrase] += 1

    # using the groups identified earlier, collate the counts and remove the individuals
    for grouped_line in groups:
        group_name = grouped_line.split(',')[0] + ' (*)'
        keywords[group_name] = 0
        for grouped_keyphrase in grouped_line.split(','):
            keywords[group_name] += keywords[grouped_keyphrase]
            del keywords[grouped_keyphrase]

    return keywords

def chart_keyphrases(data, plt):

    keywords = extract_keyphrases(data)

    sorted_keywords_list = sorted(keywords.items(), key=lambda item: item[1])

    if len(sorted_keywords_list) > 0:
        top_keywords_dict = top_x(sorted_keywords_list,15)

        x = list(top_keywords_dict.keys())
        y = list(top_keywords_dict.values())

        add_labels_h(plt, x, y, len(data.entries))
        plt.yticks([])
        plt.barh(x, y, color=CHART_COLOUR)
        plt.title("Green IT Key Phrases")
        plt.ylabel("Key Phrase")
        plt.xlabel("Publication Count")
        plt.show()
    else:
        print('No Key Phrases Found!')