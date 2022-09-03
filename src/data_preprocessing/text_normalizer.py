"""
Module for data preprocessing
"""

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer

LANGUAGE = 'english'
MAX_VALID_CHARS = 3


def get_tokens(input_text):
    """
    :param input_text:
    :return:
    """
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    tokens = [token for token in tokenizer.tokenize(input_text) if len(token) > MAX_VALID_CHARS]
    return tokens


def remove_stopwords(input_tokens):
    """
    :param input_tokens:
    :return:
    """
    stop_words = set(stopwords.words(LANGUAGE))
    filtered_tokens = [word for word in input_tokens if word.lower() not in stop_words]
    return filtered_tokens


def lemmatize(input_tokens):
    """
    :param input_tokens:
    :return:
    """
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in input_tokens]
    return lemmatized_tokens


def stem_tokens(input_tokens):
    """
    :param input_tokens:
    :return:
    """
    stemmer = SnowballStemmer("english")
    stemmed_tokens = [stemmer.stem(token) for token in input_tokens]
    words = [w for w in stemmed_tokens if str(w).isalpha()]
    return words


def normalize_data(raw_text):
    """
    :param raw_text:
    :return:
    """
    # get tokens from raw text
    tokens = get_tokens(raw_text)
    # remove stopwords
    tokens = remove_stopwords(tokens)
    # lemmatize
    tokens = lemmatize(tokens)
    # stemming
    tokens = stem_tokens(tokens)
    # remove duplicate
    tokens = set(tokens)
    return " ".join(tokens)
