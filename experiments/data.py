import datasets
import os
from os.path import join as oj
from tqdm import tqdm
import pandas as pd
import pickle as pkl
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

def load_dataset(dataset_name, test_size=0.33, subsample_frac=1.0):
    """Load dataset + return the relevant dataset key
    """
    # load dset
    if dataset_name == 'tweet_eval':
        dset = datasets.load_dataset('tweet_eval', 'hate')
    elif dataset_name == 'financial_phrasebank':
        train = datasets.load_dataset('financial_phrasebank', 'sentences_75agree',
                                      revision='main', split='train')
        idxs_train, idxs_val = train_test_split(
            np.arange(len(train)), test_size=test_size, random_state=13)
        dset = datasets.DatasetDict()
        dset['train'] = train.select(idxs_train)
        dset['validation'] = train.select(idxs_val)
    else:
        dset = datasets.load_dataset(dataset_name)

    # process dset
    dataset_key_text = 'text'
    if dataset_name == 'sst2':
        dataset_key_text = 'sentence'
    elif dataset_name == 'financial_phrasebank':
        dataset_key_text = 'sentence'
    elif dataset_name == 'imdb':
        del dset['unsupervised']
        dset['validation'] = dset['test']

    # delete test dset
    if 'test' in dset:
        del dset['test']

    # subsample data
    if subsample_frac > 0:
        dset['train'] = dset['train'].select(range(int(subsample_frac * len(dset['train']))))
    return dset, dataset_key_text

def convert_text_data_to_counts_array(dset, dataset_key_text):
    v = CountVectorizer()
    X_train = v.fit_transform(dset['train'][dataset_key_text])
    y_train = dset['train']['label']
    X_test = v.transform(dset['validation'][dataset_key_text])
    y_test = dset['validation']['label']
    feature_names = v.get_feature_names_out().tolist()
    return X_train, y_train, X_test, y_test, feature_names