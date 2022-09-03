"""
Module for combining the similarity scored obtained from bm25 and topic model
"""

import ast
import pandas as pd


def run_combined(project_name, num_topics, topk):
    """
    Combines the similarity scores for two models bm25 and topic model
    :param project_name:
    :param num_topics:
    :param topk:
    :return:
    """
    file1 = f"../score_data/{project_name}-bm25-{topk}-score.csv"
    file2 = f"../score_data/{project_name}-lda-{num_topics}-{topk}-score.csv"

    bm_df = pd.read_csv(file1)
    lda_df = pd.read_csv(file2)
    bm_dict = {}
    lda_dict = {}
    for row in bm_df.iterrows():
        score_dict = ast.literal_eval(row['duplicate'])
        bm_dict[row['original']] = score_dict

    for row in lda_df.iterrows():
        score_dict = ast.literal_eval(row['duplicate'])
        lda_dict[row['original']] = score_dict

    final_df = pd.DataFrame(columns=['original', 'duplicate'])
    ind = 0
    for issue_id, dict_from_lda in lda_dict.items():
        dict_from_bm25 = bm_dict[issue_id]
        duplicate_dict = dict(dict_from_lda)
        duplicate_dict.update(dict_from_bm25)
        for i_lda, j_lda in dict_from_lda.items():
            for x_bm, y_bm in dict_from_bm25.items():
                if i_lda == x_bm:
                    duplicate_dict[i_lda] = (j_lda + y_bm)
        sorted_result = dict(sorted(duplicate_dict.items(), key=lambda kv: -1 * kv[1]))
        final_df.loc[ind] = [issue_id] + [str(sorted_result)]
        ind += 1

    score_file = f"../score_data/{project_name}-bmlda-{num_topics}-{topk}-score.csv"
    final_df.to_csv(score_file)
