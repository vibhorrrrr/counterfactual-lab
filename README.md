# Counterfactual Lab

Most data science projects focus on prediction.
Most real decisions require knowing what would have happened otherwise.

This project estimates the **causal impact of an intervention** using
Difference-in-Differences on panel data.

## Question
What was the effect of an intervention, compared to the counterfactual
scenario where it never occurred?

## Method
- Difference-in-Differences
- Parallel trends validation
- Bootstrap confidence intervals

## Result
Estimated causal impact: +4.84  
95% confidence interval: [3.76, 5.94]

## Key Assumption
Parallel trends between treatment and control groups prior to intervention.

## Limitations
- Sensitive to violations of parallel trends
- Assumes no spillover effects
- Single intervention setting

## Why this matters
Correlation answers "what happened".
Counterfactual analysis answers "what changed because of us".
