import argparse
from copy import deepcopy
import logging
import random
from collections import defaultdict
from os.path import join
import numpy as np
import torch
import pickle as pkl

from project_name.model import DecisionTreeClassifier
import cache_save_utils
import data


def fit_model(model, X_train, y_train, X_test, y_test, feature_names, r):
    model.fit(X_train, y_train)

    evaluate_model(model, X_test, y_test, r)

    return r

def evaluate_model(model, X_test, y_test, r):
    r['test_acc'] = model.score(X_test, y_test)
    return r

if __name__ == '__main__':
    # initialize args
    def add_main_args(parser):
        """Caching uses the non-default values from argparse to name the saving directory.
        Changing the default arg an argument will break cache compatibility with previous runs.
        """

        # dataset args
        parser.add_argument('--dataset_name', type=str,
                            default='rotten_tomatoes', help='name of dataset')
        parser.add_argument('--subsample_frac', type=float,
                            default=1, help='fraction of samples to use')

        # training misc args
        parser.add_argument('--seed', type=int, default=1,
                            help='random seed')
        parser.add_argument('--save_dir', type=str, default='tmp',
                            help='directory for saving')
        return parser

    def add_computational_args(parser):
        """Arguments that only affect computation and not the results (shouldnt use when checking cache)
        """
        parser.add_argument('--use_cache', type=int, default=1, choices=[0, 1],
                            help='whether to check for cache')
        return parser

    # get args
    parser = argparse.ArgumentParser()
    parser_without_computational_args = add_main_args(parser)
    parser = add_computational_args(
        deepcopy(parser_without_computational_args))
    args = parser.parse_args()

    # set up logging
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO)
    for k in sorted(vars(args)):
        logger.info('\t' + k + ' ' + str(vars(args)[k]))

    # set up saving directory
    already_cached, save_dir = cache_save_utils.get_save_dir_unique(
        parser, parser_without_computational_args, args, args.save_dir)
    logging.info(f'\n\nsaving to ' + save_dir)
    if args.use_cache and already_cached:
        logging.info(
            f'cached version exists!\nsuccessfully skipping :)\n\n\n')
        exit(0)

    # set seed
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    random.seed(args.seed)

    # load data
    dset, dataset_key_text = data.load_dataset(
        dataset_name=args.dataset_name, subsample_frac=args.subsample_frac)
    X_train, y_train, X_test, y_test, feature_names = data.convert_text_data_to_counts_array(dset, dataset_key_text)

    # load model
    model = DecisionTreeClassifier()

    # set up saving
    r = defaultdict(list)
    r.update(vars(args))
    cache_save_utils.save_json(
        args=args, save_dir=save_dir, fname='params.json', r=r)

    # train
    r = fit_model(model, X_train, y_train, X_test, y_test, feature_names, r)

    # save results
    pkl.dump(r, open(join(save_dir, 'results.pkl'), 'wb'))
    logging.info('Succesfully completed :)\n\n')
