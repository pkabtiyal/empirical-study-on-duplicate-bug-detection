"""
mrr and topk calculator
"""

import ast
import pandas as pd


def get_reciprocal_rank(original_dups, dups):
    """
    :param original_dups:
    :param dups:
    :return:
    """
    index = -1
    for original_dup in original_dups:
        if original_dup in dups:
            new_ind = dups.index(original_dup)
            # print(f"new_ind=== {new_ind}")
            index = new_ind if new_ind < index or new_ind == 0 else index

    return 1.0 / (index + 1) if index != -1 else 0


def get_mrr_topk(project_name, ir_model, topk, num_topics):
    """
    :param project_name:
    :param ir_model:
    :param topk:
    :param num_topics:
    :return:
    """
    score_file_path = f"../score_data/{project_name}-{ir_model}-{topk}-score.csv"
    if "lda" in ir_model:
        score_file_path = f"../score_data/{project_name}-{ir_model}-{num_topics}-{topk}-score.csv"
    actual_file_path = f"../data/{project_name}-test.csv"
    sum_mrr = 0
    total_success = 0
    score_df = pd.read_csv(score_file_path)
    actual_df = pd.read_csv(actual_file_path)
    actual_df = actual_df.dropna()
    actual_filtered = actual_df[actual_df['Duplicate'].str.lower() != "null"]
    a_id_duplicates = {}
    s_id_duplicates = {}
    for row in score_df.iterrows():
        score_dict = ast.literal_eval(row['duplicate'])
        dups = list(score_dict.keys())
        s_id_duplicates[row['original']] = dups

    for row in actual_filtered.iterrows():
        original_dups = row['Duplicate'].split(';')
        a_id_duplicates[row['issue_id']] = original_dups

    for s_id, dups in s_id_duplicates.items():
        if s_id in a_id_duplicates:
            original_dups = a_id_duplicates[s_id]
            reciprocal_rank = get_reciprocal_rank(original_dups, dups)
            sum_mrr += reciprocal_rank
            if list(set(original_dups) & set(dups)):
                total_success += 1
    # print(total_success)
    return sum_mrr / len(s_id_duplicates), total_success / len(s_id_duplicates)
