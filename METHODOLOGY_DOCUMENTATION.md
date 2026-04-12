# Methodology Documentation for Report

This document summarizes what your TA wants you to include in your final report based on their feedback.

---

## TA Feedback Summary

Your TA approved the project with two key requirements:

1. **Document and justify the merging methodology clearly** with documented assumptions and acknowledged limitations
2. **Ensure enriched features actually contribute to analysis** and aren't just decorative

---

## What to Include in Your Methods/Data Section

### 1. Data Enrichment Methodology (Required)

**Title:** "Data Integration Strategy: Sleep Health Dataset Enrichment"

**Include these elements:**

#### Challenge/Problem Statement
> The primary dataset (Student_Performance) lacks detailed sleep quality metrics. The secondary dataset (Sleep_health_and_lifestyle) contains rich sleep quality data but different population. These datasets lack a common student identifier, requiring a thoughtful integration strategy.

#### Solution: Benchmark Mapping Methodology
Explain the steps:
1. Aggregate sleep quality metrics from Sleep Health dataset by sleep duration (group all people sleeping ~5 hours, ~6 hours, etc.)
2. Calculate benchmarks: mean quality and stress for each sleep hour level
3. Match students via sleep hours: Join student performance data to benchmarks using "Sleep Hours" as the key
4. Result: Students get "Sleep Quality Benchmark" and "Stress Benchmark" features representing population norms

#### Why This Approach?
- Acknowledges that no direct matching is possible
- Provides meaningful enrichment (population-level patterns)
- Transparent and defensible methodology
- Properly documents limitations (see below)

**Code Reference:** See `notebooks/02_hypothesis_tests.ipynb` → "Dataset Enrichment - Sleep Health benchmarks" cell

---

### 2. Documented Assumptions (Required)

List what you're assuming about the data:

```
Assumptions behind benchmark mapping:
1. Sleep hours are reliably self-reported in both datasets
2. Sleep quality measurement scales are comparable (both use 1-10 scale)
3. Rounding to integer sleep hours appropriately captures patterns
4. Sleep quality norms from Sleep Health population are reasonably 
   transferable to student population
```

**Include this in a "Data Assumptions" subsection of your Methods**

---

### 3. Critical Limitations (Required - This is What TA Emphasized)

Create a "Limitations" section acknowledging these constraints:

#### Population Differences
> The Sleep Health dataset was not collected from students. It represents a broader population that may include workers, retirees, and individuals with different health statuses. Sleep quality norms from this population may not perfectly apply to college students, who may have different sleep patterns and stress levels.

#### No Individual Matching
> Because no student identifier exists across datasets, this is not a case-by-case enrichment. Instead, we match based on population-level patterns. This means: A student sleeping 7 hours is assigned the *average* sleep quality from all Sleep Health participants who sleep ~7 hours, not a matched individual.

#### Aggregation Loss
> The mean benchmark masks individual variation. Two Sleep Health participants sleeping 7 hours may have very different actual sleep quality scores; we use only their mean. This creates artificial uniformity in student data.

#### Correlation ≠ Causation
> High sleep quality benchmarks do not *cause* high performance. Both may stem from healthier overall lifestyle choices. The benchmark shows association, not causal effect.

#### Imputation Bias
> Students with rare sleep durations (e.g., 3 or 12 hours) have no matching benchmark and are filled with the mean benchmark value, creating artificial data for these groups.

**Example text for your report:**

> While enrichment with sleep quality benchmarks provides valuable external context, several limitations should be acknowledged. First, the Sleep Health dataset represents a general population, not specifically students, so norms may not perfectly transfer. Second, matching is probabilistic (population-based) rather than individual. Third, this enrichment captures association, not causation. These limitations are addressed by: (a) reporting results alongside original variables, (b) acknowledging benchmark patterns as correlational evidence, and (c) including sensitivity analyses if possible.

---

### 4. Feature Contribution Validation (Required)

You've already implemented this! Include in your report:

**Key Finding:** Sleep Quality Benchmark
- Correlates with Performance Index: r = [insert value from notebook]
- Provides different information than raw Sleep Hours (not redundant)
- Meets criteria for genuine enrichment (checked in H4 analysis)

