import argparse
from copy import deepcopy
import logging
import random
from collections import defaultdict
from os.path import join
import numpy as np
import torch
import pickle as pkl

import project_name.model
import cache_save_utils
import data


def fit_model(model, X_train, X_cv, X_test, y_train, y_cv, y_test, feature_names, r):
    model.fit(X_train, y_train)
    r['acc_cv'] = model.score(X_cv, y_cv)
    evaluate_model(model, X_test, y_test, r)
    return r

def evaluate_model(model, X_test, y_test, r):
    r['acc_test'] = model.score(X_test, y_test)
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
        parser.add_argument('--save_dir', type=str, default='results',
                            help='directory for saving')

        # model args
        parser.add_argument('--model_name', type=str, choices=['decision_tree', 'ridge'],
                            default='decision_tree', help='name of model')
        parser.add_argument('--alpha', type=float, default=1,
                            help='regularization strength')
        parser.add_argument('--max_depth', type=int,
                            default=2, help='max depth of tree')
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

    # set up saving directory + check for cache
    already_cached, save_dir = cache_save_utils.get_save_dir_unique(
        parser, parser_without_computational_args, args, args.save_dir)
    
    if args.use_cache and already_cached:
        logging.info(
            f'cached version exists! Successfully skipping :)\n\n\n')
        exit(0)
    for k in sorted(vars(args)):
        logger.info('\t' + k + ' ' + str(vars(args)[k]))
    logging.info(f'\n\nsaving to ' + save_dir)

    # set seed
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    random.seed(args.seed)

    # load data
    dset, dataset_key_text = data.load_huggingface_dataset(
        dataset_name=args.dataset_name, subsample_frac=args.subsample_frac)
    X_train, X_cv, X_test, y_train, y_cv, y_test, feature_names = data.convert_text_data_to_counts_array(
        dset, dataset_key_text)

    # load model
    model = project_name.model.get_model(args)

    # set up saving dictionary + save params file
    r = defaultdict(list)
    r.update(vars(args))
    cache_save_utils.save_json(
        args=args, save_dir=save_dir, fname='params.json', r=r)

    # fit
    r = fit_model(model, X_train, X_cv, X_test, y_train, y_cv, y_test, feature_names, r)

    # save results
    pkl.dump(r, open(join(save_dir, 'results.pkl'), 'wb'))
    logging.info('Succesfully completed :)\n\n')
