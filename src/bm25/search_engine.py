"""
BM25 search engine
"""

import pandas as pd
from gensim.corpora import Dictionary
from gensim.summarization import bm25
from util.constants import REPORT, ISSUE_ID
from util.common import get_testids


def get_topk_issueids(bm25_obj, ids, query_doc, topk):
    """
    :param bm25_obj:
    :param ids:
    :param query_doc:
    :param topk:
    :return:
    """

    doc_scores = bm25_obj.get_scores(query_doc)
    result = {}
    ind = 0
    for iss_id in ids:
        result[iss_id] = doc_scores[ind]
        ind += 1
    sorted_result = dict(sorted(result.items(), key=lambda kv: -1 * kv[1])[:topk])
    print(f"sorted_result== {sorted_result}")
    return sorted_result


def get_duplicates_for_test(project_name, topk):
    """
    :param project_name:
    :param topk:
    :return:
    """
    normalized_corpus_file = f"../data/normalized/{project_name}-norm-data.csv"
    norm_content = pd.read_csv(normalized_corpus_file)
    ids_for_test = get_testids(project_name)
    original_to_duplicate = pd.DataFrame(columns=['original', 'duplicate'])
    test_df = norm_content[norm_content[ISSUE_ID].isin(ids_for_test)]
    print(f'test_df size== {len(test_df.index)}')

    tokenized_bugs = [str(x).split(' ') for x in norm_content[REPORT]]
    dictionary = Dictionary()
    corpus_bow = [dictionary.doc2bow(doc, allow_update=True) for doc in tokenized_bugs]

    bm25_obj = bm25.BM25(corpus_bow)
    ind = 0
    for row in test_df.iterrows():
        issue_id = row[ISSUE_ID]
        query = row[REPORT]
        print(f"issue_id=={issue_id}")
        print(f"query=={query}")
        print(f"ind=={ind}")
        query_doc = dictionary.doc2bow(str(query).split())
        score_map = get_topk_issueids(bm25_obj, norm_content[ISSUE_ID], query_doc, topk)
        original_to_duplicate.loc[ind] = [issue_id] + [str(score_map)]
        ind += 1
    return original_to_duplicate
