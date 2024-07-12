import numpy as np
import pandas as pd
from random import gauss
from itertools import product
from tqdm import tqdm
import statsmodels.api as sm
from numba import njit, prange

@njit
def simulate_single_run(phi, forecast, sigma, seed, rPT, rSLm, maxHP):
    p, hp = seed, 0
    while True:
        p = (1 - phi) * forecast + phi * p + sigma * np.random.normal()
        cP = p - seed
        hp += 1
        if cP > rPT or cP < -rSLm or hp > maxHP:
            return cP

@njit(parallel=True)
def synthetic_simulation(phi, forecast, sigma, nIter, maxHP, rPT, rSLm, seed):
    output = np.zeros((len(rPT), len(rSLm), 5))
    for i in prange(len(rPT)):
        for j in prange(len(rSLm)):
            results = np.zeros(nIter)
            for k in range(nIter):
                results[k] = simulate_single_run(phi, forecast, sigma, seed, rPT[i], rSLm[j], maxHP)
            mean = np.mean(results)
            std = np.std(results)
            output[i, j] = np.array([rPT[i], rSLm[j], mean, std, mean / std])
    return output

def get_sharpe_grid(output, profit_taking_range, stop_loss_range):
    sharpe = output[:, :, 4]
    sharpe_test = pd.DataFrame(
        sharpe,
        index=profit_taking_range,
        columns=stop_loss_range
    )
    sharpe_test = sharpe_test.T
    sharpe_test.sort_index(ascending=False, inplace=True)
    return sharpe_test

def get_OU_params(close: pd.Series) -> dict:
    mean = np.log(close).mean()
    price_lagged = np.log(close).shift(1)
    excess_price = price_lagged - mean

    X = sm.add_constant(excess_price.iloc[1:])
    y = np.log(close).iloc[1:]

    ols = sm.OLS(y, X).fit()

    phi = ols.params.iloc[1]
    sigma = np.std(ols.resid)
    half_life = -(np.log(2) / np.log(phi))
    forecast = ols.params.iloc[0]

    return {'forecast': forecast, 'phi': phi, 'sigma': sigma, 'half life': half_life}