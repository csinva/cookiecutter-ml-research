This is an evolving repo optimized for machine-learning projects aimed at designing a new algorithm. They require sweeping over different hyperparameters, comparing to baselines, and iteratively refining an algorithm.

# Organization
- `project_name`: to be renamed, contains main code for modeling (e.g. model architecture)
- `experiments`: contains code for runnning experiments (e.g. loading data, training models, evaluating models)
- `scripts`: contains scripts for running experiments (e.g. python scripts that launch jobs in `experiments` folder with different hyperparams)
- `notebooks`: contains jupyter notebooks for analyzing results, errors, and making figures

# Setup
- clone and run `pip install -e .`, resulting in a package named `project_name` that can be imported
    - first, rename `project_name` to your project name and modify `setup.py` accordingly
- example run: run `python scripts/01_train_models.py` then load the results in `notebooks/01_model_results.ipynb`

# Features
- scripts sweep over hyperparameters using easy-to-specify python code
- experiments automatically cache runs that have already completed
    - caching uses the (**non-default**) arguments in the argparse namespace
- notebooks can easily evaluate results aggregated over multiple experiments using pandas
- binary arguments should start with the word "use" (e.g. `--use_caching`) and take values 0 or 1

# Guidelines
- Huggingface whenever possible, then pytorch
- See some useful packages [here](https://csinva.io/blog/misc/ml_coding_tips)
- Avoid notebooks whenever possible (ideally, only for analyzing results, making figures)
- Paths should be specified relative to a file's location (e.g. `os.path.join(os.path.dirname(__file__), 'data')`)
- Use logging instead of print
- Use argparse and sweep over hyperparams using python scripts (or [amulet](https://amulet-docs.azurewebsites.net/main/index.html))
- Each run should save a single pickle file of its results
- Everything should run end-to-end with one script (caching things along the way)
- Keep an updated requirements.txt (required for amulet)
- Follow sklearn apis whenever possible