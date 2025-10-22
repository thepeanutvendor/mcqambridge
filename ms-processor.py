# This script creates a JSON file with extracted answers from CIE marking schemes for MCQ papers.

import os
import requests
import json
from docx.api import Document
from pdf2docx import Converter

ROOT_DIR = os.getcwd()
ANSWERS_PATH = os.path.join(ROOT_DIR, 'static', 'answers.json')

try:
    with open(ANSWERS_PATH, 'r') as fh:
        final_json = json.load(fh) or {}
except Exception:
    final_json = {}

subjects = [
    # IGCSE
    "IGCSE/Economics-0455",
    "IGCSE/Biology-0610",
    "IGCSE/Chemistry-0620",
    "IGCSE/Physics-0625",
    "IGCSE/Science-Combined-0653",

    # O-Levels
    "O-Level/Economics-2281",
    "O-Level/Physics-5054",
    "O-Level/Chemistry-5070",
    "O-Level/Biology-5090",
    "O-Level/Science-Combined-5129",
    # A-Levels
    "A-Level/Biology-9700",
    "A-Level/Chemistry-9701",
    "A-Level/Physics-9702",
    "A-Level/Accounting-9706",
    "A-Level/Economics-9708"
]
# https://pastpapers.co/cie/O-Level/Accounting-7707/2024-May-June/7707_s24_ms_11.pdf
# https://pastpapers.co/cie/IGCSE/Accounting-0452/2024-March/0452_m24_ms_12.pdf

years = ['2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025']
months = ['m', 's', 'w']
levels = ['1', '2', '3']
variants = ['1', '2', '3']
errors = []


def url_exists(url):
    # Send a HEAD request to check if the URL exists
    response = requests.head(url)
    return response.status_code == requests.codes.ok


def extract_answers(file):
    # Converts given pdf 'file' to DOCX, extracts MCQ answers, and returns them as a list
    data = []
    WF = 'markingscheme.docx'
    cv = Converter(file)
    cv.convert(WF)
    wf_cont = Document(WF)

    for table in wf_cont.tables:
        for i, row in enumerate(table.rows):
            text = [cell.text for cell in row.cells]
            if i == 0:
                keys = tuple(text)
                continue
            row_data = dict(zip(keys, text))
            if 'Answer ' in row_data.keys():
                data.append(row_data['Answer '].strip())
            elif 'Answer' in row_data.keys():
                data.append(row_data['Answer'].strip())

    cv.close()
    return data


for subject in subjects:
    for year in years:
        for month in months:
            for level in levels:
                for variant in variants:
                    # Extract the subject code from the subject string
                    subj_code = subject.split('-')[-1]

                    # Construct the filename
                    file_name = f"{subj_code}_{month}{str(year)[2:4]}_ms_{level}{variant}.pdf"
                    # Skip certain combinations based on conditions

                    if file_name in final_json:
                        # already processed -> skip
                        continue

                    # Level 3 (A2) only exists for A-level Econ
                    if subject != "A-Level/Economics-9708" and level == '3':
                        continue

                    # Level 2 (Extended) exists only for certain science subjects in IGCSE
                    if level == '2':
                        if subject not in ["IGCSE/Physics (0625)", "IGCSE/Chemistry (0620)", "IGCSE/Biology (0610)", "IGCSE/Science Combined (0653)"]:
                            continue

                    # Construct the ms URL
                    if month == 'm' and year == '2022':
                        url_ms = f"https://pastpapers.co/cie/{subject}/{year}-Feb-March/{file_name}"
                    elif month == 'm':
                        url_ms = f"https://pastpapers.co/cie/{subject}/{year}-March/{file_name}"
                    elif month == 's':
                        url_ms = f"https://pastpapers.co/cie/{subject}/{year}-May-June/{file_name}"
                    elif month == 'w':
                        url_ms = f"https://pastpapers.co/cie/{subject}/{year}-Oct-Nov/{file_name}"

                    # Check if the URL exists
                    if url_exists(url_ms):
                        # Download it as 'ms.pdf'
                        r = requests.get(url_ms, allow_redirects=True)
                        open(os.path.join(ROOT_DIR, 'ms.pdf'),
                             'wb').write(r.content)
                        # Extract answers and add them to final_json
                        final_json[file_name] = extract_answers('ms.pdf')
                    else:
                        # Throw error
                        error = f"{file_name}, {subject}, {year}, {month}, {level}, {variant}"

                        print(error)
                        errors.append(error)

with open(ANSWERS_PATH, 'w') as f:
    json.dump(final_json, f, indent=2)

with open('errors.txt', 'w') as f:
    for error in errors:
        f.write("%s\n" % error)
