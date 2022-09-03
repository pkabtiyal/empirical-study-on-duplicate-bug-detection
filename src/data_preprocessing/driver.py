"""
driver for data preprocessing module
"""

import pandas as pd
from data_preprocessing.text_normalizer import normalize_data
from util.common import check_to_create_dir
from util.constants import ISSUE_ID, REPORT, DESCRIPTION, TITLE


def run(project_name):
    """
    :param project_name:
    :return:
    """
    input_file_path = f"../data/raw/{project_name}.csv"
    output_file_path = f"../data/normalized/{project_name}-norm-data.csv"
    check_to_create_dir(output_file_path)

    content = pd.read_csv(input_file_path)
    docs = pd.DataFrame()
    docs[ISSUE_ID] = content.Issue_id
    docs[REPORT] = content[DESCRIPTION].str.lower() + ' ' + content[TITLE].str.lower()
    docs = docs.dropna()
    processed_docs = docs
    processed_docs[REPORT] = docs[REPORT].map(normalize_data)

    processed_docs.to_csv(output_file_path)
    print(f"Data has been processed and stored in {output_file_path}")
