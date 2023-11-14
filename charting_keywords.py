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

def chart_keyphrases(data, plt):
    keywords = {}

    # examples...
    # FIXME add support for term grouping (e.g. all the software eng related terms below)
    # FIXME join this phrase count to the keyword count (e.g. single word search like 'cloud')
    keywords['virtual machines'] = 0
    keywords['data center'] = 0
    keywords['data centre'] = 0
    keywords['data centers'] = 0
    keywords['data centres'] = 0
    keywords['datacentres'] = 0
    keywords['datacenters'] = 0
    keywords['datacentre'] = 0
    keywords['datacenter'] = 0
    keywords['software engineering'] = 0
    keywords['software architecture'] = 0
    keywords['software development'] = 0
    keywords['software sustainability'] = 0
    keywords['big data'] = 0
    keywords['machine learning'] = 0
    keywords['deep learning'] = 0
    keywords['data science'] = 0
    keywords['artificial intelligence'] = 0
    keywords['green it'] = 0
    keywords['high performance'] = 0
    keywords['high-performance'] = 0
    keywords['green computing'] = 0
    keywords['cloud computing'] = 0
    keywords['task scheduling'] = 0
    keywords['job scheduling'] = 0
    keywords['resource allocation'] = 0
    keywords['resource scheduling'] = 0
    keywords['resource optimization'] = 0
    keywords['literature review'] = 0
    keywords['mapping study'] = 0
    keywords['survey'] = 0
    keywords['energy efficient'] = 0
    keywords['energy conservation'] = 0
    # FIXME would be good if I didn't have to list these! OpenAI/Azure - 1st experiment wasn't successful

    for entry in data.entries:
        if FIELD_TITLE in entry.fields_dict:
            title = entry.fields_dict[FIELD_TITLE].value.casefold()
            for keyphrase in keywords:
                if keyphrase in title:
                    keywords[keyphrase] += 1

    # FIXME manual grouping
    keywords['data center/centre'] = keywords['data center'] + keywords['data centre'] +\
        keywords['data centers'] + keywords['data centres'] +\
        keywords['datacentres'] + keywords['datacenters'] +\
        keywords['datacentre'] + keywords['datacenter']
    del keywords['data center']
    del keywords['data centre']
    del keywords['data centres']
    del keywords['data centers']
    del keywords['datacentre']
    del keywords['datacenter']
    del keywords['datacentres']
    del keywords['datacenters']

    keywords['software development/engineering'] = keywords['software engineering'] + keywords['software development']
    del keywords['software engineering']
    del keywords['software development']

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