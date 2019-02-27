# gold-crowd
A platform to create crowd-sourced gene function gold standards with Amazon Mechanical Turk

## Installation
1. Download the repository
2. Change into it and `pipenv install` python dependencies

## Usage
1. Put the [Pubmed IDs](https://www.ncbi.nlm.nih.gov/pmc/pmctopmid/) of the abstracts you're interested in into `data/pmid_list.txt`
2. Run `pipenv run python process.py`
3. Output is in `data/abstracts` and `data/brat-input`. Put all files from these folders together in the same folder of your [brat](http://brat.nlplab.org/index.html) installation. In that same folder you will also need a file `annotation.conf` that could look like this (more information [here](http://brat.nlplab.org/configuration.html)):
    ```
    [entities]

    Gene
    Function

    [relations]

    Does	Arg1:Gene, Arg2:Function
    Does	Arg1:Function, Arg2:Gene
    DoesNot	Arg1:Function, Arg2:Gene
    DoesNot	Arg1:Gene, Arg2:Function

    [attributes]

    [events]
    ```
    There will also be a file `data/statistics.cvs` containing the number of words, genes, and functions for each abstract.
