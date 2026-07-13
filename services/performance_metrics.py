from __future__ import annotations

import numpy as np
import pandas as pd


# =====================================================
# PERFORMANCE METRICS
# =====================================================

"""
Librería científica del módulo de Rendimiento Físico.

Este archivo contiene exclusivamente funciones de cálculo.

No contiene:

- Streamlit
- Plotly
- Performance Engine
- Interpretaciones
- Recomendaciones

Todas las funciones deberán ser reutilizables desde
cualquier parte del proyecto.
"""


# =====================================================
# HELPERS
# =====================================================

def safe_divide(

    numerator,

    denominator

):

    denominator = denominator.replace(

        0,

        np.nan

    )

    return numerator / denominator


def rolling_mean(

    series,

    window

):

    return (

        series

        .rolling(

            window=window,

            min_periods=1

        )

        .mean()

    )


def rolling_std(

    series,

    window

):

    return (

        series

        .rolling(

            window=window,

            min_periods=1

        )

        .std()

    )


def exponential_moving_average(

    series,

    span

):

    return (

        series

        .ewm(

            span=span,

            adjust=False

        )

        .mean()

    )


# =====================================================
# RELATIVE METRICS
# =====================================================

def relative_metric(

    value,

    duration

):

    duration = duration.replace(

        0,

        np.nan

    )

    return value / duration


# =====================================================
# ACUTE LOAD
# =====================================================

def calculate_acute_load(

    series,

    window=7

):

    return rolling_mean(

        series,

        window

    )


# =====================================================
# CHRONIC LOAD
# =====================================================

def calculate_chronic_load(

    series,

    window=28

):

    return rolling_mean(

        series,

        window

    )


# =====================================================
# EWMA
# =====================================================

def calculate_ewma(

    series,

    span

):

    return exponential_moving_average(

        series,

        span

    )


# =====================================================
# ACWR
# =====================================================

def calculate_acwr(

    acute_load,

    chronic_load

):

    return safe_divide(

        acute_load,

        chronic_load

    )


# =====================================================
# MONOTONY
# =====================================================

def calculate_monotony(

    series,

    window=7

):

    mean = rolling_mean(

        series,

        window

    )

    std = rolling_std(

        series,

        window

    )

    return safe_divide(

        mean,

        std

    )


# =====================================================
# STRAIN
# =====================================================

def calculate_strain(

    acute_load,

    monotony

):

    return acute_load * monotony


# =====================================================
# Z-SCORE
# =====================================================

def calculate_zscore(

    series

):

    mean = series.mean()

    std = series.std()

    if std == 0 or np.isnan(std):

        return pd.Series(

            np.nan,

            index=series.index

        )

    return (

        series

        -

        mean

    ) / std


# =====================================================
# PERCENTILE
# =====================================================

def calculate_percentile(

    series

):

    return (

        series

        .rank(

            pct=True

        )

        * 100

    )


# =====================================================
# RANKING
# =====================================================

def calculate_ranking(

    series,

    ascending=False

):

    return (

        series

        .rank(

            method="dense",

            ascending=ascending

        )

    )


# =====================================================
# COEFFICIENT OF VARIATION
# =====================================================

def calculate_cv(

    series

):

    mean = series.mean()

    std = series.std()

    if mean == 0 or np.isnan(mean):

        return np.nan

    return (

        std

        /

        mean

    ) * 100


# =====================================================
# SMALLEST WORTHWHILE CHANGE
# =====================================================

def calculate_swc(

    series,

    factor=0.2

):

    return (

        series.std()

        * factor

    )


# =====================================================
# TYPICAL ERROR
# =====================================================

def calculate_typical_error(

    series

):

    differences = series.diff()

    return (

        differences.std()

        /

        np.sqrt(2)

    )

# =====================================================
# ROLLING METRICS
# =====================================================

def calculate_rolling_mean(

    series,

    window=7

):

    return rolling_mean(

        series,

        window

    )


def calculate_rolling_std(

    series,

    window=7

):

    return rolling_std(

        series,

        window

    )


def calculate_rolling_max(

    series,

    window=7

):

    return (

        series

        .rolling(

            window=window,

            min_periods=1

        )

        .max()

    )


