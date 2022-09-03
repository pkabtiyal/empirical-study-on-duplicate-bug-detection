"""
Creation of topic model and probability distributions
"""

import os
import sys
import pickle
import gensim
import pandas as pd
from gensim.corpora import Dictionary
from util.constants import REPORT, ISSUE_ID
from util.common import check_to_create_dir, get_testids


def create_topics_and_dist(docs, project_name, num_topics):
    """
    create topic model and convert corpus to topic distribution
    :param num_topics:
    :param project_name:
    :param docs:
    :return:
    """

    model_location = f"../ldamodel/{project_name}-{num_topics}-ldamallet.pkl"
    ids_for_test = get_testids(project_name)
    print(ids_for_test)
    training_docs = docs[~docs[ISSUE_ID].isin(ids_for_test)]

    tokenized_bugs = [str(x).split(' ') for x in training_docs[REPORT]]
    dictionary = Dictionary()
    corpus_bow = [dictionary.doc2bow(doc, allow_update=True) for doc in tokenized_bugs]
    print(len(corpus_bow))

    if not os.path.isfile(model_location):

        # topic model creation
        mallet_abs_path = os.path.abspath("/opt/homebrew/Cellar/mallet/2.0.8_1")
        mallet_abs_path = mallet_abs_path.replace(" ", r"\ ")
        print(f'mallet_abs_path= {mallet_abs_path}')
        mallet_path = f'{mallet_abs_path}/bin/mallet'
        model = gensim.models.wrappers.LdaMallet(
            mallet_path, corpus=corpus_bow, num_topics=num_topics, id2word=Dictionary(tokenized_bugs)
        )

        # saving the model for later use
        check_to_create_dir(model_location)
        pickle.dump(model, open(model_location, "wb"))
    else:
        model = pickle.load(open(model_location, "rb"))

    # create topic distribution file
    df = pd.DataFrame(columns=['issue_id', 'distribution'])
    norm_df = pd.read_csv(f'../data/normalized/{project_name}-norm-data.csv')
    ind_to_issueid = dict(zip(norm_df.index, norm_df[ISSUE_ID]))
    file_name = f"../ldamodel/{project_name}-dist-{num_topics}.csv"
    ind = 0
    all_topic_dist = model[corpus_bow]
    for dists in all_topic_dist:
        doc_dist = [str(topic_dist[1]) for topic_dist in dists]
        dist_content = " ".join(doc_dist)
        issue_id = ind_to_issueid[ind]
        df.loc[ind] = [str(issue_id)] + [dist_content]
        ind += 1

    print(f"saving probability distributions to {file_name}.....")
    df.to_csv(file_name)


def get_model(project_name, num_topics):
    """
    :param project_name:
    :param num_topics:
    :return:
    """
    model_location = f"../ldamodel/{project_name}-{num_topics}-ldamallet.pkl"
    if os.path.isfile(model_location):
        model = pickle.load(open(model_location, "rb"))
        return model

    print(f"Model for project {project_name} does not exit. Aborting...")
    sys.exit(1)


def run(project_name, num_topics):
    """
    :param project_name:
    :param num_topics:
    :return:
    """
    input_file_path = f"../data/normalized/{project_name}-norm-data.csv"
    if os.path.exists(input_file_path.rsplit("/", 1)[0]):
        docs = pd.read_csv(input_file_path)
        create_topics_and_dist(docs, project_name, num_topics)
    else:
        print(f'Invalid file path : {input_file_path}')
        print('Aborting...')
        sys.exit(1)
