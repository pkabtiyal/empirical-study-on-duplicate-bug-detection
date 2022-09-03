"""
Runner for lda search
"""
from topic_model.lda_search_engine import get_duplicates_for_test

if __name__ == "__main__":

    # eclipse
    PROJECT_NAME = "eclipse"
    for num_topics in [20, 50, 80, 100, 120, 140]:
        for topk in [5, 10, 15]:
            scores = get_duplicates_for_test(PROJECT_NAME, num_topics, topk)
            scores.to_csv(f"../score_data/{PROJECT_NAME}-lda-{num_topics}-{topk}-score.csv")

    # mozilla
    PROJECT_NAME = "mozilla"
    for num_topics in [20, 50, 80, 100, 120, 140]:
        for topk in [5, 10, 15]:
            scores = get_duplicates_for_test(PROJECT_NAME, num_topics, topk)
            scores.to_csv(f"../score_data/{PROJECT_NAME}-lda-{num_topics}-{topk}-score.csv")
