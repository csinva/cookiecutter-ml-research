import submit_utils

# List of values to sweep over (sweeps over all combinations of these)
params_shared_dict = {
    'seed': [1, 2],
    'save_dir': ['tmp'],
    'lr': [0.1, 0.01],
}

# List of tuples to sweep over (these values are coupled, and swept over together)
params_coupled_dict = {
    ('model_name', 'alpha'): [
        ('ridge', 0.1),
        ('ridge', 1),
    ],
    ('model_name', 'max_depth'): [
        ('decision_tree', i)
        for i in range(1, 4)
    ],
}
# print(params_coupled_dict.keys())

# FREEZE PARAMS 
# (x, xvalue)....

# IMPOSSIBLE PAIRINGS...

# If you want to couple long things, you would need to duplicate and modify this script
# (e.g. decision trees and linear models have very different params, so each would have a separate script)

submit_utils.run_dicts(
    params_shared_dict,
    params_coupled_dict,
    script_name='03_train_prefix.py',
    actually_run=False
)
