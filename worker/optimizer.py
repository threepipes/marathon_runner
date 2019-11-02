import time
import optuna
from objective_hatetris import objective_origin


def optimize():
    study = optuna.create_study()
    study.optimize(objective_origin, n_trials=100)


if __name__ == '__main__':
    optimize()
