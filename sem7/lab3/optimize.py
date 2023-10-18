import optuna
from optuna_dashboard import run_server
from model import Model
import numpy as np


def objective(trial):
    params = [None]*22
    for i in range(22):
        new = trial.suggest_float(f"p{i}", 0, 10)
        params[i] = (new, 10-new)
    model = Model(params)
    res = model.simulate_one()
    return res[1][-1]

storage = optuna.storages.InMemoryStorage()
study = optuna.create_study(storage=storage, study_name="TPE of model optimize", direction="maximize", sampler=optuna.samplers.TPESampler())
study.optimize(objective, n_trials=200, n_jobs=3)

run_server(storage)