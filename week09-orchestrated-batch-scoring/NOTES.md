# NOTES.md — Week 9: Orchestrated Batch Scoring

**Student ID used with `generate_for_student.py`:**
<!-- paste the --student-id value you used -->
112301031


## notify retry count

<!-- How many attempts did notify take in your run? (Check
     dag_run_summary.json.) -->
3


## Branch independence

<!-- Why does load still succeed even though notify — its "sibling" in the
     DAG — failed on its first two attempts? What does that tell you about
     how failures in one branch of a DAG should (or shouldn't) affect an
     unrelated branch? -->
load is independent of notify
failures in one branch of a dag should not affect an unrelated branch


## Retry cost under FinOps

<!-- Tying back to this week's FinOps content: if notify were a metered API
     call you paid for per attempt, what would you change about the retry
     strategy, and why is "retry every failed task the same way" a risky
     default once cost enters the picture? -->
I would implement an exponential backoff with jitter and an attempt ceiling,

Because Not all retry will be equally priced some may be much more expensive than the others so blind retries without fixing the underlying issue will just rack massive cost.
