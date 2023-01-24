import os
from os.path import dirname

def test_small_pipeline():
    repo_dir = dirname(dirname(os.path.abspath(__file__)))
    exit_value=os.system('python ' + os.path.join(repo_dir, 'experiments', '01_train_model.py --use_cache 0 --subsample_frac 0.1'))
    assert exit_value == 0, 'default pipeline passed'

if __name__ == '__main__':
    test_small_pipeline()