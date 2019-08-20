# IGCSE-past-paper-downloader
Download All IGCSE Past Papers And Mark Schemes Of Any Subject

## Features
1. Download A Subjects's Past IGCSE Papers Just By Giving Start And End Year
2. Filter Any Papers You Dont Need. For Example You Could Filter Out All Physics Practical Papers If You Want To
3. Merge All Subject's Paper Into One PDF.

## Requirements
```
pip install PyPDF2 requests beautifulsoup4
```

## How To Download
1. Run main.py
2. Enter download when it asks you to either merge or download
3. Enter subject code for example 0625 for physics
4. Enter start year and year
5. If ypu want to filter certain papers, say yes when program asks you to filter certain papers
6. Add codes of paper to filter. For example if you want to filter practical papers from physics, enter 51 52 53 for summer and winter, and 52 for march.
7. Voila!!, papers will start downloading
8. Papers will be in data folder

## How to merge
1. Run main.py
2. Enter merge when it asks you to either merge or download
3. Enter subject code, but make sure you have already downloaded that subject's papers
4. The merged file will be in data folder, in subject code folder, in merged folder.