def calculate_rolling_min(

    series,

    window=7

):

    return (

        series

        .rolling(

            window=window,

            min_periods=1

        )

        .min()

    )


def calculate_rolling_median(

    series,

    window=7

):

    return (

        series

        .rolling(

            window=window,

            min_periods=1

        )

        .median()

    )


# =====================================================
# DELTAS
# =====================================================

def calculate_delta(

    series

):

    return series.diff()


def calculate_delta_percent(

    series

):

    previous = series.shift(

        1

    )

    return safe_divide(

        series - previous,

        previous

    ) * 100


# =====================================================
# PLAYER BASELINE
# =====================================================

def calculate_baseline(

    series

):

    return series.mean()


def calculate_baseline_std(

    series

):

    return series.std()


def calculate_baseline_min(

    series

):

    return series.min()


def calculate_baseline_max(

    series

):

    return series.max()


# =====================================================
# PLAYER DEVIATION
# =====================================================

def calculate_deviation(

    series

):

    baseline = calculate_baseline(

        series

    )

    return (

        series

        -

        baseline

    )


def calculate_deviation_percent(

    series

):

    baseline = calculate_baseline(

        series

    )

    if baseline == 0:

        return pd.Series(

            np.nan,

            index=series.index

        )

    return (

        (

            series

            -

            baseline

        )

        /

        baseline

    ) * 100

# =====================================================
# TEAM METRICS
# =====================================================

def calculate_team_mean(

    dataframe,

    metric,

    team_column="team"

):

    return (

        dataframe

        .groupby(

            team_column

        )[metric]

        .transform(

            "mean"

        )

    )


def calculate_team_std(

    dataframe,

    metric,

    team_column="team"

):

    return (

        dataframe

        .groupby(

            team_column

        )[metric]

        .transform(

            "std"

        )

    )


def calculate_team_zscore(

    dataframe,

    metric,

    team_column="team"

):

    mean = calculate_team_mean(

        dataframe,

        metric,

        team_column

    )

    std = calculate_team_std(

        dataframe,

        metric,

        team_column

    )

    return safe_divide(

        dataframe[metric] - mean,

        std

    )


# =====================================================
# POSITION METRICS
# =====================================================

def calculate_position_mean(

    dataframe,

    metric,

    position_column="position"

):

    return (

        dataframe

        .groupby(

            position_column

        )[metric]

        .transform(

            "mean"

        )

    )


def calculate_position_std(

    dataframe,

    metric,

    position_column="position"

):

    return (

        dataframe

        .groupby(

            position_column

        )[metric]

        .transform(

            "std"

        )

    )


def calculate_position_percentile(

    dataframe,

    metric,

    position_column="position"

):

    return (

        dataframe

        .groupby(

            position_column

        )[metric]

        .rank(

            pct=True

        )

        * 100

    )


# =====================================================
# SESSION METRICS
# =====================================================

def calculate_session_mean(

    dataframe,

    metric,

    session_column="date"

):

    return (

        dataframe

        .groupby(

            session_column

        )[metric]

        .transform(

            "mean"

        )

    )


def calculate_session_std(

    dataframe,

    metric,

    session_column="date"

):

    return (

        dataframe

        .groupby(

            session_column

        )[metric]

        .transform(

            "std"

        )

    )


def calculate_session_percentile(

    dataframe,

    metric,

    session_column="date"

):

    return (

        dataframe

        .groupby(

            session_column

        )[metric]

        .rank(

            pct=True

        )

        * 100

    )


# =====================================================
# TREND
# =====================================================

def calculate_trend(

    series,

    window=5

):

    trend = (

        series

        .rolling(

            window,

            min_periods=2

        )

        .apply(

            lambda x:

            np.polyfit(

                np.arange(

                    len(x)

                ),

                x,

                1

            )[0],

            raw=False

        )

    )

    return trend

# =====================================================
# AVAILABILITY METRICS
# =====================================================

def calculate_availability(

    dataframe,

    availability_column="availability"

):

    return (

        dataframe[

            availability_column

        ]

        .notna()

        .astype(

            int

        )

    )


def calculate_availability_percentage(

    dataframe,

    availability_column="availability"

):

    return (

        dataframe

        .groupby(

            "player"

        )[availability_column]

        .transform(

            lambda x:

            x.notna().mean()

            * 100

        )

    )


