import optuna
from optuna_dashboard import run_server
from model_sig import Model
import numpy as np


def objective(trial):
    params = [None]*29
    for i in range(len(params)):
        new1 = trial.suggest_categorical(f"p1_{i}", [True, False])
        new2 = trial.suggest_categorical(f"p2_{i}", [True, False])
        params[i] = (new1, new2)
    model = Model(params)
    res = model.simulate_one()
    return res[1][-1]

storage = optuna.storages.InMemoryStorage()
study = optuna.create_study(storage=storage, study_name="TPE of model optimize", direction="maximize", sampler=optuna.samplers.TPESampler())
study.optimize(objective, n_trials=200, n_jobs=3)

run_server(storage)