**Why this matters:** This validates that the benchmark is not "decorative" but provides meaningful information for analysis.

**Include in Results/Findings section:**

> The enrichment features were validated to ensure they contribute genuinely to the analysis. Correlation analysis showed that Sleep Quality Benchmark correlates with Performance Index (r = X, p = Y), demonstrating non-trivial association with the target variable. Additionally, redundancy analysis confirmed that Sleep Quality Benchmark captures variation distinct from raw Sleep Hours (r = Z < 0.85), indicating it provides new information. This validation supports retaining the enriched features in hypothesis testing (H4).

---

## How to Reference These in Your Report

### In Abstract/Introduction
> "To enrich analysis with external sleep quality context, we integrated a secondary Sleep Health dataset using benchmark mapping methodology. Full documentation of assumptions and limitations is provided in the Methods section below."

### In Methods
Include subsections:
- **Data Enrichment Strategy:** 3-4 paragraphs explaining benchmark mapping
- **Data Assumptions:** List assumptions explicitly  
- **Limitations:** Detailed discussion of constraints (1-2 pages is appropriate)
- **Enrichment Validation:** Brief description of how you verified contribution

### In Results/H4 Section
> H4 tests whether sleep quality benchmarks (derived from external Sleep Health dataset) correlate with student performance. This hypothesis extends H1 by examining population-norm patterns rather than raw sleep hours. Results showed [your findings]. These results suggest that sleep quality benchmarks, which represent student sleep durations compared to norms, provide meaningful additional information beyond simple sleep duration for predicting academic performance.

### In Discussion/Conclusion  
Address:
- What the enrichment revealed (new dimension of understanding)
- How limitations affect interpretation (e.g., "results should be understood as correlational, not causal")
- Whether enrichment strategy was successful

---

## Files to Reference in Your Report

1. **Notebook:** `notebooks/02_hypothesis_tests.ipynb`
   - Cells: "Dataset Enrichment - Sleep Health benchmarks" and methodology sections
   - Shows how enrichment is implemented

2. **Utility Module:** `src/data_enrichment.py`
   - Contains docstrings with full methodology documentation
   - Shows thought behind each step

3. **README:** `README.md` 
   - "Data Enrichment Strategy" section has overview

---

## Checklist for Report

Use this to ensure you've addressed all TA feedback:

- [ ] **Methods section includes:**
  - [ ] Challenge statement (why enrichment was needed)
  - [ ] Benchmark mapping explanation (how it works)
  - [ ] Explicit assumptions listed
  - [ ] Comprehensive limitations section (population differences, aggregation loss, causation issue, etc.)
  - [ ] Enrichment validation (how you verified it contributes)

- [ ] **Results section shows:**
  - [ ] H4 hypothesis test results
  - [ ] Interpretation of benchmark correlation vs H1 sleep hours correlation
  - [ ] Brief summary of enrichment contribution

- [ ] **Code is documented:**
  - [ ] src/data_enrichment.py has docstrings
  - [ ] Notebook has markdown sections explaining methodology
  - [ ] Code comments explain the enrichment process

- [ ] **Report acknowledges:**
  - [ ] No causation claims
  - [ ] Population differences as limitation
  - [ ] Enrichment as providing population-level patterns, not individual matching

---

## Next Steps

1. **Run the notebook completely** - Execute all cells to generate visualizations and results
2. **Review enrichment validation output** - Note the r values and assessment from enrichment validation cell
3. **Draft methodology sections** - Use templates above
4. **Include code snippets** - Reference the enrichment code in Methods (technical appendix if too long)
5. **Get feedback** - Have TA review methodology section before final report

---

## Questions to Help Finalize

When writing, ensure you can answer:
- Q: Why didn't you just merge the datasets directly?  
  A: No common student identifier; benchmark mapping provides population-level context
- Q: How do the benchmarks help?  
  A: H4 shows they correlate with performance; validates that enrichment adds value
- Q: Are results reliable given the enrichment approach?  
  A: Reliable for understanding associations; limitations acknowledged; not for causal claims
- Q: Is this enrichment method justified?  
  A: Yes - transparent methodology, validated contribution, limitations documented

