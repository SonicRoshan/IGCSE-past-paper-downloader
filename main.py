"""IGCSE Past Papers Downloader"""
import os
import requests
import bs4

from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
import config

def mkdir(name):
    """Makes a dir if that dir does not exist"""
    try:
        os.mkdir(name)
    except FileExistsError:
        pass

def get_paper_data(paper_name):
    """Gets paper code and paper type based on paper name"""
    split = paper_name.split("_")
    code = split[-1]
    paper_type = split[-2]

    if len(split) == 5:
        code = split[-2] + split[-3]
        paper_type = split[-1]

    elif len(split) == 3:
        code = "00"
        paper_type = split[-1]

    return code, paper_type

def pdf_merge(folder):
    """Merges all pdfs in a folder and returnes merged file"""
    pdfs = [f for f in os.listdir(folder)
            if os.path.isfile(os.path.join(folder, f))]

    merger = PdfFileMerger()

    for pdf in pdfs:
        merger.append("{}/{}".format(folder, pdf))

    return merger

def remove_blank_pages(input_file_name, output_file_name):
    """Removes all blank pages from a pdf"""
    input_file = open(input_file_name, "rb")
    reader = PdfFileReader(input_file)
    writer = PdfFileWriter()

    for page_number in range(reader.getNumPages()):
        page = reader.getPage(page_number)
        if "BLANK PAGE" not in page.extractText():
            writer.addPage(page)

    output_file = open(output_file_name, "wb")
    writer.write(output_file)
    input_file.close()
    output_file.close()


def get_data_from_user():
    """Ask And Get Data About Subject And Dates From User"""
    to_filter = {
        "s" : [],
        "m" : [],
        "w" : [],
    }
    paper_code = input("Paper Code: ")
    start_year = int(input("Start Year: "))
    end_year = int(input("End Year: "))

    should_filter = input(config.PROMPT_FOR_FILTER) == "yes"
    if should_filter:
        for season in config.SEASONS:
            if input(config.PROMPT_FOR_FILTER_IN_SEASON) == "yes":
                codes_to_filter = input(config.PROMPT_FOR_PAPER_CODE)
                to_filter[season[0]].extend(codes_to_filter.split(" "))

    return paper_code, start_year, end_year, to_filter

def get_subject_url(paper_code):
    """Gets Subject's URL Based On Subject Code"""
    html_data = requests.get(config.BASE_URL, headers=config.HEADERS).content
    soup = bs4.BeautifulSoup(html_data, 'lxml')
    div = soup.find("div", attrs={"class":"entry clr", "itemprop" : "text"})
    subjects = div.findAll("p")

    for subject in subjects:
        if paper_code in subject.getText():
            return subject.find("a").get("href")

    raise Exception("Invalid Paper Code")

def get_each_years_url(subject_url, start_year, end_year):
    """Returns each years url from start year to end year of a subject"""
    output = []
    html_data = requests.get(subject_url, headers=config.HEADERS).content
    soup = bs4.BeautifulSoup(html_data, 'lxml')
    div = soup.find("div", attrs={"class":"entry clr", "itemprop" : "text"})
    years_to_get = list(range(start_year, end_year + 1))
    years = div.findAll("p")

    for year in years:
        try:
            link = year.find("a").get("href")
            if any([str(year_to_get) in link and "past-papers" in link
                    for year_to_get in years_to_get]):
                output.append(link)
        except AttributeError:
            pass

    return output

def get_papers_urls(year_url):
    """return all papers' url from a year url"""
    papers_urls = {}
    html_data = requests.get(year_url, headers=config.HEADERS).content
    soup = bs4.BeautifulSoup(html_data, 'lxml')
    div = soup.find("div", attrs={"class":"entry-content clr", "itemprop" : "text"})
    papers = div.findAll("p")

    for paper in papers:
        if " " not in paper.getText():
            papers_urls[paper.getText()] = paper.find("a").get("href")

    return papers_urls

def download_papers(paper_code, years_urls, to_filter):
    """Download all papers from a dict of paper urls"""
    for year_url in years_urls:
        papers_urls = get_papers_urls(year_url)
        papers_urls = filter_papers(papers_urls, to_filter)

        question_papers_folder = "{}/{}/{}".format(
            config.DATA_FOLDER,
            paper_code,
            config.QUESTION_PAPERS_FOLDER
        )

        mkdir(question_papers_folder)
        mkdir("{}/{}/{}".format(config.DATA_FOLDER, paper_code, config.MARK_SCHEME_FOLDER))
        num = len(os.listdir(question_papers_folder))

        for paper_name, paper_url in papers_urls.items():
            _, paper_type = get_paper_data(paper_name)
            print("Downloading {}".format(paper_name))

            if paper_type != "ms":
                folder = config.QUESTION_PAPERS_FOLDER
            else:
                folder = config.MARK_SCHEME_FOLDER

            data = requests.get(paper_url, headers=config.HEADERS).content

            name = "{}/{}/{}/{}_{}.pdf".format(config.DATA_FOLDER,
                                               paper_code,
                                               folder,
                                               num,
                                               paper_name)
            with open(name+"_temp", "wb") as file:
                file.write(data)

            remove_blank_pages(name+"_temp", name)
            os.remove(name+"_temp")


def filter_papers(papers_urls, to_filter):
    """Filters papers"""
    output = {}

    for paper_name, paper_url in papers_urls.items():
        season = paper_name.split("_")[1][0]
        code, paper_type = get_paper_data(paper_name)

        if code not in to_filter[season] and paper_type not in config.BANNED_PAPER_TYPES:
            output[paper_name] = paper_url

    return output


def download():
    """Downloads past papers"""
    paper_code, start_year, end_year, to_filter = get_data_from_user()
    subject_url = get_subject_url(paper_code)
    years_urls = get_each_years_url(subject_url, start_year, end_year)

    mkdir(config.DATA_FOLDER)
    mkdir(paper_code)

    download_papers(paper_code, years_urls, to_filter)

def merge():
    """merges past papers"""
    paper_code = input("Enter Paper Code To Merge: ")
    os.chdir(config.DATA_FOLDER)

    os.chdir(paper_code)
    mkdir(config.MERGED_FOLDER)

    merger = pdf_merge(config.QUESTION_PAPERS_FOLDER)

    os.chdir(config.MERGED_FOLDER)
    merger.write(config.MERGED_FILE)
    remove_blank_pages(config.MERGED_FILE, "temo.pdf")

def main():
    """Main Loop"""
    operation = input(config.PROMPT_OPERATION)
    if operation.lower() == "merge":
        merge()
    else:
        download()

if __name__ == "__main__":
    main()
