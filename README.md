# SystematicSearch
 A python application for developing systematic searches of research literature

# The Process...

The aim of the search process is to build a collection of BibTeX files, one for each of your preferred databases.

You can either download your search results manually, or you can attempt to automate that step, using the code provided.

That code is a mixture of API calls, web scraping, or simple http requests, depending on the database in question.

For example, to execute the dblp search, run
download_dblp.py - this will produce a series of BibTeX extracts, in the /download directory.

You can use the utility code for quickly and easily consolidating those extracts into a single file - utility.py (consolidate_files)