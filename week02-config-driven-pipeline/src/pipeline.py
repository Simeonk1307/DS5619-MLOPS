"""
The "after" version — YOUR file to complete.

Fill in the three functions marked with # TODO. Everything else (CLI wiring,
imports) is already done for you. Do not hardcode any path, format string, or
threshold value anywhere in this file — if you find yourself typing a literal
number or file path outside of a default/example, it belongs in the config
file instead.

Run with:
    python src/pipeline.py --config config/pipeline.yaml
"""
import argparse
import csv
import json
from pathlib import Path
import yaml

REQUIRED_KEYS = ["input_path", "input_format", "high_value_threshold", "output_path"]


def load_config(path):
    """Load a YAML config file and validate required keys are present.

    Must raise ValueError naming the specific missing key if REQUIRED_KEYS
    are not all present. Do not let this fail with a bare KeyError later.
    """
    with open(path, "r") as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)

    data = data or {}
    
    missing = [key for key in REQUIRED_KEYS if key not in data]
    if missing:
        raise ValueError(f"{missing} required keys are missing in the yaml file")

    return data



def load_transactions(path, fmt):
    """Load transactions from `path`, using `fmt` ("csv" or "json") to decide
    how to parse it — not by sniffing the file extension.

    Must return a list of dicts. Every dict must have at least "amount"
    (str or float) and "is_fraud" (str "True"/"False" or bool).
    Raise ValueError for any fmt other than "csv" or "json".
    """
    if fmt not in ("csv", "json"):
        raise ValueError(f"{fmt} is not a supported input_format")

    data = dict()
    if fmt == "csv":
        with open(path, "r", newline="") as f:
            reader = csv.DictReader(f)
            data = list(reader)
    else:
        with open(path, "r") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError(f"{path}: expected a JSON list of transactions")

    for i, d in enumerate(data):
        if not isinstance(d, dict):
            raise ValueError(f"{path}: row {i} is not an object (got {type(d).__name__})")
        if "amount" not in d or "is_fraud" not in d:
            raise ValueError(f"{path}: row {i} missing 'amount' and/or 'is_fraud'")
        if not isinstance(d["amount"], (str, float, int)):
            raise ValueError(f"{path}: row {i} 'amount' must be str or float, got {type(d['amount']).__name__}")
        if not isinstance(d["is_fraud"], (str, bool)):
            raise ValueError(f"{path}: row {i} 'is_fraud' must be str or bool, got {type(d['is_fraud']).__name__}")

    return data
            


def run_pipeline(config):
    """Load data per `config`, compute the same summary fields as
    pipeline_hardcoded.py (n_transactions, total_amount, fraud_rate,
    n_high_value, high_value_threshold), and write them as JSON to
    config["output_path"]. Return the report dict as well.
    """
    
    rows = load_transactions(config["input_path"], config["input_format"])
    n = len(rows)
    threshold = config["high_value_threshold"]

    total_amount = sum(float(r["amount"]) for r in rows)
    n_fraud = sum(1 for r in rows if str(r["is_fraud"]).lower() == "true")
    n_high_value = sum(1 for r in rows if float(r["amount"]) > threshold)

    report = {
        "n_transactions": n,
        "total_amount": round(total_amount, 2),
        "fraud_rate": round(n_fraud / n, 4) if n else 0.0,
        "n_high_value": n_high_value,
        "high_value_threshold": threshold,
    }

    with open(config["output_path"], "w") as f:
        json.dump(report, f, indent=2)

    print(f"Wrote report to {config['output_path']}")
    return report

    


def main():
    parser = argparse.ArgumentParser(description="Config-driven fraud transaction summary pipeline")
    parser.add_argument("--config", required=True, help="Path to a YAML config file")
    args = parser.parse_args()

    config = load_config(args.config)
    report = run_pipeline(config)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
