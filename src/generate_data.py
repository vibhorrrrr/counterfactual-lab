import numpy as np
import pandas as pd

np.random.seed(42)

# Parameters
n_units = 50            # entities per group
n_periods = 24          # months
intervention_time = 12 # month index where intervention happens
effect_size = 5.0      # true causal effect

data = []

for group in ["control", "treatment"]:
    for unit in range(n_units):
        baseline = np.random.normal(50, 5)
        trend = np.random.normal(1.0, 0.1)

        for t in range(n_periods):
            value = baseline + trend * t + np.random.normal(0, 2)

            # Apply intervention only to treatment group after time
            if group == "treatment" and t >= intervention_time:
                value += effect_size

            data.append({
                "unit": f"{group}_{unit}",
                "group": group,
                "time": t,
                "outcome": value,
                "post": int(t >= intervention_time),
                "treated": int(group == "treatment")
            })

df = pd.DataFrame(data)
df.to_csv("data/simulated_campaign.csv", index=False)

print("Dataset saved to data/simulated_campaign.csv")
