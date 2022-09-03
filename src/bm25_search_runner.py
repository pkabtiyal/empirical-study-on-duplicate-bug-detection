"""
Runner to get bm25 top 5, 10 and 15 search results for eclipse and mozilla
"""

from bm25.search_engine import get_duplicates_for_test

if __name__ == "__main__":
    # eclipse
    PROJECT_NAME = "eclipse"
    for topk in [5, 10, 15]:
        scores = get_duplicates_for_test(PROJECT_NAME, topk)
        scores.to_csv(f"../score_data/{PROJECT_NAME}-bm25-{topk}-score.csv")

    # mozilla
    PROJECT_NAME = "mozilla"
    for topk in [5, 10, 15]:
        scores = get_duplicates_for_test(PROJECT_NAME, topk)
        scores.to_csv(f"../score_data/{PROJECT_NAME}-bm25-{topk}-score.csv")
