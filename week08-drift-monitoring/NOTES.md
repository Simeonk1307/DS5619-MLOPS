# NOTES.md — Week 8: Drift and Observability Monitoring

**Student ID used with `generate_for_student.py`:**
<!-- paste the --student-id value you used -->
112301031


## Drift level vs. expectation

<!-- What drift level did the report show, and does that match what you'd
     expect given the two cameras were built with deliberately different
     visual statistics? -->
moderate drift level
yes it is as expected.


## What confidence-score-only monitoring misses

<!-- What would you monitor IN ADDITION to confidence score if you had
     access to ground-truth labels a day later? (Tie this to the kinds of
     drift from the lecture — which one does confidence-score-only
     monitoring miss?) -->
We can monitor accuracy, precision/recall per class, and a confusion matrix, and compare them over time.

We can look into label drift and concept drift.

Confidence-score based monitoring misses concept drift.
Confidence score reflects only how familiar an input looks to the model, not whether the prediction is actually correct. 
Under concept drift, the input distribution stays the same but the true input-to-label relationship changes, so the model can still produce high-confidence predictions that are now wrong.
