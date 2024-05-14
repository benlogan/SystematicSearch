import re

def categorize_title(title):
    categories = []
    if "energy" in title.lower() or "power" in title.lower() or "efficient" in title.lower():
        categories.append('ENERGY')
    if "cloud" in title.lower():
        categories.append('CLOUD')
    if "resource" in title.lower() or "allocation" in title.lower() or "placement" in title.lower():
        categories.append('ALLOC')
    if "scheduling" in title.lower():
        categories.append('SCHED')
    if "vm" in title.lower() or "virtual machine" in title.lower():
        categories.append('VM')
    if "data center" in title.lower() or "datacentre" in title.lower():
        categories.append('DC')
    if "simulation" in title.lower():
        categories.append('SIM')
    if "measurement" in title.lower() or "measuring" in title.lower():
        categories.append('MEAS')

    return ', '.join(categories)

# Replace 'path_to_your_bib_file.bib' with the path to your .bib file
with open('data/enrichment/voted_14_04_2024_21_52_28.bib', 'r') as file:
    content = file.read()

# Extracting titles
titles = re.findall(r'title\s*=\s*{([^}]+)}', content, re.IGNORECASE)

# Categorizing titles
categorized_titles = {title: categorize_title(title) for title in titles}

# Output results
for title, categories in categorized_titles.items():
    print(f"Title: {title}\nCategories: {categories}\n")
