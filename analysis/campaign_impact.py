import os
import sys

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.diff_in_diff import diff_in_diff, bootstrap_ci

# ------------------------
# Load data
# ------------------------
df = pd.read_csv("data/simulated_campaign.csv")

# ------------------------
# Parallel trends check
# ------------------------
pre = df[df.post == 0]
pre_means = pre.groupby(["time", "group"]).outcome.mean().unstack()

plt.figure(figsize=(8,4))
plt.plot(pre_means.index, pre_means["control"], label="Control")
plt.plot(pre_means.index, pre_means["treatment"], label="Treatment")
plt.title("Parallel Trends Check (Pre-Intervention)")
plt.xlabel("Time")
plt.ylabel("Outcome")
plt.legend()
plt.show()

# ------------------------
# Difference-in-Differences
# ------------------------
results = diff_in_diff(df)
ci_low, ci_high = bootstrap_ci(df)

print("Difference-in-Differences Results")
print("---------------------------------")
print(f"Causal Impact Estimate: {results['did_estimate']:.2f}")
print(f"95% CI: [{ci_low:.2f}, {ci_high:.2f}]")

# ------------------------
# Observed vs Counterfactual
# ------------------------
means = df.groupby(["time", "group"]).outcome.mean().reset_index()

control = means[means.group == "control"]
treatment = means[means.group == "treatment"]

counterfactual = (
    control.outcome.values
    + (results["treated_pre"] - results["control_pre"])
)

plt.figure(figsize=(9,5))
plt.plot(treatment.time, treatment.outcome, label="Observed (Treatment)")
plt.plot(treatment.time, counterfactual, linestyle="--", label="Counterfactual (No Intervention)")
plt.axvline(x=12, color="black", linestyle=":", label="Intervention")

plt.fill_between(
    treatment.time,
    counterfactual - (results["did_estimate"] - ci_low),
    counterfactual + (ci_high - results["did_estimate"]),
    alpha=0.2,
    label="95% CI"
)

plt.title("Observed vs Counterfactual Outcome")
plt.xlabel("Time")
plt.ylabel("Outcome")
plt.legend()
plt.tight_layout()
plt.savefig("figures/counterfactual.png", dpi=200)
plt.show()

