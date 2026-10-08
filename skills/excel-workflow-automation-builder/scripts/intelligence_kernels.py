#!/usr/bin/env python3
"""Vetted build-time reference kernels for bounded planning and forecasting.

Generated Motivs automations remain self-contained. Copy only the functions a
workflow needs into automation.py; do not import this helper at platform runtime.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from typing import Any

import numpy as np
import pandas as pd


CAPABILITIES = frozenset(
    {"clean", "reconcile", "calculate", "allocate", "predict", "simulate", "compare"}
)


def minimum_capability_route(
    *,
    rollout_mode: str = "shadow",
    advanced_outcome_explicit: bool = False,
    needs_cleaning: bool = True,
    needs_reconciliation: bool = False,
    needs_calculation: bool = False,
    needs_allocation: bool = False,
    allocation_contract_complete: bool = False,
    needs_unknown_future: bool = False,
    prediction_contract_complete: bool = False,
    temporal_baseline_available: bool = False,
    uncertainty_changes_action: bool = False,
    scenario_contract_complete: bool = False,
    needs_comparison: bool = False,
    decision_contract_complete: bool = False,
) -> dict[str, object]:
    """Validate an agent-derived route without interpreting free-form user text."""
    mode = str(rollout_mode).strip().lower()
    if mode not in {"off", "shadow", "beta", "enabled"}:
        raise ValueError("Rollout mode must be off, shadow, beta, or enabled.")

    baseline_capabilities: list[str] = []
    classified_capabilities: list[str] = []
    blockers: list[str] = []
    if needs_cleaning:
        baseline_capabilities.append("clean")
        classified_capabilities.append("clean")
    if needs_reconciliation:
        baseline_capabilities.append("reconcile")
        classified_capabilities.append("reconcile")
    if needs_calculation:
        classified_capabilities.append("calculate")
    if needs_allocation:
        classified_capabilities.append("allocate")
        if not allocation_contract_complete:
            blockers.append("allocation_contract_incomplete")
    if needs_unknown_future:
        classified_capabilities.append("predict")
        if not (prediction_contract_complete and temporal_baseline_available):
            blockers.append("prediction_gate_not_met")
    if uncertainty_changes_action:
        classified_capabilities.append("simulate")
        if not scenario_contract_complete:
            blockers.append("scenario_contract_incomplete")
    if needs_comparison:
        classified_capabilities.append("compare")
        if not decision_contract_complete:
            blockers.append("decision_contract_incomplete")

    advanced_requested = any(
        capability not in {"clean", "reconcile"} for capability in classified_capabilities
    )
    if mode == "off":
        active_capabilities = baseline_capabilities
        classified_capabilities = baseline_capabilities.copy()
        blockers = []
        status = "disabled" if advanced_requested else "ready"
    elif mode == "shadow":
        active_capabilities = baseline_capabilities
        status = "shadowed" if advanced_requested else "ready"
    else:
        if mode == "beta" and advanced_requested and not advanced_outcome_explicit:
            blockers.append("advanced_outcome_not_explicit")
        active_capabilities = (
            classified_capabilities.copy() if not blockers else baseline_capabilities
        )
        status = "ready" if not blockers else "needs_confirmation"

    return {
        "mode": mode,
        "classified_capabilities": classified_capabilities,
        "capabilities": active_capabilities,
        "blockers": blockers,
        "status": status,
    }


def _positive_horizon(horizon: int) -> int:
    value = int(horizon)
    if value < 1:
        raise ValueError("Forecast horizon must be at least one period.")
    return value


def _numeric_history(values: Iterable[object], *, minimum: int = 1) -> np.ndarray:
    series = pd.to_numeric(pd.Series(list(values), dtype="object"), errors="coerce")
    if series.isna().any():
        raise ValueError("Historical values contain missing or non-numeric observations.")
    array = series.to_numpy(dtype=float)
    if len(array) < minimum:
        raise ValueError(f"At least {minimum} historical observations are required.")
    if not np.isfinite(array).all():
        raise ValueError("Historical values contain non-finite observations.")
    return array


def last_value_forecast(values: Iterable[object], horizon: int) -> np.ndarray:
    history = _numeric_history(values)
    return np.repeat(history[-1], _positive_horizon(horizon)).astype(float)


def seasonal_naive_forecast(
    values: Iterable[object], horizon: int, *, season_length: int
) -> np.ndarray:
    history = _numeric_history(values)
    season = int(season_length)
    if season < 2:
        raise ValueError("Season length must be at least two periods.")
    if len(history) < season:
        raise ValueError("History is shorter than the requested seasonal cycle.")
    return np.asarray(
        [history[len(history) - season + (index % season)] for index in range(_positive_horizon(horizon))],
        dtype=float,
    )


def moving_average_forecast(
    values: Iterable[object], horizon: int, *, window: int = 3
) -> np.ndarray:
    history = _numeric_history(values)
    width = int(window)
    if width < 1 or width > len(history):
        raise ValueError("Moving-average window must fit inside the history.")
    return np.repeat(float(np.mean(history[-width:])), _positive_horizon(horizon))


def weighted_moving_average_forecast(
    values: Iterable[object],
    horizon: int,
    *,
    weights: Sequence[float] = (1.0, 2.0, 3.0),
) -> np.ndarray:
    history = _numeric_history(values)
    weight_array = np.asarray(list(weights), dtype=float)
    if len(weight_array) < 1 or len(weight_array) > len(history):
        raise ValueError("Weights must be non-empty and fit inside the history.")
    if not np.isfinite(weight_array).all() or (weight_array < 0).any() or weight_array.sum() <= 0:
        raise ValueError("Weights must be finite, non-negative, and have a positive total.")
    level = float(np.average(history[-len(weight_array) :], weights=weight_array))
    return np.repeat(level, _positive_horizon(horizon))


def exponential_smoothing_forecast(
    values: Iterable[object], horizon: int, *, alpha: float = 0.3
) -> np.ndarray:
    history = _numeric_history(values)
    smoothing = float(alpha)
    if not 0 < smoothing <= 1:
        raise ValueError("Smoothing alpha must be greater than zero and at most one.")
    level = float(history[0])
    for observation in history[1:]:
        level = smoothing * float(observation) + (1 - smoothing) * level
    return np.repeat(level, _positive_horizon(horizon))


def linear_trend_forecast(
    values: Iterable[object], horizon: int, *, nonnegative: bool = False
) -> np.ndarray:
    history = _numeric_history(values, minimum=3)
    x = np.arange(len(history), dtype=float)
    slope, intercept = np.polyfit(x, history, 1)
    future_x = np.arange(len(history), len(history) + _positive_horizon(horizon), dtype=float)
    result = intercept + slope * future_x
    return np.maximum(result, 0.0) if nonnegative else result


def forecast_by_method(
    values: Iterable[object],
    horizon: int,
    *,
    method: str,
    season_length: int | None = None,
    nonnegative: bool = False,
) -> np.ndarray:
    history = _numeric_history(values)
    if method == "last_value":
        result = last_value_forecast(history, horizon)
    elif method == "seasonal_naive":
        if season_length is None:
            raise ValueError("Seasonal-naive forecasting requires a season length.")
        result = seasonal_naive_forecast(history, horizon, season_length=season_length)
    elif method == "moving_average":
        result = moving_average_forecast(history, horizon, window=min(3, len(history)))
    elif method == "weighted_moving_average":
        width = min(3, len(history))
        result = weighted_moving_average_forecast(
            history, horizon, weights=tuple(range(1, width + 1))
        )
    elif method == "exponential_smoothing":
        result = exponential_smoothing_forecast(history, horizon, alpha=0.3)
    elif method == "linear_trend":
        result = linear_trend_forecast(history, horizon, nonnegative=nonnegative)
    else:
        raise ValueError(f"Unsupported forecast method: {method}")
    return np.maximum(result, 0.0) if nonnegative else result


def temporal_backtest(
    values: Iterable[object],
    *,
    method: str,
    horizon: int = 1,
    season_length: int | None = None,
    max_origins: int = 24,
    nonnegative: bool = False,
) -> dict[str, object]:
    history = _numeric_history(values, minimum=4)
    steps = _positive_horizon(horizon)
    required = max(3, int(season_length or 1) if method == "seasonal_naive" else 3)
    last_origin = len(history) - steps
    first_origin = max(required, last_origin - max(1, int(max_origins)) + 1)
    actual: list[float] = []
    predicted: list[float] = []
    origins = 0
    for origin in range(first_origin, last_origin + 1):
        try:
            estimate = forecast_by_method(
                history[:origin],
                steps,
                method=method,
                season_length=season_length,
                nonnegative=nonnegative,
            )
        except ValueError:
            continue
        actual.extend(history[origin : origin + steps].astype(float).tolist())
        predicted.extend(estimate.astype(float).tolist())
        origins += 1
    if not actual:
        raise ValueError("History is insufficient for this temporal backtest.")
    actual_array = np.asarray(actual, dtype=float)
    predicted_array = np.asarray(predicted, dtype=float)
    residuals = actual_array - predicted_array
    denominator = float(np.sum(np.abs(actual_array)))
    return {
        "method": method,
        "origins": origins,
        "forecast_points": len(actual),
        "mae": float(np.mean(np.abs(residuals))),
        "wape": float(np.sum(np.abs(residuals)) / denominator) if denominator > 0 else None,
        "bias": float(np.mean(predicted_array - actual_array)),
        "residuals": residuals,
    }


def select_forecast(
    values: Iterable[object],
    horizon: int,
    *,
    season_length: int | None = None,
    minimum_improvement: float = 0.02,
    nonnegative: bool = False,
) -> dict[str, object]:
    history = _numeric_history(values)
    steps = _positive_horizon(horizon)
    if len(history) < max(4, steps + 3):
        return {
            "status": "insufficient",
            "suitability": "insufficient",
            "method": None,
            "baseline_method": None,
            "baseline_result": "not_testable",
            "fallback_reason": "insufficient_history",
            "point": [],
            "lower": [],
            "upper": [],
            "metrics": {},
        }

    baseline_methods = ["last_value"]
    if season_length is not None and int(season_length) >= 2 and len(history) >= 2 * int(season_length):
        baseline_methods.append("seasonal_naive")
    candidate_methods = [
        "moving_average",
        "weighted_moving_average",
        "exponential_smoothing",
    ]
    if len(history) >= 6:
        candidate_methods.append("linear_trend")

    evaluations: dict[str, dict[str, object]] = {}
    for method in baseline_methods + candidate_methods:
        try:
            evaluations[method] = temporal_backtest(
                history,
                method=method,
                horizon=steps,
                season_length=season_length,
                nonnegative=nonnegative,
            )
        except ValueError:
            continue
    if "last_value" not in evaluations:
        raise ValueError("Last-value baseline could not be evaluated.")

    baseline = min(
        (evaluations[name] for name in baseline_methods if name in evaluations),
        key=lambda item: float(item["mae"]),
    )
    selected = baseline
    fallback_reason = "baseline_not_beaten"
    candidates = [evaluations[name] for name in candidate_methods if name in evaluations]
    if candidates:
        best_candidate = min(candidates, key=lambda item: float(item["mae"]))
        baseline_mae = float(baseline["mae"])
        candidate_mae = float(best_candidate["mae"])
        improvement = (
            (baseline_mae - candidate_mae) / baseline_mae if baseline_mae > 0 else 0.0
        )
        if candidate_mae < baseline_mae and improvement >= float(minimum_improvement):
            selected = best_candidate
            fallback_reason = "none"

    method = str(selected["method"])
    point = forecast_by_method(
        history,
        steps,
        method=method,
        season_length=season_length,
        nonnegative=nonnegative,
    )
    residuals = np.asarray(selected["residuals"], dtype=float)
    lower_delta, upper_delta = np.quantile(residuals, [0.1, 0.9])
    lower = point + lower_delta
    upper = point + upper_delta
    if nonnegative:
        lower = np.maximum(lower, 0.0)
        upper = np.maximum(upper, 0.0)
    return {
        "status": "passed",
        "suitability": (
            "suitable"
            if int(selected["origins"]) >= 6
            and int(selected["forecast_points"]) >= max(8, steps * 3)
            else "limited"
        ),
        "method": method,
        "baseline_method": str(baseline["method"]),
        "baseline_result": "improved" if selected is not baseline else "matched_or_fallback",
        "fallback_reason": fallback_reason,
        "point": point.tolist(),
        "lower": lower.tolist(),
        "upper": upper.tolist(),
        "metrics": {
            "mae": float(selected["mae"]),
            "wape": selected["wape"],
            "bias": float(selected["bias"]),
            "origins": int(selected["origins"]),
            "forecast_points": int(selected["forecast_points"]),
        },
    }


def safe_time_diagnostics(values: Iterable[object] | None) -> dict[str, str]:
    if values is None:
        return {
            "time_field": "not_applicable",
            "cadence": "not_applicable",
            "missing_periods": "not_applicable",
            "partial_period": "not_applicable",
        }
    parsed = pd.to_datetime(pd.Series(list(values), dtype="object"), errors="coerce")
    parsed = parsed.dropna().drop_duplicates().sort_values()
    if len(parsed) < 2:
        return {
            "time_field": "not_detected",
            "cadence": "unknown",
            "missing_periods": "unknown",
            "partial_period": "unknown",
        }
    differences = parsed.diff().dropna().dt.total_seconds().to_numpy(dtype=float) / 86400.0
    median_days = float(np.median(differences))
    if 0.5 <= median_days <= 1.5:
        cadence = "daily"
    elif 5 <= median_days <= 9:
        cadence = "weekly"
    elif 25 <= median_days <= 35:
        cadence = "monthly"
    elif 80 <= median_days <= 100:
        cadence = "quarterly"
    elif 350 <= median_days <= 380:
        cadence = "yearly"
    else:
        cadence = "irregular"
    gap_ratio = float(np.mean(differences > max(1.5 * median_days, median_days + 1)))
    missing_periods = "none_detected" if gap_ratio == 0 else "low" if gap_ratio < 0.1 else "material"
    return {
        "time_field": "detected",
        "cadence": cadence,
        "missing_periods": missing_periods,
        "partial_period": "unknown",
    }


def safe_forecast_diagnostics(
    result: Mapping[str, object],
    values: Iterable[object],
    *,
    dates: Iterable[object] | None = None,
    season_length: int | None = None,
) -> dict[str, object]:
    raw = pd.to_numeric(pd.Series(list(values), dtype="object"), errors="coerce")
    usable = raw.dropna().to_numpy(dtype=float)
    count = len(usable)
    history_length = "very_short" if count < 8 else "short" if count < 18 else "moderate" if count < 36 else "long"
    zero_share = float(np.mean(usable == 0)) if count else 0.0
    sparsity = "zero_heavy" if zero_share >= 0.5 else "some_zeros" if zero_share > 0.05 else "dense"
    warnings: list[str] = []
    if count < 4:
        warnings.append("insufficient_history")
    if sparsity == "zero_heavy":
        warnings.append("zero_heavy_target")
    if result.get("fallback_reason") == "baseline_not_beaten":
        warnings.append("baseline_fallback")

    outlier_signal = "unknown"
    trend_signal = "unknown"
    seasonality_signal = "not_applicable" if not season_length else "unknown"
    if count >= 4:
        first, third = np.quantile(usable, [0.25, 0.75])
        spread = third - first
        outlier_signal = (
            "present"
            if spread > 0 and ((usable < first - 1.5 * spread) | (usable > third + 1.5 * spread)).any()
            else "none_detected"
        )
        correlation = float(np.corrcoef(np.arange(count, dtype=float), usable)[0, 1]) if np.std(usable) > 0 else 0.0
        trend_signal = "present" if abs(correlation) >= 0.6 else "weak" if abs(correlation) >= 0.3 else "none_detected"
    if season_length and count >= 2 * int(season_length) and np.std(usable) > 0:
        lag = int(season_length)
        seasonal_correlation = float(np.corrcoef(usable[lag:], usable[:-lag])[0, 1])
        seasonality_signal = "present" if seasonal_correlation >= 0.6 else "weak" if seasonal_correlation >= 0.3 else "none_detected"

    metrics = result.get("metrics") if isinstance(result.get("metrics"), Mapping) else {}
    bias = abs(float(metrics.get("bias", 0.0))) if metrics else 0.0
    scale = float(np.mean(np.abs(usable))) if count else 0.0
    bias_ratio = bias / scale if scale > 0 else None
    bias_band = "unknown" if bias_ratio is None else "low" if bias_ratio < 0.05 else "moderate" if bias_ratio < 0.15 else "high"

    point = np.asarray(result.get("point", []), dtype=float)
    lower = np.asarray(result.get("lower", []), dtype=float)
    upper = np.asarray(result.get("upper", []), dtype=float)
    uncertainty_band = "unknown"
    if len(point) and len(point) == len(lower) == len(upper):
        point_scale = max(float(np.median(np.abs(point))), 1e-12)
        width_ratio = float(np.median(upper - lower)) / point_scale
        uncertainty_band = "narrow" if width_ratio < 0.25 else "moderate" if width_ratio < 0.75 else "wide"

    suitability = str(result.get("suitability") or "insufficient")
    if count < 4:
        suitability = "insufficient"
    elif suitability == "suitable" and (sparsity == "zero_heavy" or outlier_signal == "present"):
        suitability = "limited"
    if outlier_signal == "present":
        warnings.append("outlier_signal")
    if bias_band == "high":
        warnings.append("material_bias")
    if uncertainty_band == "wide":
        warnings.append("wide_uncertainty")

    summary: dict[str, object] = {
        "schema_version": "minimum-intelligence-v1",
        "capabilities": ["clean", "predict"],
        "suitability": suitability,
        "history_length": history_length,
        "sparsity": sparsity,
        "outlier_signal": outlier_signal,
        "trend_signal": trend_signal,
        "seasonality_signal": seasonality_signal,
        "method_family": str(result.get("method") or "not_applicable"),
        "baseline_result": str(result.get("baseline_result") or "not_testable"),
        "bias_band": bias_band,
        "uncertainty_band": uncertainty_band,
        "sensitivity": "not_applicable",
        "fallback_reason": str(result.get("fallback_reason") or "other"),
        "warning_codes": warnings,
    }
    summary.update(safe_time_diagnostics(dates))
    if summary["time_field"] == "not_detected":
        warnings.append("missing_time_field")
    if summary["cadence"] == "irregular":
        warnings.append("irregular_cadence")
    if summary["missing_periods"] == "material":
        warnings.append("missing_periods")
    summary["warning_codes"] = list(dict.fromkeys(warnings))
    return summary


def priority_allocate(
    rows: pd.DataFrame,
    *,
    available: float,
    id_column: str,
    request_column: str,
    priority_column: str,
    integer: bool = False,
) -> tuple[pd.DataFrame, dict[str, object]]:
    required = {id_column, request_column, priority_column}
    missing = sorted(required - set(rows.columns))
    if missing:
        raise ValueError(f"Missing allocation columns: {', '.join(missing)}")
    if rows[id_column].isna().any() or rows[id_column].duplicated().any():
        raise ValueError("Allocation identifiers must be present and unique.")
    requests = pd.to_numeric(rows[request_column], errors="coerce")
    priorities = pd.to_numeric(rows[priority_column], errors="coerce")
    if requests.isna().any() or priorities.isna().any() or (requests < 0).any():
        raise ValueError("Requests and priorities must be valid; requests cannot be negative.")
    capacity = float(available)
    if not np.isfinite(capacity) or capacity < 0:
        raise ValueError("Available capacity must be finite and non-negative.")
    if integer and (capacity % 1 or (requests % 1 != 0).any()):
        raise ValueError("Integer allocation requires whole-unit requests and capacity.")

    planned = rows.copy()
    planned["_request"] = requests.astype(float)
    planned["_priority"] = priorities.astype(float)
    planned["_source_order"] = np.arange(len(planned))
    planned = planned.sort_values(["_priority", "_source_order"], kind="stable")
    remaining = capacity
    allocations: list[float] = []
    for request in planned["_request"]:
        allocated = min(float(request), remaining)
        if integer:
            allocated = float(int(allocated))
        allocations.append(allocated)
        remaining -= allocated
    planned["allocated"] = allocations
    planned["unmet"] = planned["_request"] - planned["allocated"]
    planned = planned.sort_values("_source_order", kind="stable").drop(
        columns=["_request", "_priority", "_source_order"]
    )
    unmet_total = float(planned["unmet"].sum())
    summary = {
        "status": "feasible" if unmet_total == 0 else "infeasible",
        "available": capacity,
        "allocated": float(planned["allocated"].sum()),
        "unused": max(remaining, 0.0),
        "unmet": unmet_total,
    }
    return planned, summary


def weighted_compare(
    rows: pd.DataFrame,
    *,
    id_column: str,
    criteria: Mapping[str, Mapping[str, object]],
) -> pd.DataFrame:
    if id_column not in rows or rows[id_column].isna().any() or rows[id_column].duplicated().any():
        raise ValueError("Comparison identifiers must be present and unique.")
    if not criteria:
        raise ValueError("At least one confirmed criterion is required.")
    result = rows.copy()
    score = np.zeros(len(result), dtype=float)
    total_weight = 0.0
    for column, rule in criteria.items():
        if column not in result:
            raise ValueError(f"Missing comparison criterion: {column}")
        values = pd.to_numeric(result[column], errors="coerce")
        if values.isna().any():
            raise ValueError(f"Criterion {column} contains missing or non-numeric values.")
        direction = str(rule.get("direction") or "")
        if direction not in {"higher", "lower"}:
            raise ValueError(f"Criterion {column} must declare higher or lower as better.")
        weight = float(rule.get("weight") or 0)
        if not np.isfinite(weight) or weight < 0:
            raise ValueError(f"Criterion {column} has an invalid weight.")
        low, high = float(values.min()), float(values.max())
        normalized = np.full(len(values), 0.5) if high == low else (values.to_numpy(dtype=float) - low) / (high - low)
        if direction == "lower":
            normalized = 1.0 - normalized
        score += weight * normalized
        total_weight += weight
    if total_weight <= 0:
        raise ValueError("Comparison weights must have a positive total.")
    result["decision_score"] = score / total_weight
    result = result.sort_values(
        ["decision_score", id_column], ascending=[False, True], kind="stable"
    ).reset_index(drop=True)
    result["decision_rank"] = np.arange(1, len(result) + 1)
    return result


def one_way_sensitivity(
    base_inputs: Mapping[str, float],
    *,
    variable: str,
    values: Sequence[float],
    calculate: Callable[[Mapping[str, float]], float],
) -> pd.DataFrame:
    if variable not in base_inputs:
        raise ValueError(f"Unknown sensitivity variable: {variable}")
    rows: list[dict[str, float]] = []
    for value in values:
        inputs = dict(base_inputs)
        inputs[variable] = float(value)
        rows.append({variable: float(value), "result": float(calculate(inputs))})
    return pd.DataFrame(rows)


def bootstrap_statistic(
    values: Iterable[object],
    *,
    draws: int = 1_000,
    seed: int = 0,
    statistic: Callable[[np.ndarray], float] = np.mean,
) -> np.ndarray:
    sample = _numeric_history(values, minimum=2)
    repetitions = int(draws)
    if repetitions < 100 or repetitions > 100_000:
        raise ValueError("Bootstrap draws must be between 100 and 100000.")
    generator = np.random.default_rng(int(seed))
    output = np.empty(repetitions, dtype=float)
    for index in range(repetitions):
        resample = generator.choice(sample, size=len(sample), replace=True)
        output[index] = float(statistic(resample))
    return output