# =====================================================
# WELLNESS
# =====================================================

def calculate_wellness_score(

    dataframe,

    columns

):

    return (

        dataframe[columns]

        .mean(

            axis=1,

            skipna=True

        )

    )


def calculate_wellness_delta(

    series

):

    return series.diff()


def calculate_wellness_zscore(

    series

):

    return calculate_zscore(

        series

    )


# =====================================================
# HEART RATE
# =====================================================

def calculate_hr_reserve(

    max_hr,

    resting_hr,

    current_hr

):

    return safe_divide(

        current_hr - resting_hr,

        max_hr - resting_hr

    ) * 100


def calculate_hr_percentage(

    current_hr,

    max_hr

):

    return safe_divide(

        current_hr,

        max_hr

    ) * 100


# =====================================================
# READINESS
# =====================================================

def calculate_readiness_score(

    dataframe,

    variables,

    weights=None

):

    values = dataframe[

        variables

    ].copy()

    if weights is None:

        weights = np.ones(

            len(

                variables

            )

        )

    weights = np.array(

        weights

    )

    weights = weights / weights.sum()

    return (

        values

        * weights

    ).sum(

        axis=1

    )


# =====================================================
# NORMALIZATION
# =====================================================

def min_max_normalization(

    series

):

    minimum = series.min()

    maximum = series.max()

    if minimum == maximum:

        return pd.Series(

            np.nan,

            index=series.index

        )

    return (

        series

        -

        minimum

    ) / (

        maximum

        -

        minimum

    )


def normalize_0_100(

    series

):

    return (

        min_max_normalization(

            series

        )

        * 100

    )


def standardize(

    series

):

    return calculate_zscore(

        series

    )

# =====================================================
# THRESHOLDS
# =====================================================

def classify_by_thresholds(

    value,

    thresholds

):

    """
    thresholds:

    [

        (0.80, "Muy Bajo"),

        (0.90, "Bajo"),

        (1.10, "Normal"),

        (1.30, "Alto"),

        (np.inf, "Muy Alto")

    ]
    """

    if pd.isna(

        value

    ):

        return np.nan

    for limit, label in thresholds:

        if value <= limit:

            return label

    return thresholds[-1][1]


# =====================================================
# FLAGS
# =====================================================

def flag_high(

    series,

    threshold

):

    return series >= threshold


def flag_low(

    series,

    threshold

):

    return series <= threshold


def flag_between(

    series,

    minimum,

    maximum

):

    return (

        (series >= minimum)

        &

        (series <= maximum)

    )


# =====================================================
# OUTLIERS
# =====================================================

def detect_outliers_zscore(

    series,

    threshold=2

):

    z = calculate_zscore(

        series

    )

    return (

        z.abs()

        >=

        threshold

    )


def detect_outliers_iqr(

    series,

    factor=1.5

):

    q1 = series.quantile(

        0.25

    )

    q3 = series.quantile(

        0.75

    )

    iqr = q3 - q1

    lower = q1 - factor * iqr

    upper = q3 + factor * iqr

    return (

        (series < lower)

        |

        (series > upper)

    )


# =====================================================
# MISSING DATA
# =====================================================

def missing_percentage(

    dataframe

):

    return (

        dataframe

        .isna()

        .mean()

        * 100

    )


def complete_cases(

    dataframe

):

    return (

        dataframe

        .dropna()

    )


# =====================================================
# DATA QUALITY
# =====================================================

def data_quality_score(

    dataframe

):

    completeness = (

        100

        -

        missing_percentage(

            dataframe

        ).mean()

    )

    duplicates = (

        dataframe

        .duplicated()

        .mean()

        * 100

    )

    score = (

        completeness

        -

        duplicates

    )

    return max(

        0,

        min(

            100,

            score

        )

    )


# =====================================================
# EXPORTABLE SUMMARY
# =====================================================

def metric_summary(

    series

):

    return {

        "count": series.count(),

        "mean": series.mean(),

        "median": series.median(),

        "std": series.std(),

        "min": series.min(),

        "max": series.max(),

        "cv": calculate_cv(

            series

        ),

        "swc": calculate_swc(

            series

        )

    }

