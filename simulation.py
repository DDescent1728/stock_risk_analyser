import math
import random
import numpy as np


# 1. Log Returns

def compute_log_returns(prices):
    """
    Compute daily log returns from a list of historical prices.
    prices: list of floats [P0, P1, ..., PN]
    returns: list of log returns
    """
    log_returns = []
    for i in range(1, len(prices)):
        if prices[i-1] <= 0 or prices[i] <= 0:
            # prevent log of zero or negative
            continue
        r = math.log(prices[i] / prices[i-1])
        log_returns.append(r)
    return log_returns


# 2. Compute mu and sigma

def compute_mu_sigma(log_returns):
    """
    Compute mean (mu) and standard deviation (sigma) of log returns.
    """
    mu = np.mean(log_returns)
    sigma = np.std(log_returns, ddof=1) # sample standard deviation
    return mu, sigma


# 3. GBM Monte Carlo Simulation

def run_gbm_simulation(S0, mu, sigma, days, n_paths):
    """
    Run GBM Monte Carlo simulation.
    S0: initial stock price (float)
    mu: drift (mean log return)
    sigma: volatility (std dev of log returns)
    days: number of future days to simulate
    n_paths: number of simulation paths
    Returns: list of lists, each inner list = simulated path of prices
    """
    delta_t = 1/252 # assuming daily steps, 252 trading days in a year
    simulation_paths = []

    for path in range(n_paths):
        prices = [S0]
        for day in range(1, days+1):
            Z = random.gauss(0, 1) # standard normal
            St = prices[-1] * math.exp((mu - 0.5 * sigma**2) * delta_t + sigma * math.sqrt(delta_t) * Z)
            prices.append(St)
        simulation_paths.append(prices)

    return simulation_paths


# 4. Risk Metrics

def compute_risk_metrics(simulation_paths):
    """
    Compute risk metrics from simulation paths.
    Returns a dictionary with expected price, worst-case price, and 95% VaR.
    """
    # Taking last price of each path
    final_prices = [path[-1] for path in simulation_paths]

    expected_price = np.mean(final_prices)
    worst_case = min(final_prices)
    var_95 = np.percentile(final_prices, 5) # 5th percentile = 95% confidence VaR

    return {
        'expected_price': expected_price,
        'worst_case': worst_case,
        'var_95': var_95
    }
