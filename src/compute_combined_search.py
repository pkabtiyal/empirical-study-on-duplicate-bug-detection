"""
Runner to combine the search results for top k- 5,1015
"""

from src.combined.bm_lda_calculator import run_combined

if __name__ == "__main__":
    PROJECT = "eclipse"
    NUM_TOPICS = 120
    for topk in [5, 10, 15]:
        run_combined(PROJECT, NUM_TOPICS, topk)

    PROJECT = "mozilla"
    NUM_TOPICS = 100
    for topk in [5, 10, 15]:
        run_combined(PROJECT, NUM_TOPICS, topk)