# =====================================================
# PLAYER COMPARISONS
# =====================================================

def compare_against_player_mean(

    series

):

    baseline = series.mean()

    return series - baseline


def compare_against_player_percent(

    series

):

    baseline = series.mean()

    return safe_divide(

        series - baseline,

        pd.Series(

            baseline,

            index=series.index

        )

    ) * 100


def compare_against_team(

    dataframe,

    metric

):

    team_mean = calculate_team_mean(

        dataframe,

        metric

    )

    return dataframe[metric] - team_mean


def compare_against_position(

    dataframe,

    metric

):

    position_mean = calculate_position_mean(

        dataframe,

        metric

    )

    return dataframe[metric] - position_mean


# =====================================================
# MICROCYCLE METRICS
# =====================================================

def calculate_microcycle_mean(

    dataframe,

    metric,

    microcycle_column="microcycle_id"

):

    return (

        dataframe

        .groupby(

            microcycle_column

        )[metric]

        .transform(

            "mean"

        )

    )


def calculate_microcycle_total(

    dataframe,

    metric,

    microcycle_column="microcycle_id"

):

    return (

        dataframe

        .groupby(

            microcycle_column

        )[metric]

        .transform(

            "sum"

        )

    )


def calculate_microcycle_max(

    dataframe,

    metric,

    microcycle_column="microcycle_id"

):

    return (

        dataframe

        .groupby(

            microcycle_column

        )[metric]

        .transform(

            "max"

        )

    )


# =====================================================
# CHANGE DETECTION
# =====================================================

def detect_positive_change(

    series,

    threshold=5

):

    delta = calculate_delta_percent(

        series

    )

    return delta >= threshold


def detect_negative_change(

    series,

    threshold=-5

):

    delta = calculate_delta_percent(

        series

    )

    return delta <= threshold


# =====================================================
# MOVING BASELINE
# =====================================================

def calculate_dynamic_baseline(

    series,

    window=28

):

    return (

        series

        .rolling(

            window,

            min_periods=1

        )

        .mean()

    )


def compare_against_dynamic_baseline(

    series,

    window=28

):

    baseline = calculate_dynamic_baseline(

        series,

        window

    )

    return series - baseline


# =====================================================
# SCIENTIFIC INDEXES
# =====================================================

def calculate_training_monotony(

    load_series,

    window=7

):

    return calculate_monotony(

        load_series,

        window

    )


def calculate_training_strain(

    load_series,

    window=7

):

    acute = calculate_acute_load(

        load_series,

        window

    )

    monotony = calculate_monotony(

        load_series,

        window

    )

    return calculate_strain(

        acute,

        monotony

    )

# =====================================================
# PERFORMANCE STATUS
# =====================================================

def classify_acwr(

    acwr

):

    thresholds = [

        (0.80, "Muy Baja"),

        (1.30, "Óptima"),

        (1.50, "Elevada"),

        (np.inf, "Muy Elevada")

    ]

    return classify_by_thresholds(

        acwr,

        thresholds

    )


def classify_zscore(

    zscore

):

    thresholds = [

        (-2.0, "Muy Bajo"),

        (-1.0, "Bajo"),

        (1.0, "Normal"),

        (2.0, "Alto"),

        (np.inf, "Muy Alto")

    ]

    return classify_by_thresholds(

        zscore,

        thresholds

    )


def classify_percentile(

    percentile

):

    thresholds = [

        (20, "Muy Bajo"),

        (40, "Bajo"),

        (60, "Normal"),

        (80, "Alto"),

        (100, "Muy Alto")

    ]

    return classify_by_thresholds(

        percentile,

        thresholds

    )


# =====================================================
# COMPOSITE SCORE
# =====================================================

def weighted_score(

    dataframe,

    metrics,

    weights

):

    values = dataframe[

        metrics

    ].copy()

    weights = np.array(

        weights

    )

    weights = weights / weights.sum()

    return (

        values

        * weights

    ).sum(

        axis=1

    )


# =====================================================
# NORMALIZED SCORE
# =====================================================

