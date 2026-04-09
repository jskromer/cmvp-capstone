#!/usr/bin/env python3
"""
M&V Regression Validation Utility

Validates key statistical thresholds for inverse (regression) models
used in whole-facility M&V approaches.

Usage:
    python regression_check.py --cv 18.5 --r2 0.85 --n 12 --coefficients 2.5 3.1
    python regression_check.py --sample-size --cv 30 --precision 10 --confidence 90
"""

import argparse
import math
import sys
import json


# ASHRAE Guideline 14 thresholds
THRESHOLDS = {
    "monthly": {"cv_rmse": 25.0, "nmbe": 5.0},
    "daily": {"cv_rmse": 35.0, "nmbe": 10.0},
    "hourly": {"cv_rmse": 50.0, "nmbe": 10.0},
}

# t-values for 90% confidence (two-tailed) by degrees of freedom
T_VALUES_90 = {
    5: 2.015, 6: 1.943, 7: 1.895, 8: 1.860, 9: 1.833,
    10: 1.812, 11: 1.796, 12: 1.782, 15: 1.753, 20: 1.725,
    30: 1.697, 60: 1.671, 120: 1.658,
}


def get_t_value(df, confidence=90):
    """Get t-value for given degrees of freedom at specified confidence."""
    if confidence != 90:
        raise ValueError("Only 90% confidence is currently supported")
    if df in T_VALUES_90:
        return T_VALUES_90[df]
    # Interpolate or use closest
    keys = sorted(T_VALUES_90.keys())
    if df < keys[0]:
        return T_VALUES_90[keys[0]]
    if df > keys[-1]:
        return 1.645  # z-value approximation for large samples
    for i in range(len(keys) - 1):
        if keys[i] <= df <= keys[i + 1]:
            frac = (df - keys[i]) / (keys[i + 1] - keys[i])
            return T_VALUES_90[keys[i]] * (1 - frac) + T_VALUES_90[keys[i + 1]] * frac
    return 1.645


def check_regression(cv_rmse, r_squared, n_points, t_stats, interval="monthly"):
    """Validate regression model against ASHRAE Guideline 14 thresholds."""
    results = {"pass": True, "checks": []}
    thresholds = THRESHOLDS.get(interval, THRESHOLDS["monthly"])

    # CV(RMSE) check
    cv_pass = cv_rmse <= thresholds["cv_rmse"]
    results["checks"].append({
        "metric": "CV(RMSE)",
        "value": cv_rmse,
        "threshold": thresholds["cv_rmse"],
        "pass": cv_pass,
        "note": f"{'PASS' if cv_pass else 'FAIL'}: {cv_rmse:.1f}% vs {thresholds['cv_rmse']}% threshold ({interval})"
    })
    if not cv_pass:
        results["pass"] = False

    # R-squared check (informational, not a hard threshold)
    r2_note = "Adequate" if r_squared >= 0.75 else "Low -- investigate model form"
    results["checks"].append({
        "metric": "R-squared",
        "value": r_squared,
        "threshold": "0.75 (guideline, not hard threshold)",
        "pass": r_squared >= 0.75,
        "note": f"{r2_note}: R² = {r_squared:.3f}"
    })

    # t-statistic checks
    for i, t in enumerate(t_stats):
        t_pass = abs(t) >= 2.0
        results["checks"].append({
            "metric": f"t-statistic (coefficient {i + 1})",
            "value": t,
            "threshold": 2.0,
            "pass": t_pass,
            "note": f"{'PASS' if t_pass else 'FAIL'}: |t| = {abs(t):.2f} vs 2.0 threshold"
        })
        if not t_pass:
            results["pass"] = False

    # Degrees of freedom warning
    p = len(t_stats) + 1  # coefficients + intercept
    df = n_points - p
    if df < 5:
        results["checks"].append({
            "metric": "Degrees of freedom",
            "value": df,
            "threshold": 5,
            "pass": False,
            "note": f"WARNING: Only {df} degrees of freedom (n={n_points}, p={p}). Results unreliable."
        })
        results["pass"] = False

    return results


def required_sample_size(cv, precision, confidence=90):
    """
    Calculate required sample size for M&V sampling.

    n = (t * CV / precision)^2

    Args:
        cv: Coefficient of variation (%)
        precision: Desired precision (%)
        confidence: Confidence level (default 90%)

    Returns:
        dict with n, t_value, and formula details
    """
    # Start with large-sample t-value, iterate
    t = 1.645  # initial estimate (large sample)
    for _ in range(10):
        n = math.ceil((t * cv / precision) ** 2)
        df = max(n - 1, 1)
        t = get_t_value(df, confidence)
        n_new = math.ceil((t * cv / precision) ** 2)
        if n_new == n:
            break
        n = n_new

    return {
        "n": n,
        "t_value": round(t, 3),
        "cv": cv,
        "precision": precision,
        "confidence": confidence,
        "formula": f"n = ({t:.3f} x {cv} / {precision})^2 = {n}"
    }


def main():
    parser = argparse.ArgumentParser(description="M&V Regression Validation")
    parser.add_argument("--cv", type=float, help="CV(RMSE) percentage")
    parser.add_argument("--r2", type=float, help="R-squared value")
    parser.add_argument("--n", type=int, help="Number of data points")
    parser.add_argument("--coefficients", type=float, nargs="+",
                        help="t-statistics for model coefficients")
    parser.add_argument("--interval", default="monthly",
                        choices=["monthly", "daily", "hourly"],
                        help="Data interval (default: monthly)")
    parser.add_argument("--sample-size", action="store_true",
                        help="Calculate required sample size instead")
    parser.add_argument("--precision", type=float, default=10,
                        help="Desired precision %% (default: 10)")
    parser.add_argument("--confidence", type=int, default=90,
                        help="Confidence level (default: 90)")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")

    args = parser.parse_args()

    if args.sample_size:
        if not args.cv:
            parser.error("--cv is required for sample size calculation")
        result = required_sample_size(args.cv, args.precision, args.confidence)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"\nSample Size Calculation")
            print(f"{'=' * 40}")
            print(f"CV:          {result['cv']}%")
            print(f"Precision:   {result['precision']}%")
            print(f"Confidence:  {result['confidence']}%")
            print(f"t-value:     {result['t_value']}")
            print(f"Required n:  {result['n']}")
            print(f"Formula:     {result['formula']}")
    else:
        if not all([args.cv, args.r2 is not None, args.n, args.coefficients]):
            parser.error("--cv, --r2, --n, and --coefficients are all required")
        result = check_regression(args.cv, args.r2, args.n, args.coefficients, args.interval)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"\nRegression Validation ({args.interval} data)")
            print(f"{'=' * 50}")
            for check in result["checks"]:
                print(f"  {check['note']}")
            print(f"\nOverall: {'PASS' if result['pass'] else 'FAIL'}")


if __name__ == "__main__":
    main()
