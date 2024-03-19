# SystematicSearch
 Python application for developing systematic (programmable) searches of academic research literature.

## The Process...

The aim of the search process is to build a collection of BibTeX files; one for each of your preferred databases.

You can either download your search results manually, or you can attempt to automate that step, using the code provided.

That code is a mixture of API calls, web scraping, or simple HTTP requests, depending on the database in question.

For example, to execute the dblp search, run
download_dblp.py - this will produce a series of BibTeX extracts, in the /download directory.

You can use the utility code for quickly and easily consolidating those extracts into a single file - utility.py (consolidate_files)

Use the post processor; post_process.py, to reapply the search (reapply_search) - this is necessary because of the many data quality issues resulting from the database searches. The research portals are highly unreliable and inconsistent in their search implementations.

The steps are broadly as follows. Some of these steps can be skipped and the process is deliberately modular, so that you can plug your data in at various stages of the pipeline, with offline data adjustments (e.g. manual deletions) if required.

### 1. Search (execution of)

Due to the intricacies and idiosyncrasies of academic research databases (and their associated search engines), you will likely need to build individual search queries that are customised for each database.

e.g. download_dblp.py

This typically results in an output data file (data/downloads) with the following naming convention;

source_date_timestamp.bib

e.g. dblp_2023_1698748522.405377.bib

Note that this process will also consolidate multiple files for a single data source, where searches at an individual database (e.g. DBLP) have been broken down - for example, executed seperately for each year (often required in order to work around limitations with the result set size).

The consolidated results can be found here; 
data/output/consolidated_*.bib

### 2. Consolidation (of results)

Your search will have been unique to your target research database (e.g. DBLP). If you are searching across multiple databases, then there is a simple process for consolidating (merging) multiple data sets.

This is the process for merging datasets from across different data sources. If you have multiple datasets from a single data source, they should have been consolidated before this step.

process_raw_data is the function.

This typically results in an output data file (data/output) with the following naming convention;
data/output/deduped_timestamp.bib

### 3. Post Processing

At this stage, you will have cleaned and consolidated data from a number of underlying data sources. You could, at this point, start your data analysis or visualisation.

The post-processing can involve;
<ul>
<li>Reapplying the original search query - executing the search 'in code' over the top of the original dataset. This is the primary purpose of the post-processor - this was found to be VERY useful, because of the poor search implementations at source (e.g. lack of case sensitivity support).</li>
<li>Support for exclusion criteria - removing publications where there is a title word match on a particular word. If you have a broad search term, this can be particularly useful.</li>
<li>Removing duplicates (again, in code - this is more reliable).</li>
<li>Removing certain types of publications (e.g. 'proceedings').</li>
</ul>

post_process.py
is a standalone executable Python application that will;
<ol>
<li>take a .bib file as input</li>
<li>execute a series of post-processing data manipulation steps on your data</li>
<li>return a new output file, with the following naming convention;</li>
</ol>

data/output/cleaned_*_timestamp.bib

### 4. Charting (visualising results)

Visualising your results (using matplotlib). There is an executable main function in charting.py that will take a .bib file as input and then generate a series of charts based on a number of pre-defined dimensions in the data. It will currently produce 7 different charts;
<ul>    
<li>chart_publications</li>
<li>chart_journals</li>
<li>chart_authors</li>
<li>chart_types</li>
<li>chart_keywords</li>
<li>chart_actual_keywords</li>
<li>chart_keyphrases</li>
</ul>