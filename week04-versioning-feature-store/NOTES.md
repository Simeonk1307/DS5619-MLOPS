# NOTES.md — Week 4: Versioning, Feature Store & Lineage

**Student ID used with `generate_for_student.py`:**
<!-- paste the --student-id value you used -->
112301031


## v1 vs. v2 manifest comparison

<!-- What's different between the v1 and v2 feature group's manifest.json?
     (Look at both.) -->
different fields: `feature_group_version_id`, `source_raw_version_id`, `row_count`  
another difference: `transform_version` does not match `source_raw_version_id` for v2.


## Why treat amount_minor_units differently from amount?

<!-- Why does build_features need to treat amount_minor_units differently
     from amount for the aggregates to be comparable across versions? -->

because to aggregate and compare they should be in the same unit scale to be made sense of so to standardize the units we need to treat them differently.
