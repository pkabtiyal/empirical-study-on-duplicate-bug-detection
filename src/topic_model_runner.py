"""
runner for topic modelling
"""

from topic_model.modelling import run

if __name__ == "__main__":

    PROJECT_NAME = "eclipse"
    for num_topics in [20, 50, 80, 100, 120, 140]:
        run(PROJECT_NAME, num_topics)

    PROJECT_NAME = "mozilla"
    for num_topics in [20, 50, 80, 100, 120, 140]:
        run(PROJECT_NAME, num_topics)
