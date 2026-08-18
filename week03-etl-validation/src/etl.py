"""
Extract -> Validate -> Transform -> Load pipeline for the fraud transaction
data. Run with:

    python src/etl.py --config config.yaml

(a default config.yaml pointing at data/raw_transactions.csv is provided)
"""
import argparse
import csv
import json
import os
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import expectations as exp

def write_csv(output_path, rows):
    """Writes a list of dictionaries to a CSV file."""
    if not rows:
        with open(output_path, mode='w', newline='') as f:
            f.write("") 
        return

    fieldnames = list(rows[0].keys())
    with open(output_path, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


KNOWN_CATEGORIES = {
    "grocery", "electronics", "fuel", "travel", "restaurant",
    "online_retail", "utilities", "pharmacy", "entertainment", "atm_withdrawal",
}


def build_expectation_suite():
    """The data contract for this dataset. Each entry says which expectation
    function to run, and with what arguments. This is provided — read it to
    know exactly what your expectation functions in expectations.py need to
    handle correctly.
    """
    return [
        (exp.expect_column_not_null, {"column": "amount"}),
        (exp.expect_column_not_null, {"column": "card_id"}),
        (exp.expect_column_positive, {"column": "amount"}),
        (exp.expect_column_in_set, {"column": "merchant_category", "allowed_values": KNOWN_CATEGORIES}),
        (exp.expect_column_unique, {"column": "transaction_id"}),
    ]


def extract(input_path):
    with open(input_path, newline="") as f:
        return list(csv.DictReader(f))

def run_etl(config):
    """Implement the four ETL steps described in ASSIGNMENT.md:
    extract, validate (run every expectation in build_expectation_suite()
    and collect ALL violations, not just the first), transform (split into
    clean vs quarantined rows — a row with ANY violation is quarantined),
    load (write clean_output_path, quarantine_output_path, and
    report_output_path as described in the assignment).

    Return the validation_report dict as well as writing it to disk.
    """
    rows = extract(config["input_path"])
    
    violations, validation_report = [], {"expectations": {}}
    for fn, args in build_expectation_suite():
        violations.extend(fn(rows, **args))
        validation_report["expectations"][fn.__name__] = {"n_violations": 0, "row_indices": []}
    
    quarantined_row_indices = set()
    for v in violations:
        quarantined_row_indices.add(v.row_index)
        if v.expectation in validation_report["expectations"]:
            validation_report["expectations"][v.expectation]["n_violations"] += 1
            if v.row_index not in validation_report["expectations"][v.expectation]["row_indices"]:
                validation_report["expectations"][v.expectation]["row_indices"].append(v.row_index)

    clean_rows = []
    quarantined_rows = []
    for i, row in enumerate(rows):
        if i in quarantined_row_indices:
            quarantined_rows.append(row)
        else:
            clean_rows.append(row)

    final_report = {
        "expectations": list(validation_report["expectations"].values())
    }
    
    write_csv(config["clean_output_path"], clean_rows)
    write_csv(config["quarantine_output_path"], quarantined_rows)
    
    with open(config["report_output_path"], "w") as f:
        json.dump(final_report, f, indent=4, ensure_ascii=False)
    
    return final_report

"""
Extract -> Validate -> Transform -> Load pipeline for the fraud transaction
data. Run with:

    python src/etl.py --config config.yaml

(a default config.yaml pointing at data/raw_transactions.csv is provided)
"""
import argparse
import csv
import json
import os
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import expectations as exp

def write_csv(output_path, rows):
    """Writes a list of dictionaries to a CSV file."""
    if not rows:
        with open(output_path, mode='w', newline='') as f:
            f.write("") 
        return

    fieldnames = list(rows[0].keys())
    with open(output_path, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


KNOWN_CATEGORIES = {
    "grocery", "electronics", "fuel", "travel", "restaurant",
    "online_retail", "utilities", "pharmacy", "entertainment", "atm_withdrawal",
}


def build_expectation_suite():
    """The data contract for this dataset. Each entry says which expectation
    function to run, and with what arguments. This is provided — read it to
    know exactly what your expectation functions in expectations.py need to
    handle correctly.
    """
    return [
        (exp.expect_column_not_null, {"column": "amount"}),
        (exp.expect_column_not_null, {"column": "card_id"}),
        (exp.expect_column_positive, {"column": "amount"}),
        (exp.expect_column_in_set, {"column": "merchant_category", "allowed_values": KNOWN_CATEGORIES}),
        (exp.expect_column_unique, {"column": "transaction_id"}),
    ]


def extract(input_path):
    with open(input_path, newline="") as f:
        return list(csv.DictReader(f))

def run_etl(config):
    """Implement the four ETL steps described in ASSIGNMENT.md:
    extract, validate (run every expectation in build_expectation_suite()
    and collect ALL violations, not just the first), transform (split into
    clean vs quarantined rows — a row with ANY violation is quarantined),
    load (write clean_output_path, quarantine_output_path, and
    report_output_path as described in the assignment).

    Return the validation_report dict as well as writing it to disk.
    """
    rows = extract(config["input_path"])
    
    violations = []
    temp_suite = {}
    for fn, args in build_expectation_suite():
        violations.extend(fn(rows, **args))
        # Keep track of the expectation name within the dictionary structure
        temp_suite[fn.__name__] = {
            "expectation": fn.__name__,
            "n_violations": 0, 
            "row_indices": []
        }
    
    quarantined_row_indices = set()
    for v in violations:
        quarantined_row_indices.add(v.row_index)
        if v.expectation in temp_suite:
            temp_suite[v.expectation]["n_violations"] += 1
            if v.row_index not in temp_suite[v.expectation]["row_indices"]:
                temp_suite[v.expectation]["row_indices"].append(v.row_index)

    clean_rows = []
    quarantined_rows = []
    for i, row in enumerate(rows):
        if i in quarantined_row_indices:
            quarantined_rows.append(row)
        else:
            clean_rows.append(row)
    
    write_csv(config["clean_output_path"], clean_rows)
    write_csv(config["quarantine_output_path"], quarantined_rows)
    
    # Formatted exactly as a list of dicts to satisfy the pytest verification loop
    validation_report = {
        "expectations": list(temp_suite.values())
    }
    
    with open(config["report_output_path"], "w") as f:
        json.dump(validation_report, f, indent=4, ensure_ascii=False)
    
    return validation_report




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()

    with open(args.config) as f:
        config = yaml.safe_load(f)

    report = run_etl(config)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
