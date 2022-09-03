"""
Implementation of lda search using jsd
"""

import math
import pandas as pd
from gensim.corpora import Dictionary
from topic_model.modelling import get_model
from util.common import get_testids
from util.constants import REPORT, ISSUE_ID


def get_search_query_corpus(project_name):
    """
    :param project_name:
    :return:
    """
    input_file_path = f"../data/normalized/{project_name}-norm-data.csv"
    docs = pd.read_csv(input_file_path)
    ids_for_test = get_testids(project_name)
    test_docs = docs[docs[ISSUE_ID].isin(ids_for_test)]
    tokenized_bugs = [str(x).split(' ') for x in test_docs[REPORT]]
    dictionary = Dictionary()
    search_query_corpus = [dictionary.doc2bow(doc, allow_update=True) for doc in tokenized_bugs]

    return search_query_corpus


def parse_topic_dist_file(topic_dist_filepath):
    """
    :param topic_dist_filepath:
    :return:
    """
    content = pd.read_csv(topic_dist_filepath)
    dist_dict_temp = {issue_id + 1: content['distribution'][issue_id].split(' ') for issue_id in
                      range(len(content.index))}
    dist_dict = {key: [float(x) for x in value] for key, value in dist_dict_temp.items()}
    return dist_dict


def calculate_similarity(doc_dist_list, query_dist_list, num_topics):
    """
    :param doc_dist_list:
    :param query_dist_list:
    :param num_topics:
    :return:
    """
    query_dist_dict = {x[0]: x[1] for x in query_dist_list}
    left_sum = right_sum = 0
    for i in range(num_topics):
        pw1 = doc_dist_list[i]
        pw2 = query_dist_dict[i]
        m_w = (pw1 + pw2) / 2
        left_sum += pw1 * math.log(pw1 / m_w)
        right_sum += pw2 * math.log(pw2 / m_w)

    jsd = left_sum / 2 + right_sum / 2
    return 1 - jsd


def get_topk_issueids(topic_dist_filepath, query_distributions, num_topics, topk):
    """
    :param topic_dist_filepath:
    :param query_distributions:
    :param num_topics:
    :param topk:
    :return:
    """
    issue_2_distributionlist = parse_topic_dist_file(topic_dist_filepath)
    result = {}
    for issue_id, dist_arr in issue_2_distributionlist.items():
        result[issue_id] = calculate_similarity(dist_arr, query_distributions, num_topics)
    sorted_result = dict(sorted(result.items(), key=lambda kv: -1 * kv[1])[:topk])
    print(f"sorted_result== {sorted_result}")
    return sorted_result


def get_duplicates_for_test(project_name, num_topics, topk):
    """
    :param project_name:
    :param num_topics:
    :param topk:
    :return:
    """
    topic_dist_filepath = f"../ldamodel/{project_name}-dist-{num_topics}.csv"
    norm_filepath = f"../data/normalized/{project_name}-norm-data.csv"
    norm_content = pd.read_csv(norm_filepath)
    ids_for_test = get_testids(project_name)
    model = get_model(project_name, num_topics)
    search_query_corpus = get_search_query_corpus(project_name)
    original_to_duplicate = pd.DataFrame(columns=['original', 'duplicate'])

    test_df = norm_content[norm_content[ISSUE_ID].isin(ids_for_test)]
    print(f'test_df size== {len(test_df.index)}')
    ind = 0
    for row in test_df.iterrows():
        issue_id = row[ISSUE_ID]
        query_distribution = model[search_query_corpus[ind]]
        query = row[REPORT]
        print(f"issue_id=={issue_id}")
        print(f"query=={query}")
        print(f"ind=={ind}")
        score_map = get_topk_issueids(topic_dist_filepath, query_distribution, num_topics, topk)
        # print(f"score_map=={score_map}")
        original_to_duplicate.loc[ind] = [issue_id] + [str(score_map)]
        ind += 1

    return original_to_duplicate
