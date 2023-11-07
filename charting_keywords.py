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
    keywords.pop('for')
    keywords.pop('and')
    keywords.pop('in')
    keywords.pop('of')
    keywords.pop('a')
    keywords.pop('the')
    keywords.pop('on')
    keywords.pop('an')
    keywords.pop('with')
    keywords.pop('to')
    keywords.pop('using')
    keywords.pop('based')
    keywords.pop('{a}')
    keywords.pop('approach')
    keywords.pop('towards')
    keywords.pop('-')
    keywords.pop('analysis')
    keywords.pop('high')
    keywords.pop('aware')
    keywords.pop('task')
    keywords.pop('dynamic')

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

def chart_keyphrases(data, plt):
    keywords = {}

    # examples...
    # FIXME add support for term grouping (e.g. all the software eng related terms below)
    # FIXME join this phrase count to the keyword count (e.g. single word search like 'cloud')
    keywords['virtual machines'] = 0
    keywords['data center'] = 0
    keywords['data centre'] = 0
    keywords['software engineering'] = 0
    keywords['software architecture'] = 0
    keywords['software development'] = 0
    keywords['software sustainability'] = 0
    keywords['big data'] = 0
    keywords['machine learning'] = 0
    keywords['artificial intelligence'] = 0
    keywords['green it'] = 0
    keywords['high performance'] = 0
    keywords['green computing'] = 0
    keywords['cloud computing'] = 0
    keywords['task scheduling'] = 0
    keywords['literature review'] = 0
    # FIXME would be good if I didn't have to list these! OpenAI/Azure - 1st experiment wasn't successful

    for entry in data.entries:
        if FIELD_TITLE in entry.fields_dict:
            title = entry.fields_dict[FIELD_TITLE].value.casefold()
            for keyphrase in keywords:
                if keyphrase in title:
                    keywords[keyphrase] += 1

    sorted_keywords_list = sorted(keywords.items(), key=lambda item: item[1])

    if len(sorted_keywords_list) > 0:
        top_keywords_dict = top_x(sorted_keywords_list,15)

        x = list(top_keywords_dict.keys())
        y = list(top_keywords_dict.values())

        add_labels_h(plt, x, y)
        plt.yticks([])
        plt.barh(x, y, color=CHART_COLOUR)
        plt.title("Green IT Key Phrases")
        plt.ylabel("Key Phrase")
        plt.xlabel("Publication Count")
        plt.show()
    else:
        print('No Key Phrases Found!')