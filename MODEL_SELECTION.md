# Model selection

Fill this in after you have trained your candidates in MLflow. Short sentences are fine. Use numbers from your runs.

## The question
What does this model decide, and who is hurt by a wrong answer? This model predicts whether a telecom customer is likely to churn (cancel their subscription). A false negative hurts the business by missing an at-risk customer who leaves without intervention, while a false positive wastes retention incentives on a loyal customer and risks unnecessary outreach.

## Candidates
| Candidate | Why I tried it | AUC | F1 | F1 per slice (lowest) | p95 latency (ms) | Size (KB) | MLflow run ID |
|---|---|---|---|---|---|---|---|
| logreg | Fast, lightweight linear baseline with high interpretability and minimal inference overhead. | 0.798 | 0.495 | [.25] | 4.0 | 4 | 03774b75439b4fb2b5a51d32289b28ff |
| random_forest | Tree-based ensemble (`max_depth=10`) to capture non-linear feature interactions while controlling overfitting. | 0.738 | 0.412 | [.2] | 8.7 | 2368 | 3a57ffcec4994fb988f18e361fdb397b |
| gradient_boosting | Sequential boosted trees (`learning_rate=0.1`) to test if iterative error correction improves minority-class recall. | 0.748 | 0.417 | [.2222] | 4.4 | 142 | 3f7eb560c6a9402392c13fbcaa6693cc |

## The champion
I picked **`logreg`** (`03774b75439b4fb2b5a51d32289b28ff`) as the champion model. It outperformed both tree-based candidates across every operational and predictive metric: it achieved the highest overall **F1 (0.495)** and **AUC (0.798)**, the lowest **p95 latency (4.0 ms)**, and an ultra-compact footprint of **4 KB** (compared to 2368 KB for Random Forest and 142 KB for Gradient Boosting).

## My promotion rules
- Latency budget (p95): **15.0** ms, because **our champion runs at 4.0 ms locally, and setting a 15.0 ms cap guarantees real-time API responsiveness while providing a safe margin for slower GitHub Actions CI runners without letting heavy, slow models slip into production.**
- Minimum gain to replace the champion (F1 points): **0.01**, because **replacing a stable, lightweight 4 KB production model requires a statistically meaningful improvement in predictive accuracy rather than random variance or minor noise across runs.**

## What I would check next
 Data drift in customer contract types or billing plans over time—if new promotional plans or shifting user behavior alter feature distributions after deployment, a linear model (`logreg`) cannot automatically adapt to emerging non-linear churn patterns without scheduled retraining and slice-level monitoring.