def normalized_score(

    dataframe,

    metrics,

    weights=None

):

    normalized = pd.DataFrame(

        index=dataframe.index

    )

    for metric in metrics:

        normalized[metric] = normalize_0_100(

            dataframe[metric]

        )

    if weights is None:

        weights = np.ones(

            len(

                metrics

            )

        )

    return weighted_score(

        normalized,

        metrics,

        weights

    )


# =====================================================
# RISK SCORE
# =====================================================

def risk_score(

    dataframe,

    variables,

    weights=None

):

    scores = pd.DataFrame(

        index=dataframe.index

    )

    for variable in variables:

        scores[variable] = normalize_0_100(

            dataframe[variable]

        )

    if weights is None:

        weights = np.ones(

            len(

                variables

            )

        )

    return weighted_score(

        scores,

        variables,

        weights

    )


# =====================================================
# PLAYER SUMMARY
# =====================================================

def player_summary(

    dataframe,

    metrics

):

    summary = {}

    for metric in metrics:

        if metric not in dataframe.columns:

            continue

        summary[metric] = {

            "mean": dataframe[metric].mean(),

            "max": dataframe[metric].max(),

            "min": dataframe[metric].min(),

            "std": dataframe[metric].std(),

            "cv": calculate_cv(

                dataframe[metric]

            ),

            "swc": calculate_swc(

                dataframe[metric]

            ),

            "latest": dataframe[metric].iloc[-1]

        }

    return summary


# =====================================================
# TEAM SUMMARY
# =====================================================

def team_summary(

    dataframe,

    metrics,

    team

):

    df = dataframe[

        dataframe["team"] == team

    ]

    return player_summary(

        df,

        metrics

    )

# =====================================================
# LONGITUDINAL METRICS
# =====================================================

def calculate_consistency(

    series

):

    cv = calculate_cv(

        series

    )

    if np.isnan(

        cv

    ):

        return np.nan

    return 100 - cv


def calculate_stability(

    series,

    window=28

):

    rolling = calculate_rolling_std(

        series,

        window

    )

    return rolling


def calculate_variation(

    series

):

    return (

        series.max()

        -

        series.min()

    )


def calculate_range_percent(

    series

):

    mean = series.mean()

    if mean == 0:

        return np.nan

    return (

        (

            series.max()

            -

            series.min()

        )

        /

        mean

    ) * 100


# =====================================================
# SESSION COMPARISONS
# =====================================================

def compare_last_session(

    series

):

    return series.diff()


def compare_last_session_percent(

    series

):

    previous = series.shift(

        1

    )

    return safe_divide(

        series - previous,

        previous

    ) * 100


def compare_last_three_sessions(

    series

):

    baseline = (

        series

        .shift(

            1

        )

        .rolling(

            3,

            min_periods=1

        )

        .mean()

    )

    return series - baseline


# =====================================================
# FATIGUE INDEXES
# =====================================================

def calculate_fatigue_index(

    acute,

    chronic

):

    return calculate_acwr(

        acute,

        chronic

    )


def calculate_recovery_index(

    readiness,

    fatigue

):

    return readiness - fatigue


def calculate_load_balance(

    external_load,

    internal_load

):

    return safe_divide(

        external_load,

        internal_load

    )


# =====================================================
# TRAINING RESPONSE
# =====================================================

def calculate_training_efficiency(

    external_load,

    internal_load

):

    return safe_divide(

        external_load,

        internal_load

    )


def calculate_internal_external_ratio(

    internal_load,

    external_load

):

    return safe_divide(

        internal_load,

        external_load

    )


# =====================================================
# EXPORT HELPERS
# =====================================================

AVAILABLE_METRICS = [

    "acute_load",

    "chronic_load",

    "ewma",

    "acwr",

    "monotony",

    "strain",

    "percentile",

    "ranking",

    "zscore",

    "cv",

    "swc",

    "typical_error",

    "trend",

    "baseline",

    "deviation",

    "consistency",

    "stability",

    "training_efficiency",

    "load_balance",

    "fatigue_index",

    "recovery_index"

]


__all__ = [

    name

    for name in globals()

    if name.startswith(

        "calculate_"

    )

] + [

    "AVAILABLE_METRICS",

    "safe_divide",

    "relative_metric",

    "normalize_0_100",

    "standardize",

    "metric_summary",

    "classify_acwr",

    "classify_zscore",

    "classify_percentile"

]