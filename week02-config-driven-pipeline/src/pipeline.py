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
    try:
        with open(path, 'r') as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
    except Exception as err:
        print(f"Loading Error: {err}")
        exit(1)
    
    missing = []
    for key in REQUIRED_KEYS:
        if key not in data.keys():
            missing.append(key)
    
    if missing != []:
        raise ValueError(f"[{', '.join(missing)}] required keys are missing in the yaml file")



def load_transactions(path, fmt):
    """Load transactions from `path`, using `fmt` ("csv" or "json") to decide
    how to parse it — not by sniffing the file extension.

    Must return a list of dicts. Every dict must have at least "amount"
    (str or float) and "is_fraud" (str "True"/"False" or bool).
    Raise ValueError for any fmt other than "csv" or "json".
    """
    if fmt not in ["csv", "json"]:
        raise ValueError(f"{fmt} is not compatible")
    try:
        goodPath = Path(path)
    except Exception as err:
        raise ValueError(f"{path} is not Path-compliant")
    
    if ('.'+fmt) != goodPath.suffix:
        raise Exception(f"'{'.'}'+fmt i.e ({'.'+fmt}) does not match the extension {goodPath.suffix}")
    
    if fmt == "csv":
        try:
            with open(path, "r", newline="") as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception as err:
            print(f"Loading error: {err}")
            exit(1)
    else:
        try:
            with open(path, "r") as f:
                data = json.load(f)
                return list(data)
        except Exception as err:
            print(f"Loading error: {err}")
            exit(1)
            


def run_pipeline(config):
    """Load data per `config`, compute the same summary fields as
    pipeline_hardcoded.py (n_transactions, total_amount, fraud_rate,
    n_high_value, high_value_threshold), and write them as JSON to
    config["output_path"]. Return the report dict as well.
    """
    # TODO: implement
    raise NotImplementedError("run_pipeline is not implemented yet")


def main():
    parser = argparse.ArgumentParser(description="Config-driven fraud transaction summary pipeline")
    parser.add_argument("--config", required=True, help="Path to a YAML config file")
    args = parser.parse_args()

    config = load_config(args.config)
    report = run_pipeline(config)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
