from django.db import migrations


def seed_flashcards(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Course = apps.get_model('study', 'Course')
    Topic = apps.get_model('study', 'Topic')
    Flashcard = apps.get_model('study', 'Flashcard')

    system_user = User.objects.filter(username='system').first()
    if not system_user:
        return
    course = Course.objects.filter(name='Data Analytics', created_by=system_user).first()
    if not course:
        return
    topics = {t.name: t for t in Topic.objects.filter(course=course)}

    def add_cards(topic_name, cards):
        topic = topics.get(topic_name)
        if not topic or Flashcard.objects.filter(topic=topic).exists():
            return
        for card in cards:
            Flashcard.objects.create(topic=topic, **card)

    # ------------------------------------------------------------------ #
    # 001A — Descriptive Statistics & Visualisation
    # ------------------------------------------------------------------ #
    add_cards('Descriptive Statistics & Visualisation', [
        {'question': 'Difference between population and sample.',
         'answer': 'Population: entire group of interest. Sample: subset drawn from the population. Statistics are computed on samples; parameters describe populations.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Mean, median, and mode: definitions.',
         'answer': 'Mean: sum of values / count (x̄ = Σxᵢ/n). Median: middle value when sorted. Mode: most frequent value.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Sample variance formula.',
         'answer': 's² = Σ(xᵢ − x̄)²/(n − 1). Uses n−1 (Bessel\'s correction) for unbiased estimation of population variance.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Standard deviation vs variance.',
         'answer': 'Standard deviation s = √s². Same units as data. Variance s² is in squared units. Both measure spread around the mean.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Interquartile range (IQR).',
         'answer': 'IQR = Q3 − Q1 (75th − 25th percentile). Robust measure of spread; used to identify outliers (beyond Q1−1.5·IQR or Q3+1.5·IQR).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'When to use a histogram vs a box plot.',
         'answer': 'Histogram: shows distribution shape (modality, skewness). Box plot: compact summary of median, quartiles, and outliers; good for comparing groups.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is a skewed distribution?',
         'answer': 'Right-skewed (positive): long tail to the right; mean > median. Left-skewed (negative): long tail to the left; mean < median.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Pearson correlation coefficient r: range and interpretation.',
         'answer': 'r ∈ [−1, 1]. r = 1: perfect positive linear. r = −1: perfect negative linear. r = 0: no linear relationship. Computed as Cov(X,Y)/(s_X s_Y).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 002A — Inferential Statistics
    # ------------------------------------------------------------------ #
    add_cards('Inferential Statistics', [
        {'question': 'Null hypothesis (H₀) vs alternative hypothesis (H₁).',
         'answer': 'H₀: "no effect" or status quo (e.g. μ = μ₀). H₁: what we want to show (e.g. μ ≠ μ₀). We test whether data provides evidence against H₀.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'p-value definition.',
         'answer': 'Probability of observing a result at least as extreme as the sample, assuming H₀ is true. Small p-value (< α) → reject H₀.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Type I error vs Type II error.',
         'answer': 'Type I (false positive): reject H₀ when it is true. Probability = α (significance level). Type II (false negative): fail to reject H₀ when it is false. Probability = β.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': '95% confidence interval for population mean (large sample).',
         'answer': 'x̄ ± 1.96 · (s/√n). Contains the true mean with 95% confidence across repeated sampling.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Central Limit Theorem.',
         'answer': 'The sample mean x̄ of n independent samples from any population with mean μ and variance σ² is approximately normally distributed for large n: x̄ ~ N(μ, σ²/n).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'One-sample t-test: when to use it?',
         'answer': 'Testing if population mean equals a specified value μ₀ when σ is unknown and sample is small. Test statistic: t = (x̄ − μ₀)/(s/√n), with n−1 degrees of freedom.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Chi-squared test: what does it test?',
         'answer': 'Goodness of fit: do observed frequencies match expected? Or independence: are two categorical variables independent? Test statistic: χ² = Σ(O − E)²/E.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 003A — Data Preprocessing
    # ------------------------------------------------------------------ #
    add_cards('Data Preprocessing', [
        {'question': 'What is missing data imputation?',
         'answer': 'Replacing missing values with estimated ones. Methods: mean/median imputation, mode (categorical), k-NN imputation, or model-based. Avoid deleting rows unless missingness is minimal and random.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Z-score (standardisation) formula.',
         'answer': 'z = (x − μ)/σ. Transforms feature to mean 0, std 1. Required for algorithms sensitive to scale (SVM, k-NN, PCA).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Min-max normalisation formula.',
         'answer': 'x_norm = (x − x_min)/(x_max − x_min). Scales to [0, 1]. Sensitive to outliers.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'One-hot encoding: what is it and when to use it?',
         'answer': 'Converts a categorical variable with k levels into k binary (0/1) columns. Use for nominal categories with no ordering (e.g. city name, colour).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Train/validation/test split: purpose of each.',
         'answer': 'Train: fit model parameters. Validation: tune hyperparameters and select model. Test: final unbiased performance estimate — use only once.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is data leakage?',
         'answer': 'When information from the test set leaks into training (e.g. fitting a scaler on all data before splitting). Causes overly optimistic results that don\'t generalise.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is an outlier detection method?',
         'answer': 'IQR rule: outlier if x < Q1−1.5·IQR or x > Q3+1.5·IQR. Z-score: |z| > 3. Isolation Forest or DBSCAN for multivariate outliers.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 004A — Clustering Methods
    # ------------------------------------------------------------------ #
    add_cards('Clustering Methods', [
        {'question': 'k-Means algorithm: steps.',
         'answer': '1. Choose k cluster centres randomly. 2. Assign each point to nearest centre. 3. Update centres as mean of assigned points. 4. Repeat until convergence (centres stop moving).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'How do you choose k in k-Means? (Elbow method)',
         'answer': 'Plot within-cluster sum of squares (WCSS) vs k. The "elbow" point where the rate of decrease slows is the suggested k.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Euclidean distance formula between points p and q in d dimensions.',
         'answer': 'd = √(Σᵢ(pᵢ − qᵢ)²). Most common distance metric for k-Means.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'DBSCAN: key parameters and their meaning.',
         'answer': 'ε (eps): neighbourhood radius. MinPts: minimum points in ε-neighbourhood to form a core point. Points not reachable from any core point are labelled noise.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Silhouette score: range and interpretation.',
         'answer': 'Range [−1, 1]. Close to 1: well-clustered. Close to 0: on boundary. Negative: possibly mis-clustered. Average silhouette over all points measures cluster quality.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Hierarchical clustering: agglomerative vs divisive.',
         'answer': 'Agglomerative (bottom-up): start with each point as its own cluster, merge closest pairs. Divisive (top-down): start with one cluster, split. Result displayed as dendrogram.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
    ])

    # ------------------------------------------------------------------ #
    # 005A — Frequent Pattern Mining
    # ------------------------------------------------------------------ #
    add_cards('Frequent Pattern Mining', [
        {'question': 'Support of an itemset {A, B}.',
         'answer': 'support({A,B}) = (number of transactions containing both A and B) / (total transactions). Measures how often the pattern occurs.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Confidence of association rule A → B.',
         'answer': 'confidence(A→B) = support({A,B}) / support({A}). Probability that B is bought given A is bought.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Lift of association rule A → B.',
         'answer': 'lift(A→B) = confidence(A→B) / support(B). Lift > 1: positive association. Lift = 1: independent. Lift < 1: negative association.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Apriori principle.',
         'answer': 'Any subset of a frequent itemset is also frequent. Equivalently: any superset of an infrequent itemset is infrequent. Allows pruning of candidate sets.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'FP-Growth vs Apriori: key difference.',
         'answer': 'Apriori generates and tests candidates explicitly (multiple database scans). FP-Growth compresses the database into an FP-tree and mines without candidate generation — much faster on large datasets.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
    ])

    # ------------------------------------------------------------------ #
    # 006A — Regression Analysis
    # ------------------------------------------------------------------ #
    add_cards('Regression Analysis', [
        {'question': 'Simple linear regression model.',
         'answer': 'ŷ = β₀ + β₁x + ε. β₀ = intercept, β₁ = slope. ε = random error. Fitted by minimising sum of squared residuals (OLS).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'OLS formula for slope β₁.',
         'answer': 'β̂₁ = Σ(xᵢ − x̄)(yᵢ − ȳ) / Σ(xᵢ − x̄)² = Cov(X,Y)/Var(X).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'R² (coefficient of determination): definition and range.',
         'answer': 'R² = 1 − SS_res/SS_tot. Range [0, 1]. Proportion of variance in y explained by the model. R² = 0: model explains nothing; R² = 1: perfect fit.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Assumptions of OLS regression (LINE).',
         'answer': 'Linearity, Independence (of errors), Normality (of errors), Equal variance (homoscedasticity). Violations bias estimates or invalidate inference.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is multicollinearity and how is it detected?',
         'answer': 'High correlation among predictors inflates standard errors of coefficients. Detected via Variance Inflation Factor (VIF). VIF > 10 is concerning.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Ridge vs Lasso regularisation.',
         'answer': 'Ridge (L2): adds λΣβⱼ² to loss — shrinks all coefficients, never zeros. Lasso (L1): adds λΣ|βⱼ| — can zero out coefficients (feature selection). Elastic Net: combination of both.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 007A — Classification Algorithms
    # ------------------------------------------------------------------ #
    add_cards('Classification Algorithms', [
        {'question': 'Logistic regression: output and decision boundary.',
         'answer': 'P(y=1|x) = σ(wᵀx + b) = 1/(1 + e^(−(wᵀx+b))). Sigmoid maps to (0,1). Decision: predict 1 if P > 0.5, else 0.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Precision and Recall: formulas and trade-off.',
         'answer': 'Precision = TP/(TP+FP). Recall = TP/(TP+FN). High precision = few false alarms. High recall = few misses. F1 = 2·Prec·Rec/(Prec+Rec) balances both.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Decision tree: splitting criterion.',
         'answer': 'Gini impurity: 1 − Σpᵢ². Information gain: H(parent) − Σ(wᵢ H(childᵢ)) where H is entropy. Split that maximises gain is chosen.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'k-Nearest Neighbours (k-NN): classification rule.',
         'answer': 'Find k training points closest to query point. Majority vote determines class. k=1: fits training perfectly (high variance). Larger k: smoother boundary (more bias).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Random Forest: how does it differ from a single decision tree?',
         'answer': 'Ensemble of many trees trained on bootstrap samples (bagging) with random feature subsets. Majority vote reduces variance and overfitting compared to a single tree.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is cross-validation and why is it used?',
         'answer': 'k-Fold CV: split data into k folds; train on k−1 folds, test on remaining. Repeat k times. Average test score gives less biased performance estimate than a single train/test split.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
    ])

    # ------------------------------------------------------------------ #
    # 008A — Big Data Concepts
    # ------------------------------------------------------------------ #
    add_cards('Big Data Concepts', [
        {'question': 'The 3 Vs of Big Data.',
         'answer': 'Volume (huge amount of data), Velocity (generated at high speed, near real-time), Variety (structured, semi-structured, unstructured). Some add Veracity and Value.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'MapReduce paradigm: Map and Reduce phases.',
         'answer': 'Map: apply a function to each input record, emit (key, value) pairs. Reduce: aggregate all values sharing the same key. Enables distributed processing.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is Apache Hadoop?',
         'answer': 'Open-source framework for distributed storage (HDFS) and processing (MapReduce or Spark) of large datasets across commodity hardware clusters.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Apache Spark vs Hadoop MapReduce: key advantage.',
         'answer': 'Spark keeps intermediate data in memory (RDDs) rather than writing to disk between stages. 10–100× faster for iterative algorithms (e.g. machine learning).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'CAP Theorem (distributed systems).',
         'answer': 'A distributed system can guarantee at most two of: Consistency, Availability, Partition tolerance. In practice, partition tolerance is required, so the choice is between C and A.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
    ])

    # ------------------------------------------------------------------ #
    # 009A — Data Ethics, Privacy & Ownership
    # ------------------------------------------------------------------ #
    add_cards('Data Ethics, Privacy & Ownership', [
        {'question': 'What is algorithmic bias?',
         'answer': 'Systematic errors in AI/ML outputs that create unfair outcomes for certain groups, often due to biased training data or flawed model design.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'GDPR: key data protection principles (briefly).',
         'answer': 'Lawfulness/fairness/transparency; purpose limitation; data minimisation; accuracy; storage limitation; integrity/confidentiality; accountability.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Anonymisation vs pseudonymisation.',
         'answer': 'Anonymisation: irreversibly removes identifying information (no longer personal data). Pseudonymisation: replaces identifiers with pseudonyms — data can be re-linked with a key (still personal data under GDPR).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is differential privacy?',
         'answer': 'A mathematical guarantee that the output of an algorithm does not significantly change whether any single individual\'s data is included. Adds calibrated noise to protect individuals.',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Right to explanation (GDPR Article 22).',
         'answer': 'Individuals have the right not to be subject to solely automated decisions that significantly affect them, and to obtain a meaningful explanation of the logic involved.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
    ])

    # ------------------------------------------------------------------ #
    # 010A — Python & Pandas for Data Analytics
    # ------------------------------------------------------------------ #
    add_cards('Python & Pandas for Data Analytics', [
        {'question': 'Load a CSV into a Pandas DataFrame.',
         'answer': "import pandas as pd\ndf = pd.read_csv('data.csv')\ndf.head()  # first 5 rows",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Select rows where a column satisfies a condition in Pandas.',
         'answer': "df[df['age'] > 30]  # boolean indexing\n# or\ndf.query('age > 30')",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Group by a column and compute mean in Pandas.',
         'answer': "df.groupby('category')['value'].mean()",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Handle missing values in Pandas.',
         'answer': "df.isnull().sum()  # count per column\ndf.dropna()  # drop rows with any NaN\ndf.fillna(df.mean())  # fill with column mean",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Train a scikit-learn classifier with train/test split.',
         'answer': "from sklearn.model_selection import train_test_split\nfrom sklearn.ensemble import RandomForestClassifier\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)\nclf = RandomForestClassifier()\nclf.fit(X_train, y_train)\nprint(clf.score(X_test, y_test))",
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Apply StandardScaler in scikit-learn correctly (without leakage).',
         'answer': "from sklearn.preprocessing import StandardScaler\nscaler = StandardScaler()\nX_train_sc = scaler.fit_transform(X_train)  # fit on train only\nX_test_sc = scaler.transform(X_test)  # apply same transform",
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Plot a histogram in matplotlib/seaborn.',
         'answer': "import matplotlib.pyplot as plt\nplt.hist(df['column'], bins=20)\nplt.xlabel('Value'); plt.ylabel('Count'); plt.show()\n# or: import seaborn as sns; sns.histplot(df['column'])",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Compute correlation matrix and visualise as heatmap.',
         'answer': "import seaborn as sns\ncorr = df.corr()\nsns.heatmap(corr, annot=True, cmap='coolwarm')",
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
    ])


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0034_flashcards_sma209'),
    ]

    operations = [
        migrations.RunPython(seed_flashcards, reverse_func),
    ]
