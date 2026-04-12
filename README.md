## Project Title: 
Analyzing the Impact of Sleep Hours and Study Habits on Student Performance (which factors affect studets academic lifestyle)

## Motivation 
Student academic performance is influenced by various factors, including study habits, previous academic success, and lifestyle behaviors such as sleep. Among these, sleep is often overlooked despite its importance for cognitive function and concentration. This project aims to investigate how sleep duration, along with other study-related factors, affects student performance.

## Data Source and Collection: 
The dataset used in this project is obtained from Kaggle and contains information about students daily or weekly study habits and performance informations. The dataset includes variables such as hours studied, previous scores, extracurricular activities, sleep hours, and the number of practice questions completed.

Since the dataset is publicly available, additional enrichment will be achieved through feature engineering and extended analysis of relationships between variables.

## Data Characteristics: 
The dataset consists of approximately 10,000 observations and includes both numerical and categorical variables. Key features include:
- Hours Studied,
- Previous Scores,
- Sleep Hours,
- Extracurricular Activities,
- Sample Question Papers Practiced,
- Performance Index,

The dataset does not contain missing values and is suitable for both statistical analysis and machine learning applications.

## Data Enrichment Strategy: Sleep Health & Lifestyle Dataset Integration

### Challenge
The Student Performance dataset lacks detailed sleep quality metrics. The Sleep Health & Lifestyle dataset contains rich sleep quality information but represents a different population. These datasets **do not share a common student identifier**, making direct joining impossible.

### Solution: Benchmark Mapping Methodology
Rather than attempting a direct merge, we use a **benchmark mapping** approach:

1. **Benchmark Creation:** Aggregate sleep quality metrics from the Sleep Health dataset by sleep duration
   - For each sleep hour level (5, 6, 7, 8 hours, etc.)
   - Calculate mean sleep quality score
   - Calculate mean stress level
   - Track sample size (number of observations per sleep hour)

2. **Feature Enrichment:** Match students in the student performance dataset to these benchmarks
   - Key: Student's reported "Sleep Hours" 
   - Lookup: Find matching sleep duration in benchmarks
   - Add: Sleep Quality Benchmark and Stress Benchmark columns
   - Handle missing values via mean imputation

3. **New Features Added:**
   - `Sleep_Quality_Benchmark`: Mean sleep quality score for students' reported sleep duration
   - `Stress_Benchmark`: Mean stress level for students' reported sleep duration
   - These represent how a student's sleep duration compares to population norms

### Documented Assumptions
✓ Sleep hours are reliably self-reported in both datasets  
✓ Sleep quality measurement scales are comparable across datasets (1-10 scale in both)  
✓ Rounding sleep duration to nearest hour appropriately captures patterns  
✓ Sleep quality norms from one population are reasonably transferable to student population  

### Critical Limitations
⚠️ **Population Differences:** Sleep Health dataset may include non-students (workers, retirees) with different demographics  
⚠️ **No Individual Matching:** Benchmarks represent population-level patterns, not individual correspondences  
⚠️ **Aggregation Loss:** Mean benchmark masks variation within sleep hour categories  
⚠️ **Correlation ≠ Causation:** Benchmarks show associations, not causal relationships  
⚠️ **Imputation Bias:** Rare sleep durations filled with mean, creating artificial uniformity  

### Validation: Enrichment Contribution
Before including the enriched features in analysis, we validated they provide genuine new information:
- Sleep Quality Benchmark correlates with Performance Index (not just noise)
- Benchmark captures different variation than raw Sleep Hours alone
- Features are not highly redundant (r < 0.85)
- Enrichment adds a new dimension: *population norms*, not just raw duration

**Result:** The enrichment provides meaningful value and is retained for hypothesis testing (H4).

### Code Implementation
The data enrichment pipeline is documented in:
- `src/data_enrichment.py` - Functions for benchmark creation and enrichment
- `notebooks/02_hypothesis_tests.ipynb` - Notebook with full enrichment methodology and validation

## Research Questions:
- Does sleep duration have a measurable impact on student performance?
- How strongly do study habits influence academic success?
- Which variable is the most important predictor of performance?
- Do extracurricular activities affect performance outcomes?

## Planned Analysis: 
The project will begin with data cleaning and preprocessing, followed by exploratory data analysis (EDA) to understand variable distributions and relationships.

Statistical analysis methods such as correlation analysis and hypothesis testing will be applied to examine relationships between variables.

Finally, machine learning techniques, particularly regression models, will be used to predict student performance based on the given features.

## Expected Outcomes: 
The project is expected to identify the most significant factors affecting student performance and evaluate the role of sleep in academic success. The findings may provide insights into how students can optimize their study habits and daily routines for better performance.

## Status:
Proposal submitted. Exploratory Data Analysis completed.

## Notebooks and Usage:
- [EDA Notebook](notebooks/01_data_overview.ipynb) - Exploratory Data Analysis
- [Hypothesis Tests Notebook](notebooks/02_hypothesis_tests.ipynb) - H1-H4 Statistical Tests + Enrichment

## Hypotheses
- **H1:** Students sleeping 7+ hours perform significantly better (t-test)
- **H2:** Hours studied positively correlates with performance (Pearson)
- **H3:** Extracurricular activities do not significantly affect performance (t-test)
- **H4:** Sleep quality benchmark correlates with performance (Pearson)

## AI Tool Disclosure
Claude (Anthropic) was used as an AI assistant in this project for hypothesis design, 
Python code structuring, and enrichment strategy. 

Key prompts included requests for: hypothesis test selection, scipy.stats implementation, 
and Sleep Health dataset integration approach.

All outputs were reviewed, tested, and verified by the student.
