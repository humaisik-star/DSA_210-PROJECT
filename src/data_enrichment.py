"""
Data Enrichment Module: Sleep Health & Lifestyle Dataset Integration

METHODOLOGY DOCUMENTATION
=========================

MERGING APPROACH:
-----------------
Since the Primary Dataset (Student_Performance.csv) and the Sleep Health Dataset 
(Sleep_health_and_lifestyle_dataset.csv) do not share a direct common identifier (e.g., 
student ID), we employ a BENCHMARK MAPPING approach:

1. Aggregate sleep quality metrics from the Sleep Health dataset by sleep duration
2. Create "sleep quality benchmarks" for each sleep hour level (e.g., 5 hrs, 6 hrs, 7 hrs, etc.)
3. Match students in the primary dataset to these benchmarks based on their reported sleep hours

RATIONALE:
----------
- No direct key exists between datasets (different populations)
- Sleep duration is a consistent variable across both datasets
- Sleep quality benchmarks provide normative reference points for interpreting sleep patterns
- This approach enriches the primary dataset with external benchmark values

ASSUMPTIONS:
============
1. Sleep hours are reliably reported in both datasets
2. Sleep quality norms from the Sleep Health population are representative and transferable
   to the student population (reasonable assumption: both involve adults with similar 
   sleep quality measurement scales)
3. Aggregating by sleep hour rounds data appropriately (Sleep Health data may have decimals,
   we round to match Sleep Hours column in primary dataset)
4. Students with the same sleep duration experience similar sleep quality patterns

LIMITATIONS & CAVEATS:
======================
⚠️  CRITICAL LIMITATIONS:

1. POPULATION DIFFERENCE:
   - Sleep Health dataset may have different demographic composition (age, health status)
   - Sleep quality norms may not perfectly apply to student population
   - Confounding factors (exercise, diet, stress) differ between populations

2. IMPERFECT MATCHING:
   - Rounding sleep hours may obscure important differences
   - No causality can be inferred; benchmarks are correlational
   - Students with exactly 7 hours may have diverse sleep quality experiences

3. AGGREGATION LOSS:
   - Mean benchmark masks individual variation within each sleep hour category
   - Assumes within-hour groups are homogeneous (they're not)

4. MISSING DATA HANDLING:
   - Sleep hour values in primary dataset without matching benchmarks get filled 
     with the mean benchmark value (default imputation strategy)

VALIDATION:
===========
To assess whether the enriched features actually contribute to analysis:
- Compare model performance WITH vs WITHOUT enriched features
- Check correlation of benchmark with target variable (Performance Index)
- Verify that benchmark adds information not already captured by raw sleep hours
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict


def create_sleep_benchmarks(sleep_health_df: pd.DataFrame) -> pd.DataFrame:
    """
    Create sleep quality benchmarks from Sleep Health dataset.
    
    Parameters:
    -----------
    sleep_health_df : pd.DataFrame
        Raw sleep health dataset with columns:
        - 'Sleep Duration' (in hours, may be float)
        - 'Quality of Sleep' (1-10 scale)
        - 'Stress Level' (1-10 scale)
    
    Returns:
    --------
    pd.DataFrame
        Benchmarks with columns:
        - Sleep_Hours_Rounded: integer sleep hours (5, 6, 7, 8, etc.)
        - Sleep_Quality_Benchmark: mean quality of sleep for that duration
        - Stress_Benchmark: mean stress level for that duration
    """
    # Round sleep duration to nearest hour
    sleep_health_df = sleep_health_df.copy()
    sleep_health_df['Sleep_Hours_Rounded'] = sleep_health_df['Sleep Duration'].round().astype(int)
    
    # Aggregate benchmarks by sleep hour
    benchmarks = sleep_health_df.groupby('Sleep_Hours_Rounded').agg(
        Sleep_Quality_Benchmark=('Quality of Sleep', 'mean'),
        Stress_Benchmark=('Stress Level', 'mean'),
        Sample_Size=('Sleep Duration', 'count')  # Track how many observations per hour
    ).reset_index()
    
    return benchmarks


def enrich_student_data(student_df: pd.DataFrame, 
                       benchmarks_df: pd.DataFrame,
                       fill_method: str = 'mean') -> pd.DataFrame:
    """
    Enrich student dataset with sleep quality benchmarks.
    
    Parameters:
    -----------
    student_df : pd.DataFrame
        Student performance dataset with 'Sleep Hours' column
    benchmarks_df : pd.DataFrame
        Sleep benchmarks created by create_sleep_benchmarks()
    fill_method : str
        Strategy for missing benchmark values: 'mean' or 'forward_fill'
    
    Returns:
    --------
    pd.DataFrame
        Enriched dataset with added columns:
        - Sleep_Quality_Benchmark
        - Stress_Benchmark
    
    Notes:
    ------
    - Missing values (students with sleep hours not in benchmark data) are handled via fill_method
    - Original columns preserved; new columns appended
    """
    df_enriched = student_df.copy()
    
    # Merge on sleep hours
    df_enriched = df_enriched.merge(
        benchmarks_df[['Sleep_Hours_Rounded', 'Sleep_Quality_Benchmark', 'Stress_Benchmark']],
        left_on='Sleep Hours',
        right_on='Sleep_Hours_Rounded',
        how='left'
    )
    
    # Handle missing values
    if fill_method == 'mean':
        df_enriched['Sleep_Quality_Benchmark'].fillna(
            df_enriched['Sleep_Quality_Benchmark'].mean(), 
            inplace=True
        )
        df_enriched['Stress_Benchmark'].fillna(
            df_enriched['Stress_Benchmark'].mean(),
            inplace=True
        )
    elif fill_method == 'forward_fill':
        df_enriched['Sleep_Quality_Benchmark'].fillna(method='ffill', inplace=True)
        df_enriched['Sleep_Quality_Benchmark'].fillna(method='bfill', inplace=True)
    
    # Drop temporary merge column
    if 'Sleep_Hours_Rounded' in df_enriched.columns:
        df_enriched.drop('Sleep_Hours_Rounded', axis=1, inplace=True)
    
    return df_enriched


def assess_enrichment_value(student_df: pd.DataFrame, 
                           enriched_df: pd.DataFrame,
                           target: str = 'Performance Index') -> Dict:
    """
    Assess whether enriched features contribute meaningful information.
    
    Parameters:
    -----------
    student_df : pd.DataFrame
        Original (non-enriched) dataset
    enriched_df : pd.DataFrame
        Enriched dataset with benchmarks
    target : str
        Target variable name
    
    Returns:
    --------
    dict
        Analysis metrics including:
        - correlation_original: corr(Sleep Hours, Performance) from original data
        - correlation_enriched: corr(Sleep Quality Benchmark, Performance) from enriched
        - information_gain: whether benchmark adds new information
        - redundancy_check: correlation between Sleep Hours and benchmark
    """
    from scipy.stats import pearsonr
    
    results = {}
    
    # Correlation of original sleep hours with performance
    r_sleep_perf, _ = pearsonr(
        student_df['Sleep Hours'], 
        student_df[target]
    )
    results['correlation_sleep_hours_performance'] = r_sleep_perf
    
    # Correlation of enriched benchmark with performance
    r_bench_perf, _ = pearsonr(
        enriched_df['Sleep_Quality_Benchmark'],
        enriched_df[target]
    )
    results['correlation_benchmark_performance'] = r_bench_perf
    
    # Check if benchmark and sleep hours are overly redundant
    r_redundancy, _ = pearsonr(
        student_df['Sleep Hours'],
        enriched_df['Sleep_Quality_Benchmark']
    )
    results['redundancy_sleep_hours_vs_benchmark'] = r_redundancy
    
    # Summary interpretation
    results['enrichment_assessment'] = {
        'benchmark_correlates_with_target': abs(r_bench_perf) > 0.1,
        'provides_new_information': abs(r_redundancy) < 0.9,  # Not perfectly correlated
        'meaningful_strength': abs(r_bench_perf) > abs(r_sleep_perf) or abs(r_bench_perf) > 0.2
    }
    
    return results
