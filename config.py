"""Configurations For IGCSE Past Papers Downloader"""

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'
}

DATA_FOLDER = "data"
MARK_SCHEME_FOLDER = "mark_scheme"
QUESTION_PAPERS_FOLDER = "question_papers"
MERGED_FOLDER = "MERGED"
MERGED_FILE = "merged.pdf"
MERGED_TEMP_FILE = "merged_temp.pdf"
BANNED_PAPER_TYPES = ["ir", "gt", "er"]
SEASONS = ["summer", "mid-year(march) ", "winter"]

BASE_URL = "https://www.cienotes.com/cie-igcse-past-papers/"

PROMPT_FOR_FILTER = "Do you want to exclude certain paper code (yes or no): "
PROMPT_FOR_FILTER_IN_SEASON = "Do you want to filter any code in {} (yes or no): "
PROMPT_FOR_PAPER_CODE = "Which codes to filter (seperated by space): "
PROMPT_OPERATION = "Do You Want To Download Past Papers Or Merge Them(download or merge): "
