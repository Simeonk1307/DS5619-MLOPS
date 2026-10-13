# NOTES.md — Week 10: Fairness and Robustness Audit

**Student ID used with `generate_for_student.py`:**
<!-- paste the --student-id value you used -->
112301031


## Which classes got flagged?

<!-- Which classes got flagged, and does that match what you'd expect given how generate_for_student.py built the fixtures? -->
Bicycle, Two-wheeler & Three-wheeler were flagged below the 0.90 recall threshold.
yes as they are small vehicles


## If the grouping variable were a protected attribute

<!-- Tying back to the framing note: what would change about this audit's
     stakes and your obligations as an engineer if the grouping variable
     were a protected demographic attribute instead of a vehicle class? -->
There could be ethical and legal problems which could later lead to financial losses.
if it works bad for certain group then there could be safety issues


## Which attack could corrupt this audit?

<!-- Name one lifecycle stage and attack from the lecture (data poisoning,
     model theft, or adversarial examples) that could silently corrupt THIS
     audit's result, and one control from the lecture that would reduce the
     risk. -->
Data Poisoning (Training/Testing Stage)
Cryptographic Integrity Verification (by hashing the datasets before running the audit)


## Would SHAP or LIME explain a missed detection?

<!-- Pick one missed ground-truth box in a flagged class. An auditor asks
     you to explain WHY the detector missed it, not just that it did. Would
     SHAP or LIME actually help you answer that for a bounding-box detector
     — and if not, what's different about this detector's inputs/outputs
     that breaks the assumption both tools make? -->
No.
* Output Mismatch: They require a scalar. A missed object yields no score to attribute feature importance to.
* Input Mismatch: Perturbation-based explainers evaluate changes to existing predictions; they cannot explain why a non-existent box was never proposed.


## What did your attack show?

<!-- Using fairness_report.json["adversarial"]: at what eps does each flagged
     class fall further? Which class is most fragile, and is it the same
     class the clean audit flagged? Compare the drop ranking
     (most_fragile) with lowest_recall_under_attack — do they agree, and
     which is the better measure of who is hurt? What does that say about who bears the
     cost of an attack (or of an unmonitored failure)? Then: what would
     adversarial training or input validation look like for this detector,
     and why does a rule this simple break so much more easily than a CNN
     (or does it)? -->

* **Eps Thresholds:** **Bicycle** drops 0.8462 $\rightarrow$ 0.2308 ($\epsilon=0 \rightarrow 40$); **Two-wheeler** drops 0.8500 $\rightarrow$ 0.3000; **Three-wheeler** holds until $\epsilon=20$ (0.8889) then falls to 0.5000 ($\epsilon=40$).
* **Fragility:** At $\epsilon=20$, **Truck** has the biggest drop (0.4167), followed by **Bicycle** (0.3847) and **Mini-bus** (0.3571).
* **Drop vs. Absolute Recall:** They disagree (`most_fragile` = Truck, Bicycle, Mini-bus vs. `lowest_recall` = Bicycle, Truck, Two-wheeler). **Lowest absolute recall** is the better measure of harm because safety depends on actual detection, not relative loss.
* **Cost of Failure:** Vulnerable road users (cyclists/riders) bear the physical safety risk, masked by high overall average accuracy.
* **Rule vs. CNN Brittleness:** Hardcoded rules ($R > 120, R-G > 40$) break instantly when $\epsilon$ shifts pixels past static boundaries. CNNs resist simple color shifts better by extracting spatial features and textures.
* **Mitigations:** Normalize color channels (input validation) and include perturbed $\pm\epsilon$ samples during rule/model training (adversarial training).