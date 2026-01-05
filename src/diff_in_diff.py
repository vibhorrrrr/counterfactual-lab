import pandas as pd
import numpy as np

def diff_in_diff(df):
    """
    Computes Difference-in-Differences estimate.
    """

    # Group means
    treated_pre = df[(df.treated == 1) & (df.post == 0)].outcome.mean()
    treated_post = df[(df.treated == 1) & (df.post == 1)].outcome.mean()

    control_pre = df[(df.treated == 0) & (df.post == 0)].outcome.mean()
    control_post = df[(df.treated == 0) & (df.post == 1)].outcome.mean()

    did_estimate = (treated_post - treated_pre) - (control_post - control_pre)

    return {
        "treated_pre": treated_pre,
        "treated_post": treated_post,
        "control_pre": control_pre,
        "control_post": control_post,
        "did_estimate": did_estimate
    }

def bootstrap_ci(df, n_bootstrap=1000, alpha=0.05):
    estimates = []

    for _ in range(n_bootstrap):
        sample = df.sample(frac=1, replace=True)
        estimates.append(diff_in_diff(sample)["did_estimate"])

    lower = np.percentile(estimates, 100 * alpha / 2)
    upper = np.percentile(estimates, 100 * (1 - alpha / 2))

    return lower, upper
