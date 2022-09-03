"""
Runner for normalizing raw data of eclipse and mozilla
"""

from data_preprocessing.driver import run

if __name__ == "__main__":
    # eclipse
    PROJECT_NAME = "eclipse"
    run(PROJECT_NAME)

    # mozilla firefox
    PROJECT_NAME = "mozilla"
    run(PROJECT_NAME)
