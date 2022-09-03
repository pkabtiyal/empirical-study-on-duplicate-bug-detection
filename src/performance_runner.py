"""
Runner to get the MRR and Topk for eclipse and mozilla
"""

from performance_evaluator.calculator import get_mrr_topk

if __name__ == "__main__":
    # eclipse
    PROJECT_NAME = "eclipse"
    print(f"\n************** Performance on {PROJECT_NAME} Dataset ***************\n")
    ir_models = ["bm25", "lda", "bmlda"]
    NUM_TOPICS = 120
    for k in [5, 10, 15]:
        for ir_model in ir_models:
            mrr, topk = get_mrr_topk(PROJECT_NAME, ir_model, k, NUM_TOPICS)
            print(f"IR model {ir_model} || MRR@{k} = {mrr}")
            print(f"IR model {ir_model} || TOPK@{k} = {topk}\n")
            print("\n")

    # mozilla
    PROJECT_NAME = "mozilla"
    print(f"\n************** Performance on {PROJECT_NAME} Dataset ***************\n")
    ir_models = ["bm25", "lda", "bmlda"]
    NUM_TOPICS = 100
    for k in [5, 10, 15]:
        for ir_model in ir_models:
            mrr, topk = get_mrr_topk(PROJECT_NAME, ir_model, k, NUM_TOPICS)
            print(f"IR model {ir_model} || MRR@{k} = {mrr}")
            print(f"IR model {ir_model} || TOPK@{k} = {topk}\n")
            print("\n")
