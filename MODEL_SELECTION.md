# Model selection

Fill this in after you have trained your candidates in MLflow. Short sentences are fine. Use numbers from your runs.

## The question
What does this model decide, and who is hurt by a wrong answer? This model predicts whether a telecom customer is likely to churn (cancel their subscription). A false negative hurts the business by missing an at-risk customer who leaves without intervention, while a false positive wastes retention incentives on a loyal customer and risks unnecessary outreach.

## Candidates
| Candidate | Why I tried it | AUC | F1 | F1 per slice (lowest) | p95 latency (ms) | Size (KB) | MLflow run ID |
|---|---|---|---|---|---|---|---|
| logreg | Fast, lightweight linear baseline with high interpretability and minimal inference overhead. | 0.798 | 0.495 | 0.25 | 3.13 | 3.5 | d7a97045c3b045db9a1cb314c9fdc36f |
| random_forest | Tree-based ensemble (`max_depth=10`) to capture non-linear feature interactions while controlling overfitting. | 0.738 | 0.412 | 0.20 | 6.06 | 2368 | 5af7bf630bca4e6e8889995d91f3739d |
| gradient_boosting | Sequential boosted trees (`learning_rate=0.1`) to test if iterative error correction improves minority-class recall. | 0.748 | 0.417 | 0.2222 | 4.86 | 142 |c435d13b3e04493a8b33661bad84d73d |

## The champion
I picked **logreg** (d7a97045c3b045db9a1cb314c9fdc36f) as the champion model. It achieved the highest overall F1 (0.495) and AUC (0.798), the best worst-slice F1 (0.25), the lowest p95 latency (3.1 ms), and the smallest size (3.5 KB, compared to 2368 KB for Random Forest and 142 KB for Gradient Boosting).

What I accepted losing: logreg is weaker on one-year contracts (0.25 vs 0.4444 for gradient boosting) and on two-year contracts (0.25 vs 0.3636 for random forest). These slices have very few positive samples, so these numbers are noisy. I accepted this because overall F1, AUC, worst-slice F1, latency and size all favour logreg.

## My promotion rules
- Latency budget (p95): **15.0** ms, because our champion runs at 3.1 ms locally, and a 15 ms cap leaves a safe margin for slower GitHub Actions CI runners while stopping heavy, slow models from reaching production.
- Minimum gain to replace the champion (F1 points): **0.01**, because a gain smaller than this may just be noise on a small test set, so a new model must beat the stable, lightweight 3.5 KB champion by at least this much.

## What I would check next
Data drift in customer contract types or billing plans over time. If new promotional plans or shifting user behavior alter feature distributions after deployment, a linear model (`logreg`) cannot automatically adapt to emerging non-linear churn patterns without scheduled retraining and slice-level monitoring.