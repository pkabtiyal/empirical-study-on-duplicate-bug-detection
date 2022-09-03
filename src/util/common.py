"""
This file contains common methods
"""

import os
import pandas as pd
from util.constants import ISSUE_ID


def check_to_create_dir(file_path):
    """
    :param file_path:
    :return:
    """
    temp = file_path.rsplit("/", 1)
    path = temp[0]
    if not os.path.exists(path):
        os.mkdir(path)


def get_testids(project_name):
    """
    :param project_name:
    :return:
    """
    content_df = pd.read_csv(f"../data/{project_name}-test.csv")
    without_na = content_df.dropna()
    filtered = without_na[without_na['Duplicate'].str.lower() != "null"]
    print(f'filtered=={len(filtered.index)}')
    return list(filtered[ISSUE_ID])
