from runner import evaluation

COMMAND = 'node data/bundle.js'
NUM = 12

def objective_origin(trial):
    params = {
        'depthContrbRandom': trial.suggest_uniform('depthContrbRandom', -2.0, 2.0),
        'randomCoef': 0.5,
        'capCoef': trial.suggest_uniform('capCoef', 0.0, 5.0),
        'highBlueCoef': trial.suggest_uniform('highBlueCoef', 0.0, 5.0)
    }
    param_str = ','.join([f'{k}={v}' for k, v in params.items()])
    command = COMMAND + ' -d 20 -s ' + param_str
    return NUM / (evaluation(command, NUM, 'optuna', param_str) + 1)
