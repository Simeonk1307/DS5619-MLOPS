# NOTES.md — Week 5: Model Registry Governance

**Student ID used with `generate_for_student.py`:**
<!-- paste the --student-id value you used -->
112301031


## Which candidate reached Production, and why?

<!-- Which candidate ended up in Production, and why? -->
v2 reached production because the f1 of v2 model exceeded the set threshold of 0.7 (promote model has this gate)


## Gating stale feature data

<!-- What would you need to add to promote_model's gate if you also wanted
     to block promotion of a model trained on stale (e.g. >30-day-old)
     feature data? -->
The model card should have the least event time of a transaction also stored.
We will check if datetime.now(timezone.utc) - training_end).days > 30 then raise governance error else accept


## Scaling the gate to 40 candidates

<!-- Tying back to this week's AutoML/HPO framing: if a hyperparameter
     search had handed you 40 candidates instead of 2, what in your
     register_model/promote_model design would need to change (or
     genuinely wouldn't) to gate 40 instead of 2? -->

register_model and promote_model i think scales well and does not need any change as the registry gives version and the way registry is used.

manually writing model cards and doing promotion for all 40 would be bad instead only the top candidate can be first shown and then promoted.




