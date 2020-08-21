# iXBRL Parser

Scrap/parse annual reports in iXBRL format from HTML or XHTML source to CSV table.

## What is XBRL

-- Some companies publish annual reports with [XBRL/iXBRL tags](https://en.wikipedia.org/wiki/XBRL) 
-- These tags essentially allow identification of certain positions in annual reports (machine readable)
-- This allows for automated reading/parsing of annual reports in HTML or XHTML format to structured table data

## Related Work

There are related projects for Python and R. I benefited from work by [ONSBigData](https://github.com/ONSBigData/parsing_company_accounts), where some very helpful options to parse company accounts are presented. I also found [this blogpost](https://www.codeproject.com/Articles/1227765/Parsing-XBRL-with-Python) helpful. There are other Python approaches, such as [this one](https://github.com/bergant/XBRLFiles) by [David Kane](https://dkane.net/2018/working-with-xbrl/).

There is also some work in R, such as the [XBRL package](https://cran.r-project.org/web/packages/XBRL/XBRL.pdf), but I did not look into this work a lot, since I had trouble setting up the installation. 

## My Approach

In order to understand the structure of XBRL tagged annual reports published as HTML or XHTML file, I set up a very basic linear parser which retrieves XBRL tagged content. Dependencies are kept to an absolute minimum. The aim is to show how to access relevant content. 

A locally stored HTML or XHTML file is loaded, XBRL tagged content is parsed, and tagged content is stored in a [CSV table](https://github.com/Bixi81/iXBRL/blob/master/myxbrltable.csv).

For testing, I used the annual report of [GLEIF](https://www.gleif.org/en/about/governance/annual-report/). I did not so much testing so far. 

Find the Python code [here](https://github.com/Bixi81/iXBRL/blob/master/read_xbrl.py).




