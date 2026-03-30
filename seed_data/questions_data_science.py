"""
Data Science / ML interview questions for PlaceRight.
~300 questions across 11 topics, conversational style.
"""

from typing import List, Dict


def _q(topic: str, difficulty: str, text: str, follow_ups: List[str],
       points: List[str], company: str = "", tags: List[str] = None) -> Dict:
    rubric = {
        "1-3": "Cannot explain the concept. Gives textbook definition without understanding.",
        "4-5": "Partial understanding. Knows the term but cannot apply or explain trade-offs.",
        "6-7": "Good explanation with practical awareness. Can discuss when to use and basic trade-offs.",
        "8-10": "Excellent depth. Explains intuition, math where needed, real-world trade-offs, and edge cases.",
    }
    return {
        "domain": "data_science",
        "topic": topic,
        "difficulty": difficulty,
        "level": "fresher",
        "question_text": text,
        "follow_ups": follow_ups,
        "expected_points": points,
        "scoring_rubric": rubric,
        "company_specific": company,
        "tags": tags or [topic],
    }


def get_data_science_questions() -> List[Dict]:
    Q: List[Dict] = []

    # ==================================================================
    # STATISTICS & PROBABILITY (50)
    # ==================================================================

    _sp = "statistics_probability"

    Q.append(_q(_sp, "easy",
        "Explain Bayes' theorem to me as if I'm a product manager who has never taken a stats course.",
        ["Can you walk me through a real-world example?", "How would you use it in a spam filter?"],
        ["Prior probability", "Likelihood", "Posterior", "Normalization constant", "Intuitive example"]))

    Q.append(_q(_sp, "easy",
        "What is the difference between population and sample? Why does it matter in data science?",
        ["When would using population data be impractical?", "How does sample size affect your confidence?"],
        ["Population vs sample definition", "Sampling bias", "Representativeness", "Central limit theorem mention"]))

    Q.append(_q(_sp, "easy",
        "If I flip a fair coin 10 times and get 10 heads, what is the probability the next flip is heads?",
        ["What if I told you I suspect the coin is biased?", "How would you test for bias statistically?"],
        ["Independence of events", "Gambler's fallacy", "Bayesian update for bias", "Hypothesis testing approach"]))

    Q.append(_q(_sp, "medium",
        "Walk me through what a p-value actually means. I've seen people misinterpret it -- how would you explain it correctly?",
        ["What's wrong with saying 'the probability the null hypothesis is true'?", "What p-value threshold would you use and why?"],
        ["Correct definition", "Common misinterpretations", "Significance level choice", "Multiple testing problem"]))

    Q.append(_q(_sp, "medium",
        "You ran an A/B test and got a p-value of 0.04. Your manager says 'ship it'. What questions would you ask before agreeing?",
        ["What if the sample size was only 50 per group?", "How would you check for practical significance vs statistical significance?"],
        ["Effect size", "Sample size adequacy", "Practical significance", "Multiple comparisons", "Business impact"],
        company="Flipkart", tags=[_sp, "ab_testing"]))

    Q.append(_q(_sp, "easy",
        "What is a confidence interval? If I have a 95% CI of [2.1, 4.3], what does that actually tell me?",
        ["Does it mean there's a 95% chance the true value is in that range?", "How does sample size affect CI width?"],
        ["Frequentist interpretation", "Not probability of parameter", "Repeated sampling interpretation", "Width vs precision"]))

    Q.append(_q(_sp, "medium",
        "Explain the Central Limit Theorem. Why is it considered one of the most important results in statistics?",
        ["Does it work for any distribution?", "What's the minimum sample size you'd want?"],
        ["Sampling distribution of mean", "Approaches normal", "n >= 30 rule of thumb", "Enables hypothesis testing"]))

    Q.append(_q(_sp, "easy",
        "What's the difference between Type I and Type II errors? Give me a real-world example where each one is more dangerous.",
        ["In a cancer screening test, which error is worse?", "How do you control for each type?"],
        ["False positive vs false negative", "Alpha and beta", "Trade-off", "Context-dependent severity"]))

    Q.append(_q(_sp, "medium",
        "You're designing an A/B test for a new checkout flow. How would you decide the sample size needed?",
        ["What if you can only run the test for 2 weeks?", "How do you handle multiple metrics?"],
        ["Power analysis", "Effect size estimation", "Alpha and power levels", "Minimum detectable effect"],
        company="Amazon", tags=[_sp, "ab_testing"]))

    Q.append(_q(_sp, "medium",
        "Explain the difference between Gaussian, Poisson, and Binomial distributions. When would you use each?",
        ["Give me a real dataset example for each.", "What happens when n is large in binomial?"],
        ["Continuous vs discrete", "Use cases for each", "Parameter meanings", "Convergence relationships"]))

    Q.append(_q(_sp, "hard",
        "What is the law of large numbers and how does it differ from the Central Limit Theorem?",
        ["Can you give a practical example where LLN matters in ML?", "How does this relate to Monte Carlo methods?"],
        ["Convergence of sample mean", "LLN about mean convergence", "CLT about distribution shape", "Practical implications"]))

    Q.append(_q(_sp, "easy",
        "What is correlation? Does correlation imply causation? Give me a funny example of spurious correlation.",
        ["How would you establish causation then?", "What's the difference between Pearson and Spearman correlation?"],
        ["Linear relationship measure", "Causation requires experiment", "Confounders", "Correlation types"]))

    Q.append(_q(_sp, "medium",
        "Explain what statistical power is. If your A/B test has low power, what happens?",
        ["How would you increase power without increasing sample size?", "What's a typical power target?"],
        ["Probability of detecting true effect", "80% standard", "Factors affecting power", "Consequences of low power"]))

    Q.append(_q(_sp, "hard",
        "You have a dataset where the variance of one feature is 1000x larger than another. Why is this a problem and how do you fix it?",
        ["Which ML algorithms are affected by this?", "What scaling method would you choose and why?"],
        ["Scale dominance", "Standardization vs normalization", "Algorithm sensitivity", "Feature importance distortion"]))

    Q.append(_q(_sp, "medium",
        "What is the difference between parametric and non-parametric tests? When would you prefer one over the other?",
        ["Give me examples of each.", "What if your data is ordinal?"],
        ["Distributional assumptions", "t-test vs Mann-Whitney", "Sample size considerations", "Robustness"]))

    Q.append(_q(_sp, "easy",
        "Explain mean, median, and mode. When is median better than mean?",
        ["What about for income data in India?", "What's a trimmed mean?"],
        ["Central tendency measures", "Sensitivity to outliers", "Skewed distributions", "Use case examples"]))

    Q.append(_q(_sp, "medium",
        "What is a probability distribution function vs a cumulative distribution function? Draw the relationship.",
        ["How do you go from PDF to CDF?", "What does the area under the PDF represent?"],
        ["PDF gives density", "CDF gives cumulative probability", "Integration relationship", "Properties of each"]))

    Q.append(_q(_sp, "hard",
        "Explain Maximum Likelihood Estimation. How would you use it to estimate the parameters of a normal distribution?",
        ["What's the difference between MLE and MAP?", "When does MLE fail?"],
        ["Likelihood function", "Log-likelihood", "Optimization", "Overfitting risk", "Bayesian alternative"],
        company="Goldman Sachs", tags=[_sp, "estimation"]))

    Q.append(_q(_sp, "medium",
        "What is the chi-squared test? When would you use it in a data science project?",
        ["Can you use it for continuous variables?", "What are the assumptions?"],
        ["Goodness of fit", "Independence testing", "Categorical variables", "Expected frequency requirements"]))

    Q.append(_q(_sp, "easy",
        "What are outliers? How do you detect them and what do you do with them?",
        ["When should you keep outliers?", "What's the IQR method?"],
        ["Definition", "Z-score method", "IQR method", "Domain-dependent treatment", "Impact on models"]))

    Q.append(_q(_sp, "medium",
        "Explain the concept of conditional probability with a real-world example.",
        ["How does this connect to Bayes' theorem?", "What's the chain rule of probability?"],
        ["P(A|B) definition", "Joint vs marginal", "Independence", "Bayes connection"]))

    Q.append(_q(_sp, "hard",
        "What is the expectation-maximization algorithm? Explain it intuitively.",
        ["Where is EM used in practice?", "What are its limitations?"],
        ["Latent variables", "E-step and M-step", "Gaussian mixture models", "Convergence properties"],
        company="Mu Sigma", tags=[_sp, "advanced"]))

    Q.append(_q(_sp, "medium",
        "What is hypothesis testing? Walk me through the complete process for testing whether a new drug is effective.",
        ["What's the difference between one-tailed and two-tailed tests?", "When would you use a one-tailed test?"],
        ["Null and alternative hypotheses", "Test statistic", "P-value", "Decision rule", "Practical example"]))

    Q.append(_q(_sp, "easy",
        "What is standard deviation and why do we use it instead of just variance?",
        ["What's the relationship between the two?", "What does 'two standard deviations from the mean' mean practically?"],
        ["Spread measure", "Same units as data", "68-95-99.7 rule", "Interpretability"]))

    Q.append(_q(_sp, "medium",
        "Explain what a sampling distribution is. How is it different from the distribution of the data itself?",
        ["How does the standard error relate to this?", "Why does it matter for inference?"],
        ["Distribution of a statistic", "Repeated sampling", "Standard error", "CLT connection"]))

    Q.append(_q(_sp, "hard",
        "What is the Kolmogorov-Smirnov test? When would you use it over other normality tests?",
        ["What alternatives exist?", "What if your sample size is very small?"],
        ["Non-parametric test", "Compares CDFs", "Shapiro-Wilk alternative", "Sample size sensitivity"],
        company="Mu Sigma", tags=[_sp, "testing"]))

    Q.append(_q(_sp, "medium",
        "You observe that users who use Feature X have 30% higher retention. Does Feature X cause better retention?",
        ["How would you design an experiment to test causation?", "What confounders might exist?"],
        ["Selection bias", "Confounders", "A/B test design", "Causal inference basics"],
        company="Flipkart", tags=[_sp, "causal_inference"]))

    Q.append(_q(_sp, "easy",
        "What is the difference between discrete and continuous random variables? Give examples of each.",
        ["Can you convert one to the other?", "Which probability function does each use?"],
        ["Countable vs uncountable", "PMF vs PDF", "Examples", "Binning continuous"]))

    Q.append(_q(_sp, "medium",
        "Explain covariance and how it differs from correlation.",
        ["Why is correlation preferred in practice?", "Can two variables have zero correlation but be dependent?"],
        ["Joint variability", "Scale dependence of covariance", "Normalized version", "Non-linear dependence"]))

    Q.append(_q(_sp, "hard",
        "What is the bootstrap method? How does it help when you don't know the underlying distribution?",
        ["When would bootstrap fail?", "How many bootstrap samples do you typically need?"],
        ["Resampling with replacement", "Empirical distribution", "Confidence interval estimation", "Assumptions"]))

    Q.append(_q(_sp, "medium",
        "If I tell you a model has an R-squared of 0.95, should you be impressed? Why or why not?",
        ["What's adjusted R-squared?", "Can R-squared be negative?"],
        ["Proportion of variance explained", "Overfitting risk", "Adjusted for features", "Context matters"],
        company="Mu Sigma", tags=[_sp, "regression"]))

    Q.append(_q(_sp, "easy",
        "What is the difference between descriptive and inferential statistics?",
        ["Give me an example of each in a business context.", "Which one does machine learning use more?"],
        ["Summarizing vs generalizing", "Population inference", "Business examples", "ML connection"]))

    Q.append(_q(_sp, "medium",
        "Explain the concept of degrees of freedom. Why does it matter?",
        ["How do degrees of freedom affect the t-distribution?", "Why do we use n-1 for sample variance?"],
        ["Free parameters", "Bessel's correction", "t-distribution shape", "Information consumed by estimation"]))

    Q.append(_q(_sp, "hard",
        "What is Simpson's Paradox? Give me a real-world example and explain why it happens.",
        ["How do you detect it in your data?", "What's the implication for reporting aggregate statistics?"],
        ["Trend reversal in subgroups", "Lurking variable", "UC Berkeley example", "Disaggregation importance"],
        company="Goldman Sachs", tags=[_sp, "paradox"]))

    Q.append(_q(_sp, "medium",
        "What is a QQ-plot and how do you interpret it?",
        ["What does it look like for heavy-tailed data?", "How is it better than a histogram for checking normality?"],
        ["Quantile comparison", "Diagonal = normal", "Tail behavior", "Visual diagnostic"]))

    Q.append(_q(_sp, "easy",
        "What's the difference between independent and mutually exclusive events?",
        ["Can two events be both independent and mutually exclusive?", "Give a card game example."],
        ["P(A and B) = P(A)*P(B)", "P(A and B) = 0", "Cannot be both unless P=0", "Examples"]))

    Q.append(_q(_sp, "medium",
        "Explain the concept of statistical significance vs practical significance with a business example.",
        ["How would you communicate this to a non-technical stakeholder?", "What's an effect size?"],
        ["Large n detects tiny effects", "Business impact matters", "Effect size metrics", "Decision framework"]))

    Q.append(_q(_sp, "hard",
        "What is the multiple comparisons problem? You run 20 A/B tests -- how many false positives do you expect at alpha=0.05?",
        ["What's the Bonferroni correction?", "What about FDR control?"],
        ["Expected 1 false positive", "Family-wise error rate", "Bonferroni", "Benjamini-Hochberg"],
        company="Amazon", tags=[_sp, "ab_testing"]))

    Q.append(_q(_sp, "medium",
        "What is the difference between Bayesian and frequentist approaches to statistics?",
        ["When would you prefer Bayesian?", "What's a prior and how do you choose one?"],
        ["Philosophical difference", "Prior and posterior", "Credible vs confidence interval", "Practical trade-offs"]))

    Q.append(_q(_sp, "easy",
        "Explain what a normal distribution is. Why is it so common in nature?",
        ["What are the parameters?", "What's the 68-95-99.7 rule?"],
        ["Bell curve", "Mean and std dev", "CLT explains prevalence", "Empirical rule"]))

    Q.append(_q(_sp, "medium",
        "What is heteroscedasticity? Why is it a problem and how do you detect it?",
        ["How do you fix it?", "Which models are affected?"],
        ["Non-constant variance", "Residual plots", "Breusch-Pagan test", "Weighted least squares"],
        company="Mu Sigma", tags=[_sp, "regression"]))

    Q.append(_q(_sp, "hard",
        "Explain the concept of entropy in information theory. How is it used in decision trees?",
        ["What's the relationship between entropy and information gain?", "How does Gini impurity compare?"],
        ["Uncertainty measure", "Bits", "Information gain = entropy reduction", "Gini comparison"]))

    Q.append(_q(_sp, "medium",
        "You have two classifiers. Classifier A has 90% accuracy on your test set, Classifier B has 85%. Can you say A is significantly better?",
        ["How would you test this statistically?", "What's McNemar's test?"],
        ["Statistical testing needed", "McNemar's test", "Confidence intervals", "Cross-validation variance"]))

    Q.append(_q(_sp, "easy",
        "What is the law of total probability? Give a practical example.",
        ["How does it connect to Bayes' theorem?", "When is it useful in data science?"],
        ["Partition of sample space", "Weighted sum", "Marginalization", "Practical example"]))

    Q.append(_q(_sp, "medium",
        "Explain what a likelihood function is. How is it different from probability?",
        ["Why do we maximize likelihood?", "What's the log-likelihood?"],
        ["Function of parameters", "Fixed data", "Probability vs likelihood", "Optimization convenience"]))

    Q.append(_q(_sp, "hard",
        "What is the curse of dimensionality? How does it affect distance-based algorithms?",
        ["How do you mitigate it?", "At what dimensionality does it start to matter?"],
        ["Sparsity in high dimensions", "Distance concentration", "Dimensionality reduction", "Feature selection"],
        company="Mu Sigma", tags=[_sp, "high_dimensional"]))

    Q.append(_q(_sp, "medium",
        "What is survival analysis? Where would you use it in a tech company?",
        ["What's a hazard function?", "How is it different from regular regression?"],
        ["Time-to-event analysis", "Censoring", "Kaplan-Meier", "Churn prediction application"],
        company="Flipkart", tags=[_sp, "survival"]))

    Q.append(_q(_sp, "easy",
        "What is the difference between a population parameter and a sample statistic?",
        ["Give examples of each.", "Why do we use statistics to estimate parameters?"],
        ["True value vs estimate", "mu vs x-bar", "Sigma vs s", "Inference purpose"]))

    Q.append(_q(_sp, "medium",
        "Explain the ANOVA test. When would you use it instead of multiple t-tests?",
        ["What are the assumptions?", "What do you do if ANOVA is significant?"],
        ["Comparing multiple group means", "F-statistic", "Post-hoc tests", "Multiple comparison problem"]))

    Q.append(_q(_sp, "hard",
        "What is the difference between joint probability, marginal probability, and conditional probability? Explain with a real dataset example.",
        ["How do you compute marginal from joint?", "What is the chain rule?"],
        ["Definitions", "Marginalization by summing", "Conditioning", "Chain rule", "Table example"]))

    # ==================================================================
    # REGRESSION (30)
    # ==================================================================

    _reg = "regression"

    Q.append(_q(_reg, "easy",
        "Explain linear regression to me like I'm a college freshman. What does it actually do?",
        ["What is the 'line of best fit'?", "How do you measure 'best'?"],
        ["Relationship between variables", "Minimizing error", "Slope and intercept", "Prediction"]))

    Q.append(_q(_reg, "medium",
        "What are the assumptions of linear regression? What happens when they are violated?",
        ["How do you check each assumption?", "Which violation is the most dangerous?"],
        ["Linearity", "Independence", "Homoscedasticity", "Normality of residuals", "Consequences of violation"]))

    Q.append(_q(_reg, "medium",
        "Explain logistic regression. Why can't we just use linear regression for classification?",
        ["What's the sigmoid function?", "How do you interpret the coefficients?"],
        ["Probability output", "Sigmoid squashes to 0-1", "Log-odds interpretation", "Decision boundary"]))

    Q.append(_q(_reg, "medium",
        "What is multicollinearity? How do you detect it and why is it a problem?",
        ["What's VIF?", "Does multicollinearity affect prediction accuracy?"],
        ["Correlated predictors", "Unstable coefficients", "VIF > 5 or 10", "Prediction vs interpretation"],
        company="Mu Sigma", tags=[_reg, "diagnostics"]))

    Q.append(_q(_reg, "hard",
        "Explain L1 and L2 regularization. Why does L1 produce sparse solutions while L2 doesn't?",
        ["Draw the constraint regions.", "When would you use Elastic Net?"],
        ["Lasso vs Ridge", "Diamond vs circle constraint", "Sparsity geometry", "Feature selection with L1"]))

    Q.append(_q(_reg, "easy",
        "What is the cost function in linear regression? Why do we use squared error?",
        ["What about absolute error?", "What's the gradient descent approach?"],
        ["MSE/SSE", "Convexity", "Differentiability", "MAE alternative"]))

    Q.append(_q(_reg, "medium",
        "If I add more features to my regression model, R-squared always increases. Is this a good thing?",
        ["What's adjusted R-squared?", "How do you decide which features to keep?"],
        ["Overfitting", "Adjusted R-squared penalty", "Feature selection", "AIC/BIC"]))

    Q.append(_q(_reg, "medium",
        "Explain the difference between Ridge regression and Lasso regression with a practical example.",
        ["When would you prefer one over the other?", "What's the effect on feature coefficients?"],
        ["L2 vs L1 penalty", "Shrinkage vs zeroing", "Feature selection", "Use cases"]))

    Q.append(_q(_reg, "hard",
        "You built a regression model and the residual plot shows a funnel shape. What does this mean and how do you fix it?",
        ["What transformation might help?", "How does this affect confidence intervals?"],
        ["Heteroscedasticity", "Log transform", "WLS", "Invalid standard errors"],
        company="Goldman Sachs", tags=[_reg, "diagnostics"]))

    Q.append(_q(_reg, "easy",
        "What is the difference between simple and multiple linear regression?",
        ["How do you interpret coefficients in multiple regression?", "What's the 'holding other variables constant' interpretation?"],
        ["One vs multiple predictors", "Partial regression coefficients", "Ceteris paribus", "Complexity trade-off"]))

    Q.append(_q(_reg, "medium",
        "How does gradient descent work in linear regression? Why not just use the normal equation?",
        ["What's the difference between batch, mini-batch, and stochastic gradient descent?", "What's the learning rate?"],
        ["Iterative optimization", "Normal equation limitations", "Scalability", "Learning rate choice"]))

    Q.append(_q(_reg, "medium",
        "What is polynomial regression? When would you use it and what are the risks?",
        ["How do you choose the degree?", "How does it relate to overfitting?"],
        ["Non-linear relationships", "Degree selection", "Overfitting risk", "Cross-validation for degree"]))

    Q.append(_q(_reg, "hard",
        "Explain the bias-variance trade-off in the context of regression models.",
        ["How does model complexity relate to bias and variance?", "What's the optimal trade-off point?"],
        ["Underfitting vs overfitting", "Total error decomposition", "Complexity curve", "Regularization connection"]))

    Q.append(_q(_reg, "medium",
        "What are interaction terms in regression? Give a real-world example where they matter.",
        ["How do you test if an interaction is significant?", "How does it change interpretation?"],
        ["Combined effect", "Non-additive relationships", "Marketing example", "Interpretation complexity"]))

    Q.append(_q(_reg, "easy",
        "What is the difference between regression and classification?",
        ["Can logistic regression be used for regression?", "What about regression trees?"],
        ["Continuous vs categorical output", "Different loss functions", "Overlap in methods", "Examples"]))

    Q.append(_q(_reg, "medium",
        "How do you handle categorical variables in a regression model?",
        ["What's the dummy variable trap?", "How do you handle ordinal categories?"],
        ["One-hot encoding", "Dummy variable trap", "N-1 dummies", "Ordinal encoding options"]))

    Q.append(_q(_reg, "hard",
        "What is quantile regression and when is it more useful than ordinary least squares?",
        ["How does it handle outliers differently?", "Give a use case in e-commerce."],
        ["Predicts quantiles not mean", "Robust to outliers", "Heterogeneous effects", "Delivery time prediction"],
        company="Flipkart", tags=[_reg, "advanced"]))

    Q.append(_q(_reg, "medium",
        "Explain how you would interpret logistic regression coefficients. What do odds ratios mean?",
        ["How do you go from log-odds to probability?", "What does a coefficient of 0.5 mean?"],
        ["Log-odds interpretation", "Odds ratio = exp(beta)", "Probability conversion", "Practical meaning"]))

    Q.append(_q(_reg, "medium",
        "What is regularization and why do we need it? Explain with a regression example.",
        ["What happens if lambda is too large?", "How do you choose lambda?"],
        ["Penalty on complexity", "Overfitting prevention", "Cross-validation for lambda", "Bias-variance trade-off"]))

    Q.append(_q(_reg, "hard",
        "You have 50 features and 100 samples. What regression approach would you use and why?",
        ["Would OLS work here?", "How does regularization help in this scenario?"],
        ["p > n problem", "Lasso/Ridge", "Dimensionality reduction", "Feature selection needed"],
        company="Mu Sigma", tags=[_reg, "high_dimensional"]))

    Q.append(_q(_reg, "medium",
        "What are residuals? How do you use residual analysis to diagnose model problems?",
        ["What should a good residual plot look like?", "What patterns indicate problems?"],
        ["Actual minus predicted", "Random scatter ideal", "Patterns indicate violations", "Diagnostic plots"]))

    Q.append(_q(_reg, "easy",
        "What's the difference between correlation and regression?",
        ["Can you have high correlation but poor regression?", "Which one implies directionality?"],
        ["Relationship strength vs prediction", "Directionality", "Both measure linear association", "Use cases"]))

    Q.append(_q(_reg, "medium",
        "Explain stepwise regression. What are its pros and cons?",
        ["What's forward vs backward selection?", "Why do statisticians dislike stepwise?"],
        ["Automated feature selection", "Forward/backward/both", "Overfitting risk", "P-value instability"]))

    Q.append(_q(_reg, "hard",
        "What is the difference between MLE and OLS for estimating regression parameters? When do they give the same result?",
        ["Under what distribution assumption do they agree?", "What if errors are not normal?"],
        ["Normality assumption equivalence", "Gaussian errors", "MLE more general", "Robust alternatives"],
        company="Goldman Sachs", tags=[_reg, "theory"]))

    Q.append(_q(_reg, "medium",
        "How do you handle non-linear relationships in regression without using non-linear models?",
        ["What transformations are common?", "When would you use splines?"],
        ["Log transforms", "Polynomial terms", "Interaction terms", "Basis function expansion"]))

    Q.append(_q(_reg, "medium",
        "What is the coefficient of determination (R-squared)? What are its limitations?",
        ["Can R-squared be misleading?", "What does a negative R-squared mean?"],
        ["Proportion of explained variance", "Only for linear", "Doesn't imply causation", "Adjusted version"]))

    Q.append(_q(_reg, "easy",
        "If your linear regression has a very high R-squared on training data but poor performance on test data, what happened?",
        ["How would you fix this?", "What regularization technique would you try?"],
        ["Overfitting", "Too many features", "Regularization", "Cross-validation"]))

    Q.append(_q(_reg, "medium",
        "What is the difference between parametric and non-parametric regression?",
        ["Give examples of each.", "When would you prefer non-parametric?"],
        ["Fixed vs flexible form", "Linear vs KNN regression", "Assumptions", "Data requirements"]))

    Q.append(_q(_reg, "hard",
        "Explain Generalized Linear Models. How do logistic and Poisson regression fit into this framework?",
        ["What's a link function?", "What's the exponential family?"],
        ["Link function", "Exponential family", "Canonical links", "Unified framework"]))

    Q.append(_q(_reg, "medium",
        "You built a logistic regression model for credit risk. The AUC is 0.92 but the business team says it's not useful. What could be wrong?",
        ["What if the threshold is wrong?", "How would you calibrate the probabilities?"],
        ["Threshold optimization", "Calibration", "Business metric alignment", "Cost-sensitive classification"],
        company="Goldman Sachs", tags=[_reg, "applied"]))

    # ==================================================================
    # CLASSIFICATION (30)
    # ==================================================================

    _cls = "classification"

    Q.append(_q(_cls, "easy",
        "Explain decision trees to me. How does a decision tree decide where to split?",
        ["What's information gain?", "Why are decision trees prone to overfitting?"],
        ["Recursive partitioning", "Split criteria", "Gini/Entropy", "Overfitting and pruning"]))

    Q.append(_q(_cls, "medium",
        "What is Random Forest? How does it improve over a single decision tree?",
        ["What's bagging?", "How does feature randomness help?"],
        ["Ensemble of trees", "Bagging", "Feature subsampling", "Variance reduction"]))

    Q.append(_q(_cls, "medium",
        "Explain Support Vector Machines. What is the intuition behind finding the maximum margin hyperplane?",
        ["What are support vectors?", "How does the kernel trick work?"],
        ["Maximum margin classifier", "Support vectors definition", "Kernel for non-linear", "Soft margin"]))

    Q.append(_q(_cls, "easy",
        "How does K-Nearest Neighbors work? What are its strengths and weaknesses?",
        ["How do you choose K?", "Why is KNN called a lazy learner?"],
        ["Distance-based classification", "No training phase", "K selection", "Curse of dimensionality"]))

    Q.append(_q(_cls, "medium",
        "Explain Naive Bayes classifier. Why is it called 'naive' and when does it work surprisingly well?",
        ["What's the independence assumption?", "How does it handle continuous features?"],
        ["Bayes theorem application", "Conditional independence assumption", "Text classification strength", "Gaussian NB"]))

    Q.append(_q(_cls, "medium",
        "What is ensemble learning? Compare bagging and boosting.",
        ["When would you use boosting over bagging?", "What's the bias-variance perspective?"],
        ["Combining multiple models", "Bagging reduces variance", "Boosting reduces bias", "Examples of each"]))

    Q.append(_q(_cls, "hard",
        "Explain how XGBoost works. Why has it been so successful in competitions?",
        ["What's the difference between XGBoost and regular gradient boosting?", "What regularization does XGBoost add?"],
        ["Sequential tree building", "Gradient optimization", "Regularization terms", "Speed optimizations"],
        company="Amazon", tags=[_cls, "ensemble"]))

    Q.append(_q(_cls, "medium",
        "If I give you a dataset with 80% class imbalance, how would you build a classifier?",
        ["What sampling techniques would you use?", "Which metrics would you optimize?"],
        ["SMOTE/oversampling", "Undersampling", "Class weights", "F1 over accuracy", "Stratified splitting"],
        company="Flipkart", tags=[_cls, "imbalance"]))

    Q.append(_q(_cls, "easy",
        "What is the difference between a parametric and non-parametric classifier? Give examples.",
        ["Which one needs more data?", "Which one is more flexible?"],
        ["Fixed vs flexible structure", "Logistic vs KNN", "Data requirements", "Assumption trade-offs"]))

    Q.append(_q(_cls, "medium",
        "Explain the concept of a decision boundary. How does it differ for logistic regression vs SVM vs decision trees?",
        ["Can decision boundaries be non-linear?", "Which algorithm gives the simplest boundary?"],
        ["Separating classes in feature space", "Linear vs non-linear", "Piecewise for trees", "Margin for SVM"]))

    Q.append(_q(_cls, "hard",
        "What is gradient boosting? Walk me through how it builds each successive tree.",
        ["What's the residual learning intuition?", "How does the learning rate affect performance?"],
        ["Sequential fitting to residuals", "Shrinkage", "Learning rate trade-off", "Number of trees vs depth"]))

    Q.append(_q(_cls, "medium",
        "Compare decision tree, random forest, and gradient boosting. When would you use each?",
        ["How do training times compare?", "Which is most interpretable?"],
        ["Single tree for interpretability", "RF for variance reduction", "GBM for accuracy", "Trade-offs"]))

    Q.append(_q(_cls, "easy",
        "What is overfitting in classification? How do you detect and prevent it?",
        ["What does the training vs validation accuracy curve look like?", "Name 3 techniques to prevent overfitting."],
        ["Memorizing noise", "Train-test gap", "Regularization", "Cross-validation", "Early stopping"]))

    Q.append(_q(_cls, "medium",
        "How does the kernel trick in SVM work? Explain the intuition without heavy math.",
        ["What's the RBF kernel?", "How do you choose which kernel to use?"],
        ["Implicit high-dimensional mapping", "Inner product in feature space", "Common kernels", "Grid search for selection"]))

    Q.append(_q(_cls, "hard",
        "You have a fraud detection system. Only 0.1% of transactions are fraudulent. How do you build and evaluate a model for this?",
        ["Why is accuracy a terrible metric here?", "What's the cost of a false negative vs false positive?"],
        ["Extreme imbalance handling", "Precision-recall focus", "Cost-sensitive learning", "Anomaly detection alternative"],
        company="Goldman Sachs", tags=[_cls, "imbalance", "fraud"]))

    Q.append(_q(_cls, "medium",
        "What is the difference between hard and soft classification? When would you prefer probability outputs?",
        ["How does logistic regression give probabilities?", "How do you calibrate probabilities?"],
        ["Label vs probability", "Threshold flexibility", "Calibration", "Business decision making"]))

    Q.append(_q(_cls, "easy",
        "Explain the concept of a confusion matrix. What information can you extract from it?",
        ["How do you compute precision and recall from it?", "What's a good confusion matrix look like?"],
        ["TP, FP, TN, FN", "Derived metrics", "Visualization", "Per-class analysis"]))

    Q.append(_q(_cls, "medium",
        "What is AdaBoost? How is it different from Random Forest?",
        ["How does AdaBoost weight misclassified samples?", "Which is more prone to overfitting?"],
        ["Adaptive boosting", "Sequential weighting", "Boosting vs bagging", "Noise sensitivity"]))

    Q.append(_q(_cls, "medium",
        "Explain multiclass classification strategies: one-vs-all and one-vs-one.",
        ["Which one is computationally more expensive?", "How does softmax handle multiclass natively?"],
        ["Binary to multiclass", "N vs N*(N-1)/2 classifiers", "Softmax alternative", "Practical considerations"]))

    Q.append(_q(_cls, "hard",
        "What is a Gaussian Mixture Model? How is it different from K-means for classification?",
        ["When would you prefer GMM?", "How does it handle overlapping clusters?"],
        ["Soft assignment", "Probabilistic model", "EM algorithm", "Covariance structure"],
        company="Mu Sigma", tags=[_cls, "probabilistic"]))

    Q.append(_q(_cls, "medium",
        "How would you handle missing values before building a classifier?",
        ["Does the method depend on the algorithm?", "When is imputation better than deletion?"],
        ["Imputation methods", "MCAR/MAR/MNAR", "Algorithm-specific handling", "Impact on bias"]))

    Q.append(_q(_cls, "easy",
        "What is the difference between a generative and discriminative classifier?",
        ["Give examples of each.", "Which one models P(X|Y) vs P(Y|X)?"],
        ["Modeling joint vs conditional", "Naive Bayes vs logistic regression", "Trade-offs", "Data efficiency"]))

    Q.append(_q(_cls, "medium",
        "Explain how a decision tree handles continuous features vs categorical features.",
        ["What's a threshold split?", "How does it handle ordinal features?"],
        ["Threshold selection for continuous", "Subset selection for categorical", "Ordinal treatment", "Computational cost"]))

    Q.append(_q(_cls, "hard",
        "What is stacking in ensemble learning? How does it differ from bagging and boosting?",
        ["How do you train the meta-learner?", "What prevents data leakage in stacking?"],
        ["Meta-learning concept", "Level 0 and level 1", "Cross-validation for stacking", "Diversity of base learners"]))

    Q.append(_q(_cls, "medium",
        "You're building a model to predict customer churn. Walk me through your complete approach from data to deployment.",
        ["Which features would be most important?", "How would you handle temporal aspects?"],
        ["Feature engineering", "Class imbalance", "Model selection", "Temporal validation", "Business integration"],
        company="Flipkart", tags=[_cls, "applied"]))

    Q.append(_q(_cls, "easy",
        "What is a hyperparameter? How is it different from a model parameter? Give examples for decision trees.",
        ["How do you tune hyperparameters?", "What's grid search vs random search?"],
        ["Learned vs set by user", "Max depth, min samples", "Grid vs random search", "Cross-validation"]))

    Q.append(_q(_cls, "medium",
        "How does the learning rate affect gradient boosting models?",
        ["What's the relationship between learning rate and number of trees?", "What's a typical starting value?"],
        ["Step size in gradient space", "Trade-off with n_estimators", "Regularization effect", "Typical values"]))

    Q.append(_q(_cls, "hard",
        "Compare LightGBM and XGBoost. What are the key architectural differences?",
        ["What's histogram-based splitting?", "When would you prefer LightGBM?"],
        ["Leaf-wise vs level-wise", "Histogram binning", "Categorical feature handling", "Speed comparison"],
        company="Amazon", tags=[_cls, "ensemble"]))

    Q.append(_q(_cls, "medium",
        "What is multi-label classification? How is it different from multiclass?",
        ["Give a real-world example.", "How do you evaluate multi-label models?"],
        ["Multiple labels per instance", "Movie genre example", "Binary relevance", "Hamming loss, micro/macro F1"]))

    Q.append(_q(_cls, "medium",
        "Explain the No Free Lunch theorem. What does it mean for choosing classifiers?",
        ["Does this mean there's no best algorithm?", "How does this guide your model selection strategy?"],
        ["No universally best algorithm", "Problem-specific performance", "Empirical comparison needed", "Algorithm diversity"]))

    # ==================================================================
    # CLUSTERING (20)
    # ==================================================================

    _clu = "clustering"

    Q.append(_q(_clu, "easy",
        "Explain K-Means clustering. How does it work step by step?",
        ["How do you choose K?", "What are its limitations?"],
        ["Initialize centroids", "Assign-update loop", "Convergence", "Sensitivity to initialization"]))

    Q.append(_q(_clu, "medium",
        "What is the elbow method? How do you use it to choose the number of clusters?",
        ["What if there's no clear elbow?", "What alternatives exist?"],
        ["WCSS vs K plot", "Diminishing returns", "Silhouette method alternative", "Gap statistic"]))

    Q.append(_q(_clu, "medium",
        "Explain hierarchical clustering. What's the difference between agglomerative and divisive?",
        ["How do you read a dendrogram?", "What are different linkage methods?"],
        ["Bottom-up vs top-down", "Dendrogram interpretation", "Single/complete/average linkage", "No need to prespecify K"]))

    Q.append(_q(_clu, "medium",
        "What is DBSCAN? When would you prefer it over K-Means?",
        ["What are epsilon and minPts?", "How does it handle noise?"],
        ["Density-based clustering", "No K needed", "Handles arbitrary shapes", "Noise as outliers"]))

    Q.append(_q(_clu, "medium",
        "What is the silhouette score? How do you interpret it?",
        ["What's a good silhouette score?", "Can you compute it per point?"],
        ["Cohesion vs separation", "Range -1 to 1", "Per-point analysis", "Cluster quality measure"]))

    Q.append(_q(_clu, "easy",
        "What's the difference between clustering and classification?",
        ["Can clustering results be used for classification?", "Give a business use case for clustering."],
        ["Unsupervised vs supervised", "No labels in clustering", "Customer segmentation example", "Pseudo-labeling"]))

    Q.append(_q(_clu, "hard",
        "You have customer transaction data for an e-commerce platform. How would you segment customers using clustering?",
        ["What features would you engineer?", "How do you validate the clusters make business sense?"],
        ["RFM features", "Feature scaling", "Algorithm choice", "Business validation", "Segment profiling"],
        company="Flipkart", tags=[_clu, "applied"]))

    Q.append(_q(_clu, "medium",
        "What are the limitations of K-Means clustering?",
        ["How does K-Means++ help?", "What about non-spherical clusters?"],
        ["Spherical assumption", "Sensitive to outliers", "Fixed K", "K-Means++ initialization"]))

    Q.append(_q(_clu, "medium",
        "How do you evaluate clustering quality when you don't have ground truth labels?",
        ["What internal metrics exist?", "What about external metrics when labels are available?"],
        ["Silhouette", "Davies-Bouldin", "Calinski-Harabasz", "ARI and NMI for external"]))

    Q.append(_q(_clu, "hard",
        "Explain Gaussian Mixture Models for clustering. How is it different from K-Means?",
        ["What's soft vs hard assignment?", "How does EM fit the GMM?"],
        ["Probabilistic assignment", "Covariance modeling", "EM algorithm", "Model selection with BIC"]))

    Q.append(_q(_clu, "easy",
        "What is the difference between distance-based and density-based clustering?",
        ["Give an example of each.", "Which handles noise better?"],
        ["K-Means vs DBSCAN", "Cluster shape assumptions", "Noise handling", "When to use which"]))

    Q.append(_q(_clu, "medium",
        "How does feature scaling affect clustering results? Which scaling method would you use?",
        ["What happens if you don't scale?", "Does PCA help before clustering?"],
        ["Dominant feature problem", "StandardScaler vs MinMaxScaler", "Distance metric impact", "Dimensionality reduction"]))

    Q.append(_q(_clu, "medium",
        "What is spectral clustering? When is it preferred over K-Means?",
        ["How does it use graph theory?", "What's the computational cost?"],
        ["Graph-based approach", "Eigenvalue decomposition", "Non-convex clusters", "Scalability issues"]))

    Q.append(_q(_clu, "hard",
        "You have text documents and need to cluster them into topics. Walk me through your approach.",
        ["What text representation would you use?", "How do you determine the number of topics?"],
        ["TF-IDF or embeddings", "Dimensionality reduction", "Clustering algorithm choice", "Topic coherence evaluation"],
        company="Mu Sigma", tags=[_clu, "nlp"]))

    Q.append(_q(_clu, "medium",
        "What is the gap statistic for determining the optimal number of clusters?",
        ["How does it compare to the elbow method?", "What's the null reference distribution?"],
        ["Compares to random data", "Reference distribution", "Statistical approach", "More rigorous than elbow"]))

    Q.append(_q(_clu, "easy",
        "Can K-Means handle categorical data? If not, what alternative would you use?",
        ["What's K-Modes?", "What about mixed data types?"],
        ["K-Means needs numeric", "K-Modes for categorical", "K-Prototypes for mixed", "Encoding approaches"]))

    Q.append(_q(_clu, "medium",
        "What is the OPTICS algorithm? How does it relate to DBSCAN?",
        ["What problem does OPTICS solve that DBSCAN doesn't?", "What's a reachability plot?"],
        ["Variable density handling", "Reachability distance", "Ordering of points", "Generalization of DBSCAN"]))

    Q.append(_q(_clu, "hard",
        "How would you cluster time-series data? What distance metric would you use?",
        ["What's Dynamic Time Warping?", "How does time-series clustering differ from regular clustering?"],
        ["DTW distance", "Shape-based vs feature-based", "Temporal alignment", "Subsequence clustering"]))

    Q.append(_q(_clu, "medium",
        "What is the difference between partitional and hierarchical clustering approaches?",
        ["When would you choose one over the other?", "Can you combine them?"],
        ["Flat vs tree structure", "Scalability differences", "Nested vs non-nested", "Bisecting K-Means hybrid"]))

    Q.append(_q(_clu, "medium",
        "How do you handle high-dimensional data in clustering?",
        ["What's subspace clustering?", "Does PCA always help?"],
        ["Curse of dimensionality", "PCA/t-SNE preprocessing", "Feature selection", "Subspace approaches"]))

    # ==================================================================
    # FEATURE ENGINEERING (25)
    # ==================================================================

    _fe = "feature_engineering"

    Q.append(_q(_fe, "easy",
        "What is feature engineering? Why is it considered more important than model selection?",
        ["Give me an example of a creative feature.", "How do you know when to stop engineering features?"],
        ["Creating informative inputs", "Domain knowledge application", "Model performance impact", "Diminishing returns"]))

    Q.append(_q(_fe, "medium",
        "Compare one-hot encoding, label encoding, and target encoding for categorical variables. When would you use each?",
        ["What's the cardinality problem with one-hot?", "How does target encoding cause data leakage?"],
        ["Nominal vs ordinal", "High cardinality handling", "Leakage in target encoding", "Algorithm-specific choices"]))

    Q.append(_q(_fe, "medium",
        "What is feature scaling? Compare StandardScaler, MinMaxScaler, and RobustScaler.",
        ["Which algorithms need scaling?", "Which scaler is best with outliers?"],
        ["Z-score vs min-max", "Outlier sensitivity", "Algorithm requirements", "RobustScaler for outliers"]))

    Q.append(_q(_fe, "medium",
        "You have a dataset with 30% missing values in several columns. Walk me through your strategy.",
        ["When would you drop columns vs impute?", "What's multiple imputation?"],
        ["MCAR/MAR/MNAR assessment", "Simple vs advanced imputation", "KNN imputer", "Missingness as a feature"]))

    Q.append(_q(_fe, "hard",
        "Explain PCA. What does it do and when should you use it?",
        ["How do you choose the number of components?", "What are the limitations of PCA?"],
        ["Variance maximization", "Eigenvalues and eigenvectors", "Explained variance ratio", "Linearity assumption"]))

    Q.append(_q(_fe, "medium",
        "What is feature importance? Compare different methods for measuring it.",
        ["How does tree-based feature importance work?", "What's permutation importance?"],
        ["Impurity-based", "Permutation-based", "SHAP values", "Correlation-based"]))

    Q.append(_q(_fe, "easy",
        "What is the difference between feature selection and feature extraction?",
        ["Give examples of each.", "When would you prefer one over the other?"],
        ["Selecting subset vs creating new", "PCA vs filter methods", "Interpretability trade-off", "Dimensionality reduction"]))

    Q.append(_q(_fe, "medium",
        "Explain forward selection, backward elimination, and recursive feature elimination.",
        ["Which is most computationally expensive?", "How does RFE use a model internally?"],
        ["Greedy approaches", "Wrapper methods", "RFE with estimator", "Computational trade-offs"]))

    Q.append(_q(_fe, "medium",
        "How do you create features from datetime columns? Give me at least 5 useful features.",
        ["How would you encode cyclical features like month?", "What about lag features?"],
        ["Hour, day, month, day of week", "Is_weekend", "Sine/cosine encoding", "Time since event", "Lag features"]))

    Q.append(_q(_fe, "hard",
        "What is target encoding? How do you implement it without data leakage?",
        ["What's leave-one-out encoding?", "How does smoothing help?"],
        ["Mean of target per category", "Cross-validation encoding", "Smoothing with global mean", "Leakage prevention"],
        company="Amazon", tags=[_fe, "encoding"]))

    Q.append(_q(_fe, "medium",
        "What are interaction features? How do you decide which interactions to create?",
        ["Can you automate interaction discovery?", "What's the risk of too many interactions?"],
        ["Product/ratio of features", "Domain knowledge", "Polynomial features", "Curse of dimensionality"]))

    Q.append(_q(_fe, "easy",
        "What is binning/discretization? When would you convert a continuous variable to categorical?",
        ["What's equal-width vs equal-frequency binning?", "Can binning lose information?"],
        ["Continuous to discrete", "Noise reduction", "Non-linear relationship capture", "Information loss"]))

    Q.append(_q(_fe, "medium",
        "How do you handle text data as features for a machine learning model?",
        ["Compare TF-IDF and word embeddings.", "When would you use bag-of-words?"],
        ["Text vectorization", "BoW vs TF-IDF vs embeddings", "Sparse vs dense", "Contextual embeddings"]))

    Q.append(_q(_fe, "hard",
        "What are SHAP values? How do they explain feature contributions for individual predictions?",
        ["How is SHAP different from LIME?", "What's the computational cost of SHAP?"],
        ["Shapley values from game theory", "Additive feature attribution", "Local interpretability", "LIME comparison"],
        company="Mu Sigma", tags=[_fe, "explainability"]))

    Q.append(_q(_fe, "medium",
        "How do you handle highly skewed features? What transformations would you apply?",
        ["When would you use log vs Box-Cox?", "Does the algorithm matter?"],
        ["Log transform", "Box-Cox", "Yeo-Johnson", "Algorithm sensitivity to skewness"]))

    Q.append(_q(_fe, "medium",
        "What is multicollinearity in features and how does it affect different models?",
        ["How do you detect it?", "Does it matter for tree-based models?"],
        ["VIF", "Correlation matrix", "Impact on linear models", "Tree models less affected"]))

    Q.append(_q(_fe, "easy",
        "What is the difference between filter, wrapper, and embedded feature selection methods?",
        ["Give an example of each.", "Which is fastest?"],
        ["Statistical tests vs model-based", "Examples of each", "Speed vs accuracy trade-off", "Lasso as embedded"]))

    Q.append(_q(_fe, "medium",
        "How would you engineer features for a recommendation system?",
        ["What user features would you create?", "What about item features?"],
        ["User history aggregations", "Item popularity", "User-item interaction features", "Temporal patterns"],
        company="Amazon", tags=[_fe, "recommendation"]))

    Q.append(_q(_fe, "hard",
        "What is t-SNE? How is it different from PCA for dimensionality reduction?",
        ["Why can't you use t-SNE for feature extraction in a model?", "What's UMAP and how does it compare?"],
        ["Non-linear reduction", "Perplexity parameter", "Visualization only", "Not for new data transformation"]))

    Q.append(_q(_fe, "medium",
        "How do you handle imbalanced features where 95% of values are the same?",
        ["Should you drop near-zero variance features?", "When might they still be useful?"],
        ["Near-zero variance", "Information content", "Rare event detection", "Domain-specific importance"]))

    Q.append(_q(_fe, "medium",
        "What is feature hashing? When would you use it?",
        ["How does it handle collisions?", "What's the trade-off with one-hot encoding?"],
        ["Hash trick", "Fixed dimensionality", "Collision trade-off", "High cardinality solution"]))

    Q.append(_q(_fe, "hard",
        "You have a dataset with 500 features. Walk me through your feature selection pipeline.",
        ["How do you balance thoroughness with computational cost?", "What order would you apply different methods?"],
        ["Variance threshold first", "Correlation removal", "Model-based selection", "Cross-validation", "Domain review"],
        company="Mu Sigma", tags=[_fe, "pipeline"]))

    Q.append(_q(_fe, "easy",
        "What is data leakage? Give me an example of how feature engineering can accidentally cause it.",
        ["How do you prevent it?", "Why is it hard to detect?"],
        ["Future information in training", "Target leakage example", "Temporal leakage", "Train-test split discipline"]))

    Q.append(_q(_fe, "medium",
        "How do you create features from geographic data (latitude, longitude)?",
        ["What's geohashing?", "How would you compute distance features?"],
        ["Haversine distance", "Geohash binning", "Proximity to landmarks", "Clustering-based regions"]))

    Q.append(_q(_fe, "medium",
        "What is the Variance Inflation Factor? How do you use it in practice?",
        ["What VIF threshold indicates a problem?", "What do you do when VIF is high?"],
        ["Multicollinearity measure", "VIF > 5 or 10", "Remove or combine features", "Regression diagnostics"]))

    # ==================================================================
    # MODEL EVALUATION (25)
    # ==================================================================

    _me = "model_evaluation"

    Q.append(_q(_me, "easy",
        "Explain accuracy, precision, recall, and F1 score. When would you prioritize each one?",
        ["Give a medical diagnosis example.", "What's the F1 score formula?"],
        ["Definitions of each", "When accuracy misleads", "Precision vs recall trade-off", "F1 as harmonic mean"]))

    Q.append(_q(_me, "medium",
        "What is the AUC-ROC curve? How do you interpret it?",
        ["What does AUC = 0.5 mean?", "When is precision-recall curve better than ROC?"],
        ["TPR vs FPR plot", "Area under curve", "Random baseline", "Imbalanced data preference for PR curve"]))

    Q.append(_q(_me, "medium",
        "Explain k-fold cross-validation. Why is it better than a single train-test split?",
        ["What's stratified k-fold?", "What value of k do you typically use?"],
        ["Data utilization", "Variance reduction", "Stratification for imbalance", "k=5 or 10 typical"]))

    Q.append(_q(_me, "medium",
        "What is the bias-variance trade-off? Draw the typical U-shaped curve and explain it.",
        ["How does model complexity relate to bias and variance?", "What's irreducible error?"],
        ["Underfitting = high bias", "Overfitting = high variance", "Sweet spot", "Irreducible noise"]))

    Q.append(_q(_me, "hard",
        "You have a model with 99% accuracy for fraud detection. Why might this be terrible?",
        ["What metrics would you use instead?", "How do you set the classification threshold?"],
        ["Class imbalance problem", "Precision and recall", "Cost-sensitive evaluation", "Threshold optimization"],
        company="Goldman Sachs", tags=[_me, "imbalance"]))

    Q.append(_q(_me, "easy",
        "What is overfitting? How do you detect it and what can you do about it?",
        ["What does the learning curve look like?", "Name 3 regularization techniques."],
        ["Memorizing training data", "Train-test gap", "Regularization", "More data", "Simpler model"]))

    Q.append(_q(_me, "medium",
        "Compare different cross-validation strategies: k-fold, leave-one-out, and time-series split.",
        ["When must you use time-series split?", "What's the computational cost of LOOCV?"],
        ["Standard k-fold", "LOOCV extreme", "Temporal ordering", "Appropriate for different data types"]))

    Q.append(_q(_me, "medium",
        "What is the log loss (binary cross-entropy)? Why is it preferred over accuracy for probabilistic models?",
        ["How does it penalize confident wrong predictions?", "What's the relationship to information theory?"],
        ["Probability-aware metric", "Penalizes confidence in wrong class", "Proper scoring rule", "Entropy connection"]))

    Q.append(_q(_me, "hard",
        "How do you compare two models statistically? Just saying 'Model A has higher accuracy' isn't enough.",
        ["What's the paired t-test for cross-validation?", "What about McNemar's test?"],
        ["Statistical significance testing", "Paired comparisons", "Confidence intervals", "Multiple comparison correction"]))

    Q.append(_q(_me, "medium",
        "What is a calibration curve? Why does it matter for real-world deployment?",
        ["How do you calibrate a model?", "What's Platt scaling?"],
        ["Predicted vs actual probability", "Reliability diagram", "Platt scaling", "Isotonic regression"]))

    Q.append(_q(_me, "easy",
        "What is the confusion matrix? Walk me through every cell with a spam detection example.",
        ["How do you compute precision from it?", "What's the difference between sensitivity and specificity?"],
        ["TP/FP/TN/FN with spam example", "Precision = TP/(TP+FP)", "Sensitivity = recall", "Specificity = TN/(TN+FP)"]))

    Q.append(_q(_me, "medium",
        "When would you use RMSE vs MAE vs MAPE for evaluating regression models?",
        ["How does RMSE penalize outliers differently?", "When does MAPE fail?"],
        ["Squared penalty in RMSE", "MAE robustness", "MAPE percentage interpretation", "Zero values break MAPE"]))

    Q.append(_q(_me, "hard",
        "What is the difference between model performance on IID test data vs out-of-distribution data? How do you test for robustness?",
        ["What's domain shift?", "How do you detect distribution drift in production?"],
        ["IID assumption", "Covariate shift", "Concept drift", "Monitoring strategies"],
        company="Amazon", tags=[_me, "production"]))

    Q.append(_q(_me, "medium",
        "Explain precision-recall trade-off. How do you choose the optimal threshold for your problem?",
        ["What if false negatives cost 10x more than false positives?", "What's the F-beta score?"],
        ["Threshold selection", "Cost-based optimization", "F-beta weighting", "PR curve analysis"]))

    Q.append(_q(_me, "medium",
        "What is the difference between micro-averaging and macro-averaging for multiclass metrics?",
        ["When would results differ significantly?", "Which is better for imbalanced classes?"],
        ["Aggregate vs per-class", "Class imbalance effect", "Micro favors majority", "Macro treats classes equally"]))

    Q.append(_q(_me, "easy",
        "What is a learning curve? What do different shapes tell you about your model?",
        ["What does a flat training curve mean?", "What if training and validation curves diverge?"],
        ["Performance vs training size", "Convergence patterns", "Overfitting signature", "Underfitting signature"]))

    Q.append(_q(_me, "medium",
        "How do you perform hyperparameter tuning? Compare grid search, random search, and Bayesian optimization.",
        ["Why does random search often beat grid search?", "What's the computational trade-off?"],
        ["Exhaustive vs random vs informed", "Random covers space better", "Bayesian uses past results", "Computational budget"]))

    Q.append(_q(_me, "hard",
        "What is nested cross-validation? When do you need it instead of regular cross-validation?",
        ["What's the risk of using the same CV for model selection and evaluation?", "How does it work structurally?"],
        ["Selection bias in CV", "Inner loop for tuning", "Outer loop for evaluation", "Unbiased performance estimate"]))

    Q.append(_q(_me, "medium",
        "You deployed a model 6 months ago and its performance is degrading. What could be happening?",
        ["How do you monitor model performance in production?", "What's concept drift vs data drift?"],
        ["Concept drift", "Data drift", "Feature drift", "Monitoring and retraining strategy"],
        company="Flipkart", tags=[_me, "production"]))

    Q.append(_q(_me, "easy",
        "What is a validation set? How is it different from a test set?",
        ["Why do you need both?", "What happens if you tune on the test set?"],
        ["Hyperparameter tuning", "Final evaluation", "Data leakage if test used for tuning", "Three-way split"]))

    Q.append(_q(_me, "medium",
        "What is stratified sampling and why is it important for model evaluation?",
        ["When is it critical?", "How does it affect cross-validation?"],
        ["Preserving class proportions", "Imbalanced datasets", "Representative splits", "StratifiedKFold"]))

    Q.append(_q(_me, "medium",
        "Explain the concept of a proper scoring rule. Why is Brier score useful?",
        ["How is Brier score different from log loss?", "What makes a scoring rule 'proper'?"],
        ["Incentivizes honest probabilities", "Brier = MSE of probabilities", "Quadratic vs logarithmic", "Calibration incentive"]))

    Q.append(_q(_me, "hard",
        "How do you evaluate a recommendation system? Accuracy metrics don't capture everything.",
        ["What's NDCG?", "How do you measure diversity and novelty?"],
        ["Ranking metrics", "NDCG and MAP", "Coverage and diversity", "Online vs offline evaluation"],
        company="Amazon", tags=[_me, "recommendation"]))

    Q.append(_q(_me, "medium",
        "What is early stopping? How does it relate to regularization?",
        ["How do you choose the patience parameter?", "Is early stopping always a good idea?"],
        ["Stop before overfitting", "Validation metric monitoring", "Implicit regularization", "Patience trade-off"]))

    Q.append(_q(_me, "medium",
        "What is the Matthews Correlation Coefficient? When is it better than F1?",
        ["How does it handle all four confusion matrix cells?", "When does F1 give misleading results?"],
        ["Balanced measure", "Uses all 4 cells", "Good for imbalance", "Range -1 to 1"]))

    # ==================================================================
    # DEEP LEARNING (30)
    # ==================================================================

    _dl = "deep_learning"

    Q.append(_q(_dl, "easy",
        "What is a neural network? Explain it to someone who only knows basic math.",
        ["What does a single neuron do?", "Why do we need multiple layers?"],
        ["Layers of connected nodes", "Weighted sum + activation", "Universal approximation", "Depth enables abstraction"]))

    Q.append(_q(_dl, "medium",
        "Explain backpropagation. How does the network learn from its mistakes?",
        ["What's the chain rule's role?", "What is vanishing gradient problem?"],
        ["Forward pass then backward", "Chain rule for gradients", "Weight update", "Gradient flow issues"]))

    Q.append(_q(_dl, "medium",
        "What are activation functions? Compare sigmoid, tanh, and ReLU.",
        ["Why is ReLU preferred in hidden layers?", "What's the dying ReLU problem?"],
        ["Non-linearity introduction", "Sigmoid saturation", "ReLU efficiency", "LeakyReLU fix"]))

    Q.append(_q(_dl, "medium",
        "Explain Convolutional Neural Networks. Why are they good for image data?",
        ["What does a convolutional filter learn?", "What's the role of pooling?"],
        ["Spatial hierarchy", "Filter/kernel operation", "Parameter sharing", "Translation invariance"]))

    Q.append(_q(_dl, "medium",
        "What is an RNN? Why was it designed and what problem does it solve?",
        ["What's the vanishing gradient problem in RNNs?", "How does LSTM solve it?"],
        ["Sequential data processing", "Hidden state", "Temporal dependencies", "Gradient issues"]))

    Q.append(_q(_dl, "hard",
        "Explain LSTM in detail. What are the gates and what does each one do?",
        ["How does the cell state flow through time?", "What's the difference between LSTM and GRU?"],
        ["Forget, input, output gates", "Cell state highway", "Gradient flow preservation", "GRU simplification"]))

    Q.append(_q(_dl, "hard",
        "Explain the Transformer architecture. What problem did it solve that RNNs couldn't?",
        ["What is self-attention?", "Why is 'Attention is All You Need' considered a landmark paper?"],
        ["Parallel processing", "Self-attention mechanism", "Positional encoding", "Scalability advantage"]))

    Q.append(_q(_dl, "hard",
        "What is the attention mechanism? Walk me through how it computes queries, keys, and values.",
        ["What's multi-head attention?", "Why use scaled dot-product attention?"],
        ["Q, K, V matrices", "Attention weights", "Softmax normalization", "Multi-head for different subspaces"]))

    Q.append(_q(_dl, "medium",
        "What is dropout? How does randomly removing neurons help with overfitting?",
        ["How does dropout relate to ensemble methods?", "What dropout rate do you typically start with?"],
        ["Random neuron deactivation", "Ensemble interpretation", "Training vs inference behavior", "0.2-0.5 typical"]))

    Q.append(_q(_dl, "medium",
        "What is batch normalization? Why does it help training?",
        ["Where do you place batch norm in a network?", "What happens during inference?"],
        ["Normalizing layer inputs", "Internal covariate shift", "Running statistics for inference", "Placement debate"]))

    Q.append(_q(_dl, "easy",
        "What is the difference between a deep learning model and a traditional ML model? When would you NOT use deep learning?",
        ["How much data does deep learning need?", "What about interpretability?"],
        ["Feature learning vs engineering", "Data requirements", "Compute cost", "Small data disadvantage"]))

    Q.append(_q(_dl, "medium",
        "Explain the concept of transfer learning. Why is it so powerful in practice?",
        ["How do you decide which layers to freeze?", "What's fine-tuning vs feature extraction?"],
        ["Pretrained knowledge reuse", "Freeze early layers", "Domain adaptation", "Reduced data needs"]))

    Q.append(_q(_dl, "hard",
        "What is the vanishing gradient problem? How do modern architectures solve it?",
        ["How do skip connections help?", "What's the role of careful initialization?"],
        ["Gradient shrinkage through layers", "Sigmoid problem", "ResNet skip connections", "He/Xavier initialization"]))

    Q.append(_q(_dl, "medium",
        "Explain the difference between SGD, Adam, and RMSprop optimizers.",
        ["Why is Adam the most popular default?", "When might SGD with momentum outperform Adam?"],
        ["Momentum concept", "Adaptive learning rates", "Adam combines momentum + RMSprop", "Generalization debate"]))

    Q.append(_q(_dl, "medium",
        "What is a loss function? Compare MSE, cross-entropy, and hinge loss.",
        ["How do you choose a loss function?", "Can you create custom loss functions?"],
        ["Objective to minimize", "Task-specific choices", "Regression vs classification", "Custom loss for business needs"]))

    Q.append(_q(_dl, "hard",
        "Explain how a GAN (Generative Adversarial Network) works.",
        ["What's mode collapse?", "How do you evaluate GAN quality?"],
        ["Generator vs discriminator", "Adversarial training", "Nash equilibrium", "FID score"]))

    Q.append(_q(_dl, "medium",
        "What is a learning rate schedule? Why don't you just use a fixed learning rate?",
        ["What's cosine annealing?", "What about warm-up?"],
        ["Decay strategies", "Too high vs too low", "Cyclical learning rates", "Warm-up for stability"]))

    Q.append(_q(_dl, "medium",
        "What are residual connections (skip connections)? Why did ResNet revolutionize deep learning?",
        ["How do skip connections help gradient flow?", "Can you use them in non-image architectures?"],
        ["Identity mapping", "Gradient highway", "Enabling very deep networks", "Used in transformers too"]))

    Q.append(_q(_dl, "hard",
        "What is an autoencoder? What are its variants and applications?",
        ["What's a variational autoencoder?", "How is it used for anomaly detection?"],
        ["Encoder-decoder structure", "Bottleneck representation", "VAE latent space", "Anomaly detection application"]))

    Q.append(_q(_dl, "easy",
        "What is an epoch, a batch, and an iteration in neural network training?",
        ["How do you choose batch size?", "What's the effect of batch size on training?"],
        ["One pass through data", "Subset of data", "Steps per epoch", "Batch size trade-offs"]))

    Q.append(_q(_dl, "medium",
        "Explain 1x1 convolutions. Why are they useful despite seeming trivial?",
        ["How do they reduce parameters in Inception networks?", "What's depthwise separable convolution?"],
        ["Channel-wise linear combination", "Dimensionality reduction", "Cross-channel interaction", "Computational efficiency"]))

    Q.append(_q(_dl, "hard",
        "What is the difference between seq2seq models and transformer-based models for machine translation?",
        ["Why did transformers replace RNN-based seq2seq?", "What's the role of cross-attention?"],
        ["Encoder-decoder architecture", "Attention bottleneck in seq2seq", "Parallel processing", "Cross-attention mechanism"]))

    Q.append(_q(_dl, "medium",
        "What is data augmentation? How does it help in deep learning for computer vision?",
        ["What augmentations would you use for medical images?", "What's Mixup and CutMix?"],
        ["Artificial data expansion", "Rotation, flip, crop", "Domain-specific augmentation", "Advanced techniques"]))

    Q.append(_q(_dl, "medium",
        "Explain weight initialization. Why can't you just initialize all weights to zero?",
        ["What's Xavier/Glorot initialization?", "What's He initialization?"],
        ["Symmetry breaking", "Gradient flow consideration", "Activation function matching", "Random initialization"]))

    Q.append(_q(_dl, "hard",
        "What is knowledge distillation? How do you compress a large model into a smaller one?",
        ["What's the temperature parameter?", "What are soft labels?"],
        ["Teacher-student framework", "Soft probability transfer", "Temperature scaling", "Model compression"],
        company="Amazon", tags=[_dl, "optimization"]))

    Q.append(_q(_dl, "medium",
        "What is the difference between padding types in CNNs: valid, same, and full?",
        ["How does padding affect output dimensions?", "When would you use each?"],
        ["No padding vs zero padding", "Output size formulas", "Edge information preservation", "Stride interaction"]))

    Q.append(_q(_dl, "hard",
        "Explain positional encoding in transformers. Why do we need it?",
        ["How do sinusoidal encodings work?", "What are learned positional embeddings?"],
        ["Sequence order information", "Sine/cosine functions", "Learned vs fixed", "Relative vs absolute position"]))

    Q.append(_q(_dl, "medium",
        "What is gradient clipping? When and why would you use it?",
        ["What's the difference between clipping by value and by norm?", "How does it relate to exploding gradients?"],
        ["Gradient magnitude limiting", "Exploding gradient prevention", "By value vs by norm", "RNN training stability"]))

    Q.append(_q(_dl, "hard",
        "What is self-supervised learning? How do models like BERT and GPT learn without labels?",
        ["What's masked language modeling?", "How is contrastive learning self-supervised?"],
        ["Pretext tasks", "MLM for BERT", "Autoregressive for GPT", "Contrastive methods"]))

    Q.append(_q(_dl, "medium",
        "What is the difference between model parallelism and data parallelism in distributed training?",
        ["When would you use each?", "What's gradient accumulation?"],
        ["Splitting model vs splitting data", "Communication overhead", "Large model necessity", "Gradient sync"]))

    # ==================================================================
    # NLP (25)
    # ==================================================================

    _nlp = "nlp"

    Q.append(_q(_nlp, "easy",
        "What is tokenization? Why is it the first step in most NLP pipelines?",
        ["What's the difference between word and subword tokenization?", "What's BPE?"],
        ["Breaking text into units", "Word vs subword vs character", "BPE algorithm", "Handling OOV words"]))

    Q.append(_q(_nlp, "medium",
        "Explain word embeddings. What problem did Word2Vec solve?",
        ["What's the difference between CBOW and Skip-gram?", "How do embeddings capture meaning?"],
        ["Dense vector representation", "Semantic relationships", "CBOW vs Skip-gram", "King - Man + Woman = Queen"]))

    Q.append(_q(_nlp, "medium",
        "What is TF-IDF? How does it improve over simple bag-of-words?",
        ["What does the IDF term capture?", "When would you use TF-IDF over embeddings?"],
        ["Term frequency-inverse document frequency", "Importance weighting", "Sparse representation", "Baseline method"]))

    Q.append(_q(_nlp, "hard",
        "Explain BERT. How does it differ from previous NLP models?",
        ["What's masked language modeling?", "What's the [CLS] token used for?"],
        ["Bidirectional context", "Masked LM pretraining", "NSP task", "Fine-tuning for downstream tasks"]))

    Q.append(_q(_nlp, "medium",
        "How would you build a sentiment analysis system? Walk me through the complete pipeline.",
        ["What features would you use?", "How do you handle sarcasm?"],
        ["Data collection", "Preprocessing", "Feature extraction", "Model selection", "Evaluation"],
        company="Flipkart", tags=[_nlp, "sentiment"]))

    Q.append(_q(_nlp, "medium",
        "What is text classification? Compare traditional ML approaches with deep learning approaches.",
        ["When would TF-IDF + logistic regression beat BERT?", "What about training time?"],
        ["Feature-based vs learned", "Data size requirements", "Compute trade-offs", "Transfer learning advantage"]))

    Q.append(_q(_nlp, "easy",
        "What is stemming vs lemmatization? When would you use each?",
        ["What's the Porter stemmer?", "Can stemming create non-words?"],
        ["Root form extraction", "Stemming is rule-based", "Lemmatization uses dictionary", "Accuracy trade-off"]))

    Q.append(_q(_nlp, "medium",
        "Explain the concept of word embeddings using Word2Vec. How does the Skip-gram model work?",
        ["What's negative sampling?", "How do you evaluate embedding quality?"],
        ["Context prediction", "Sliding window", "Negative sampling efficiency", "Analogy evaluation"]))

    Q.append(_q(_nlp, "hard",
        "What is the attention mechanism in NLP? How did it evolve from seq2seq to transformers?",
        ["What's Bahdanau attention?", "How does self-attention differ from cross-attention?"],
        ["Alignment model", "Context vector", "Self vs cross attention", "Evolution to transformers"]))

    Q.append(_q(_nlp, "medium",
        "How do you handle out-of-vocabulary words in NLP models?",
        ["What's subword tokenization?", "How does WordPiece work?"],
        ["UNK token", "Character-level fallback", "BPE/WordPiece", "Fasttext subword embeddings"]))

    Q.append(_q(_nlp, "medium",
        "What is Named Entity Recognition? How would you build an NER system?",
        ["What's the BIO tagging scheme?", "How does SpaCy handle NER?"],
        ["Entity identification", "BIO/BILOU schemes", "CRF vs neural approaches", "Pre-trained models"]))

    Q.append(_q(_nlp, "hard",
        "Explain the GPT architecture. How is it different from BERT?",
        ["What's autoregressive generation?", "Why can't you use GPT for bidirectional understanding tasks?"],
        ["Unidirectional transformer", "Autoregressive pretraining", "Generative vs understanding", "Left-to-right attention"]))

    Q.append(_q(_nlp, "medium",
        "What is sequence labeling? Give examples of NLP tasks that use it.",
        ["What's the CRF layer for?", "How does it differ from classification?"],
        ["Per-token prediction", "POS tagging, NER", "CRF for dependencies", "Viterbi decoding"]))

    Q.append(_q(_nlp, "easy",
        "What is stop word removal? Is it always a good idea?",
        ["When should you keep stop words?", "How does it affect TF-IDF?"],
        ["Common word filtering", "Sentiment context loss", "Task-dependent decision", "Impact on representations"]))

    Q.append(_q(_nlp, "medium",
        "How would you build a text summarization system? Compare extractive and abstractive approaches.",
        ["What models are used for abstractive summarization?", "How do you evaluate summaries?"],
        ["Extractive selects sentences", "Abstractive generates new text", "ROUGE metrics", "Factual consistency"]))

    Q.append(_q(_nlp, "hard",
        "What is the difference between contextual and static word embeddings?",
        ["How does BERT create contextual embeddings?", "Why does 'bank' need context?"],
        ["Word2Vec static", "ELMo/BERT contextual", "Polysemy handling", "Layer-wise representations"]))

    Q.append(_q(_nlp, "medium",
        "What are language models? Explain the difference between masked and autoregressive language models.",
        ["Which type is BERT? Which is GPT?", "How are they used for different downstream tasks?"],
        ["Probability of text", "MLM vs causal LM", "BERT bidirectional", "GPT left-to-right"]))

    Q.append(_q(_nlp, "medium",
        "How do you evaluate NLP models? What are BLEU, ROUGE, and perplexity?",
        ["When would you use each?", "What are the limitations of BLEU?"],
        ["BLEU for translation", "ROUGE for summarization", "Perplexity for LM", "N-gram overlap limitations"]))

    Q.append(_q(_nlp, "hard",
        "What is fine-tuning a pre-trained language model? Walk me through the process for a text classification task.",
        ["How do you choose the learning rate for fine-tuning?", "What's catastrophic forgetting?"],
        ["Pretrain then adapt", "Lower learning rate", "Task-specific head", "Catastrophic forgetting mitigation"]))

    Q.append(_q(_nlp, "medium",
        "What is topic modeling? Explain LDA (Latent Dirichlet Allocation).",
        ["How do you choose the number of topics?", "What's the difference between LDA and NMF?"],
        ["Document-topic distribution", "Topic-word distribution", "Generative process", "Coherence evaluation"],
        company="Mu Sigma", tags=[_nlp, "topic_modeling"]))

    Q.append(_q(_nlp, "easy",
        "What is text preprocessing? Walk me through the steps you would take for a typical NLP task.",
        ["Do you always need all these steps?", "How does preprocessing differ for deep learning vs traditional ML?"],
        ["Lowercasing, punctuation", "Tokenization", "Stopwords", "Stemming/lemmatization", "Deep learning needs less"]))

    Q.append(_q(_nlp, "medium",
        "How would you build a chatbot? What are the key components?",
        ["What's the difference between retrieval-based and generative chatbots?", "How do you handle context?"],
        ["Intent detection", "Entity extraction", "Response generation", "Context management"]))

    Q.append(_q(_nlp, "hard",
        "What is prompt engineering? How do you get the best results from large language models?",
        ["What's few-shot vs zero-shot prompting?", "What's chain-of-thought prompting?"],
        ["Instruction design", "Examples in prompt", "Chain-of-thought", "Prompt sensitivity"]))

    Q.append(_q(_nlp, "medium",
        "What is text similarity? Compare cosine similarity, Jaccard similarity, and semantic similarity.",
        ["When would cosine similarity fail?", "How do you compute semantic similarity with embeddings?"],
        ["Vector-based vs set-based", "Cosine on embeddings", "Jaccard for overlap", "Sentence transformers"]))

    Q.append(_q(_nlp, "medium",
        "How do you handle multilingual NLP? What challenges arise?",
        ["What's mBERT?", "How do you handle languages with no training data?"],
        ["Multilingual models", "Cross-lingual transfer", "Script differences", "Zero-shot cross-lingual"]))

    # ==================================================================
    # PYTHON FOR DATA SCIENCE (25)
    # ==================================================================

    _py = "python_for_ds"

    Q.append(_q(_py, "easy",
        "What is a Pandas DataFrame? How is it different from a Python dictionary or a NumPy array?",
        ["When would you use each?", "How does Pandas handle missing values?"],
        ["Tabular data structure", "Labeled axes", "Mixed types", "NaN handling"]))

    Q.append(_q(_py, "medium",
        "Explain the difference between .loc and .iloc in Pandas. Give examples of each.",
        ["What happens with slicing?", "How do you select both rows and columns?"],
        ["Label-based vs position-based", "Inclusive vs exclusive", "Boolean indexing", "Multi-axis selection"]))

    Q.append(_q(_py, "medium",
        "How do you handle missing values in Pandas? Walk me through different strategies.",
        ["What's the difference between dropna and fillna?", "How do you detect missing values?"],
        ["isnull/isna", "dropna with thresholds", "fillna strategies", "Interpolation"]))

    Q.append(_q(_py, "medium",
        "Explain the groupby operation in Pandas. How would you compute the average sales per region per month?",
        ["What's the agg function?", "How do you apply multiple aggregations?"],
        ["Split-apply-combine", "Aggregation functions", "Multi-level groupby", "Transform vs aggregate"]))

    Q.append(_q(_py, "easy",
        "What is NumPy? Why is it faster than regular Python lists for numerical computation?",
        ["What's broadcasting?", "How does vectorization work?"],
        ["Contiguous memory", "C implementation", "Vectorized operations", "Broadcasting rules"]))

    Q.append(_q(_py, "medium",
        "How do you merge/join DataFrames in Pandas? Compare merge, join, and concat.",
        ["What are the different join types?", "How do you handle duplicate column names?"],
        ["Inner/outer/left/right", "On keys vs index", "Concat for stacking", "Suffixes for duplicates"]))

    Q.append(_q(_py, "medium",
        "How would you use scikit-learn to build a complete ML pipeline?",
        ["What's the Pipeline class?", "How does it prevent data leakage?"],
        ["Preprocessing + model", "Fit_transform vs transform", "Column transformer", "Leakage prevention"]))

    Q.append(_q(_py, "easy",
        "How do you create basic visualizations using Matplotlib and Seaborn? When would you use each?",
        ["What's the difference between plt.plot and ax.plot?", "What chart type for what data?"],
        ["Matplotlib for customization", "Seaborn for statistical", "Figure vs axes", "Chart selection"]))

    Q.append(_q(_py, "medium",
        "What is the apply function in Pandas? When should you use it vs vectorized operations?",
        ["Why is apply slow?", "What's the alternative using np.where or np.select?"],
        ["Row/column-wise function", "Vectorization preferred", "Performance implications", "Alternatives"]))

    Q.append(_q(_py, "hard",
        "How do you optimize Pandas operations for large datasets that don't fit in memory?",
        ["What's chunking?", "When would you switch to Dask or Polars?"],
        ["Chunked reading", "Data types optimization", "Dask for parallel", "Memory profiling"],
        company="Mu Sigma", tags=[_py, "performance"]))

    Q.append(_q(_py, "medium",
        "Explain the train_test_split function in scikit-learn. What parameters are important?",
        ["What's stratify?", "What's the random_state parameter?"],
        ["Test size", "Stratification", "Reproducibility", "Shuffle parameter"]))

    Q.append(_q(_py, "easy",
        "What is a Pandas Series? How does it relate to a DataFrame?",
        ["How do you create a Series?", "Can you do arithmetic with Series?"],
        ["Single column", "Index-aligned operations", "DataFrame is dict of Series", "Vectorized arithmetic"]))

    Q.append(_q(_py, "medium",
        "How do you use cross_val_score in scikit-learn? What does it return?",
        ["How do you choose the scoring metric?", "What's the difference between cross_val_score and cross_validate?"],
        ["K-fold evaluation", "Scoring parameter", "Returns array of scores", "cross_validate for multiple metrics"]))

    Q.append(_q(_py, "medium",
        "Explain how you would perform feature engineering in Pandas. Give me a concrete example with dates and categories.",
        ["How do you extract date components?", "How do you do one-hot encoding?"],
        ["dt accessor", "pd.get_dummies", "Cut/qcut for binning", "String methods"]))

    Q.append(_q(_py, "hard",
        "How do you write efficient Pandas code? Give me 5 common performance anti-patterns.",
        ["What's the problem with iterrows?", "How does memory usage change with data types?"],
        ["Avoid loops", "Vectorize operations", "Downcast dtypes", "Categorical for strings", "Chain operations"]))

    Q.append(_q(_py, "medium",
        "How do you create a pivot table in Pandas? When would you use pivot_table vs crosstab?",
        ["What aggregation functions can you use?", "How do you handle multiple values?"],
        ["Reshaping data", "Aggregation in pivot", "Crosstab for frequency", "Multi-level pivot"]))

    Q.append(_q(_py, "easy",
        "How do you read and write CSV, Excel, and JSON files in Pandas?",
        ["What parameters do you commonly set for read_csv?", "How do you handle encoding issues?"],
        ["read_csv/to_csv", "read_excel", "read_json", "Encoding, separator, header options"]))

    Q.append(_q(_py, "medium",
        "Explain NumPy broadcasting. What are the rules?",
        ["Give an example where broadcasting works.", "When does broadcasting fail?"],
        ["Dimension alignment from right", "Size 1 stretches", "Shape compatibility", "Failure cases"]))

    Q.append(_q(_py, "medium",
        "How do you use matplotlib subplots? Create a 2x2 grid of different chart types.",
        ["What's the difference between plt.subplots and plt.subplot?", "How do you share axes?"],
        ["fig, axes pattern", "Sharing axes", "Layout customization", "Tight layout"]))

    Q.append(_q(_py, "hard",
        "How do you implement a custom transformer in scikit-learn that fits into a Pipeline?",
        ["What methods must it have?", "When would you need a custom transformer?"],
        ["BaseEstimator + TransformerMixin", "fit and transform methods", "Feature engineering custom logic", "Pipeline integration"]))

    Q.append(_q(_py, "medium",
        "What is the difference between deep copy and shallow copy in Pandas?",
        ["When does modifying a slice modify the original?", "What's the SettingWithCopyWarning?"],
        ["Reference vs copy", "View vs copy", "Copy method", "Chained indexing warning"]))

    Q.append(_q(_py, "easy",
        "How do you sort a DataFrame by multiple columns in Pandas?",
        ["What's ascending parameter?", "How do you sort by index?"],
        ["sort_values", "Multiple columns", "Ascending/descending per column", "sort_index"]))

    Q.append(_q(_py, "medium",
        "How do you handle categorical data in Pandas? What's the Categorical dtype?",
        ["How does it save memory?", "How does ordering work for ordinal categories?"],
        ["Category dtype", "Memory efficiency", "Ordered categories", "CategoricalDtype"]))

    Q.append(_q(_py, "medium",
        "What is method chaining in Pandas? Show me a complex data transformation using method chaining.",
        ["What's the pipe method?", "When does chaining become unreadable?"],
        ["Fluent interface", "Assign for new columns", "Pipe for custom functions", "Readability trade-off"]))

    Q.append(_q(_py, "hard",
        "How do you profile and optimize a slow Pandas/NumPy workflow?",
        ["What tools do you use for profiling?", "How do you decide between Pandas optimization and switching to a different tool?"],
        ["line_profiler", "Memory profiler", "Bottleneck identification", "Vectorization", "Cython/Numba for critical paths"]))

    # ==================================================================
    # SQL FOR DATA SCIENCE (20)
    # ==================================================================

    _sql = "sql_for_ds"

    Q.append(_q(_sql, "easy",
        "Write a SQL query to find the top 5 customers by total order value. Walk me through your approach.",
        ["How would you handle ties?", "What if you need the top 5 per region?"],
        ["JOIN orders and customers", "GROUP BY + SUM", "ORDER BY DESC LIMIT 5", "Ties with RANK"]))

    Q.append(_q(_sql, "medium",
        "Explain window functions in SQL. How are they different from GROUP BY?",
        ["Give me an example using ROW_NUMBER, RANK, and DENSE_RANK.", "What's the PARTITION BY clause?"],
        ["Per-row calculation", "No row collapse", "OVER clause", "Partition and order"]))

    Q.append(_q(_sql, "medium",
        "How would you calculate a running total and a 7-day moving average in SQL?",
        ["What window frame do you use?", "How do you handle the first 6 days?"],
        ["SUM OVER with ROWS BETWEEN", "Moving average with PRECEDING", "UNBOUNDED PRECEDING for running", "Edge cases"]))

    Q.append(_q(_sql, "medium",
        "Write a query to find users who made a purchase in January but not in February.",
        ["What join type would you use?", "Can you do it without a subquery?"],
        ["LEFT JOIN with NULL check", "NOT EXISTS approach", "EXCEPT/MINUS", "Performance comparison"]))

    Q.append(_q(_sql, "hard",
        "How would you find the second highest salary in each department? Give me at least 2 approaches.",
        ["What if there are ties?", "Which approach is most efficient?"],
        ["DENSE_RANK approach", "Subquery approach", "LIMIT OFFSET", "Handling ties"],
        company="Amazon", tags=[_sql, "window_functions"]))

    Q.append(_q(_sql, "medium",
        "Explain the difference between INNER JOIN, LEFT JOIN, RIGHT JOIN, and FULL OUTER JOIN with examples.",
        ["When would you use each?", "What about CROSS JOIN?"],
        ["Matching rows only", "All from left", "All from right", "All from both", "Cartesian product"]))

    Q.append(_q(_sql, "medium",
        "What is a CTE (Common Table Expression)? When would you use it over a subquery?",
        ["Can CTEs be recursive?", "How do they affect performance?"],
        ["WITH clause", "Readability improvement", "Recursive CTE for hierarchies", "Materialization behavior"]))

    Q.append(_q(_sql, "hard",
        "Write a query to calculate month-over-month growth rate for each product category.",
        ["How do you handle months with zero sales?", "What's the LAG function?"],
        ["LAG for previous month", "Growth rate formula", "COALESCE for nulls", "Percentage calculation"],
        company="Flipkart", tags=[_sql, "analytics"]))

    Q.append(_q(_sql, "easy",
        "What is the difference between WHERE and HAVING in SQL?",
        ["Can you use aggregates in WHERE?", "What's the order of execution in SQL?"],
        ["Row filter vs group filter", "WHERE before GROUP BY", "HAVING after GROUP BY", "Aggregate functions"]))

    Q.append(_q(_sql, "medium",
        "How would you detect duplicate records in a table? How would you remove them keeping one copy?",
        ["What's ROW_NUMBER approach for deduplication?", "How do you define 'duplicate'?"],
        ["GROUP BY HAVING COUNT > 1", "ROW_NUMBER for deletion", "CTE approach", "Definition of duplicate"]))

    Q.append(_q(_sql, "medium",
        "What are indexes in SQL? How do they speed up queries and when can they hurt?",
        ["What's a composite index?", "How do you decide which columns to index?"],
        ["B-tree structure", "Query optimization", "Write overhead", "Selectivity consideration"]))

    Q.append(_q(_sql, "hard",
        "Write a SQL query to find users whose spending increased for 3 consecutive months.",
        ["How do you detect consecutive patterns in SQL?", "What window functions help here?"],
        ["LAG/LEAD comparison", "Row numbering gaps", "Self-join approach", "Consecutive sequence detection"],
        company="Goldman Sachs", tags=[_sql, "analytics"]))

    Q.append(_q(_sql, "medium",
        "What is a correlated subquery? How does it differ from a regular subquery?",
        ["Give an example of each.", "Which is typically faster?"],
        ["References outer query", "Row-by-row execution", "Performance implications", "Rewrite as JOIN"]))

    Q.append(_q(_sql, "easy",
        "Explain GROUP BY with a practical example. What aggregate functions do you commonly use?",
        ["Can you GROUP BY multiple columns?", "What happens to non-aggregated columns?"],
        ["Grouping rows", "SUM, COUNT, AVG, MIN, MAX", "Multiple column grouping", "All columns must be aggregated or grouped"]))

    Q.append(_q(_sql, "medium",
        "How do you handle NULL values in SQL? What gotchas should you watch for?",
        ["What does NULL = NULL return?", "How does NULL affect aggregations?"],
        ["IS NULL not = NULL", "COALESCE function", "NULL in aggregations", "Three-valued logic"]))

    Q.append(_q(_sql, "hard",
        "Write a query to calculate the median salary. SQL doesn't have a built-in MEDIAN function in most databases.",
        ["How would you do it in MySQL vs PostgreSQL?", "What about using PERCENTILE_CONT?"],
        ["ROW_NUMBER approach", "PERCENTILE_CONT where available", "Self-join median", "Even vs odd row counts"]))

    Q.append(_q(_sql, "medium",
        "What is a self-join? Give me a real-world example where it's necessary.",
        ["How do you find employees who earn more than their manager?", "What's the performance implication?"],
        ["Joining table to itself", "Manager-employee hierarchy", "Alias necessity", "Alternative approaches"]))

    Q.append(_q(_sql, "medium",
        "How would you optimize a slow SQL query? Walk me through your debugging process.",
        ["What does EXPLAIN show you?", "What's a full table scan?"],
        ["EXPLAIN plan", "Index usage", "Query rewriting", "Avoiding SELECT *", "Join order"]))

    Q.append(_q(_sql, "hard",
        "Write a query to perform cohort analysis -- group users by signup month and track their retention over subsequent months.",
        ["How do you define retention?", "How do you pivot the results?"],
        ["Cohort definition", "Date arithmetic", "COUNT DISTINCT", "Pivot or conditional aggregation"],
        company="Flipkart", tags=[_sql, "analytics"]))

    Q.append(_q(_sql, "medium",
        "What is the difference between UNION and UNION ALL? When would you use each?",
        ["What's the performance difference?", "What requirements must the queries meet?"],
        ["Deduplication in UNION", "UNION ALL faster", "Column compatibility", "Use cases"]))

    # ==================================================================
    # ML SYSTEM DESIGN (20)
    # ==================================================================

    _mls = "ml_system_design"

    Q.append(_q(_mls, "medium",
        "Walk me through how you would design an ML pipeline from raw data to production model.",
        ["How do you handle data versioning?", "What's CI/CD for ML?"],
        ["Data ingestion", "Feature engineering", "Training", "Validation", "Deployment", "Monitoring"]))

    Q.append(_q(_mls, "hard",
        "What is a feature store? Why do companies like Uber and Netflix build them?",
        ["What problems does it solve?", "How does it ensure consistency between training and serving?"],
        ["Feature reuse", "Online/offline consistency", "Point-in-time correctness", "Team collaboration"],
        company="Amazon", tags=[_mls, "infrastructure"]))

    Q.append(_q(_mls, "medium",
        "How do you serve ML models in production? Compare batch inference vs real-time inference.",
        ["When would you use each?", "What about edge deployment?"],
        ["Latency requirements", "Batch for recommendations", "Real-time for fraud", "Cost trade-offs"]))

    Q.append(_q(_mls, "hard",
        "How do you monitor an ML model in production? What metrics do you track beyond accuracy?",
        ["How do you detect data drift?", "What triggers model retraining?"],
        ["Prediction drift", "Feature drift", "Latency monitoring", "Alerting thresholds", "Retraining strategy"],
        company="Flipkart", tags=[_mls, "monitoring"]))

    Q.append(_q(_mls, "medium",
        "Design a recommendation system for an e-commerce platform. What approach would you take?",
        ["How do you handle the cold start problem?", "What's collaborative vs content-based filtering?"],
        ["Collaborative filtering", "Content-based", "Hybrid approach", "Cold start solutions"],
        company="Amazon", tags=[_mls, "recommendation"]))

    Q.append(_q(_mls, "hard",
        "How do you design an A/B testing platform at scale? What are the challenges?",
        ["How do you handle network effects?", "What about multiple concurrent experiments?"],
        ["Randomization", "Sample size calculation", "Interaction effects", "Sequential testing"],
        company="Flipkart", tags=[_mls, "ab_testing"]))

    Q.append(_q(_mls, "medium",
        "What is model versioning? How do you manage multiple model versions in production?",
        ["What tools exist for model versioning?", "How do you do A/B testing between model versions?"],
        ["MLflow/DVC", "Model registry", "Canary deployments", "Rollback capability"]))

    Q.append(_q(_mls, "medium",
        "How do you handle data quality issues in an ML pipeline?",
        ["What data validation checks would you add?", "What's Great Expectations?"],
        ["Schema validation", "Distribution checks", "Missing value monitoring", "Automated alerts"]))

    Q.append(_q(_mls, "hard",
        "Design a fraud detection system. How would you handle the extreme class imbalance and real-time requirements?",
        ["How do you reduce false positives?", "What's the feedback loop for improving the model?"],
        ["Real-time scoring", "Feature engineering from transactions", "Ensemble approach", "Human-in-the-loop"],
        company="Goldman Sachs", tags=[_mls, "fraud"]))

    Q.append(_q(_mls, "medium",
        "What is MLOps? How does it differ from DevOps?",
        ["What are the key components of an MLOps platform?", "What tools would you use?"],
        ["Model lifecycle management", "Data-centric differences", "Experiment tracking", "Model monitoring"]))

    Q.append(_q(_mls, "medium",
        "How do you handle model retraining? What strategies exist for deciding when to retrain?",
        ["What's scheduled vs triggered retraining?", "How do you validate before deploying a retrained model?"],
        ["Performance degradation trigger", "Scheduled retraining", "Champion-challenger", "Validation pipeline"]))

    Q.append(_q(_mls, "hard",
        "Design a search ranking system. How would you combine relevance, personalization, and business rules?",
        ["What features would you use?", "How do you evaluate search quality?"],
        ["Learning to rank", "Feature engineering", "NDCG evaluation", "Multi-objective optimization"],
        company="Flipkart", tags=[_mls, "search"]))

    Q.append(_q(_mls, "medium",
        "What is data drift vs concept drift? How do you detect each in production?",
        ["What statistical tests can detect drift?", "How do you handle it when detected?"],
        ["Input distribution change", "Target relationship change", "KS test, PSI", "Retraining triggers"]))

    Q.append(_q(_mls, "medium",
        "How do you design an ML system for high availability? What happens when the model service goes down?",
        ["What's a fallback strategy?", "How do you handle latency spikes?"],
        ["Redundancy", "Load balancing", "Fallback models", "Caching", "Graceful degradation"]))

    Q.append(_q(_mls, "hard",
        "Design a real-time pricing system for a ride-sharing platform. What ML components are needed?",
        ["How do you handle surge pricing fairly?", "What's the feedback loop?"],
        ["Demand prediction", "Supply estimation", "Dynamic optimization", "Fairness constraints"],
        company="Flipkart", tags=[_mls, "pricing"]))

    Q.append(_q(_mls, "medium",
        "What is experiment tracking? Why is it essential for ML teams?",
        ["What do you log in each experiment?", "What tools exist?"],
        ["Hyperparameters", "Metrics", "Artifacts", "Reproducibility", "MLflow/W&B"]))

    Q.append(_q(_mls, "medium",
        "How do you handle personally identifiable information (PII) in ML pipelines?",
        ["What anonymization techniques exist?", "How does GDPR/DPDP affect ML?"],
        ["Data masking", "Differential privacy", "Federated learning", "Compliance requirements"]))

    Q.append(_q(_mls, "hard",
        "Design an ML system for content moderation at scale. How do you handle the speed vs accuracy trade-off?",
        ["How do you handle adversarial content?", "What about cultural context?"],
        ["Cascading models", "Fast filter + accurate classifier", "Human review loop", "Adversarial robustness"],
        company="Amazon", tags=[_mls, "content"]))

    Q.append(_q(_mls, "medium",
        "What are shadow deployments for ML models? When would you use them?",
        ["How do they compare to canary deployments?", "What do you measure during shadow mode?"],
        ["Parallel prediction without serving", "Risk reduction", "Comparison metrics", "Resource overhead"]))

    Q.append(_q(_mls, "medium",
        "How do you estimate the infrastructure cost for an ML system? What factors matter?",
        ["How do you optimize compute costs?", "What's spot vs on-demand for training?"],
        ["Training compute", "Serving compute", "Storage", "Spot instances for training", "Model optimization"]))

    return Q
