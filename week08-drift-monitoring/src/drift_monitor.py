"""
Feature drift monitoring for the vehicle detector — this week's lecture
content (univariate drift, PSI) applied to the detector's own confidence
scores as the monitored feature.

BMD-45's paper reports a real domain-shift finding: the SAME detector
architecture scores ~33.6% mAP when trained on a different dataset and
evaluated on BMD-45's real-world CCTV footage, versus ~83.8% mAP when
trained in-domain on BMD-45 itself. `data/fixtures/camera_A_daylight/` and
`data/fixtures/camera_B_lowlight/` are a synthetic, illustrative stand-in
for that same idea — same detector, two different visual conditions.
Confidence score
is the feature we monitor here because it's the one thing a production
system has at inference time without ground truth labels (which is exactly
why feature/prediction drift monitoring exists — you often don't get labels
in real time).

Fill in the four functions marked # TODO. Constants above them are given.
"""
import glob
import math
import os
import statistics
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mock_detector as det

PSI_MODERATE_THRESHOLD = 0.10
PSI_SIGNIFICANT_THRESHOLD = 0.25
N_BINS = 10


# ---------------------------------------------------------------------------
# Part 1 — Extract the monitored feature (confidence scores) from a camera
# ---------------------------------------------------------------------------

def extract_confidence_scores(camera_dir):
    """Run the detector over every *.jpg image in `camera_dir` (use
    glob.glob(os.path.join(camera_dir, "*.jpg")), sorted for determinism)
    and return a flat list of every detection's confidence score (float)
    across all images in that directory.

    Use Image.open(path).convert("RGB") to load each image, then
    det.detect(image) to get its detections, and collect d.score from each.
    """
    conf_scores = []
    img_paths = sorted(glob.glob(os.path.join(camera_dir, "*.jpg")))
    for path in img_paths:
        with Image.open(path).convert("RGB") as img:
            detections = det.detect(img)
            for d in detections:
                conf_scores.append(float(d.score))
    return conf_scores


# ---------------------------------------------------------------------------
# Part 2 — Population Stability Index between a reference and live distribution
# ---------------------------------------------------------------------------

def compute_psi(reference_scores, live_scores, n_bins=N_BINS):
    """Compute the Population Stability Index between two lists of scores,
    both assumed to lie in [0.0, 1.0] (confidence scores).

    Steps:
      1. Split [0.0, 1.0] into `n_bins` equal-width bins.
      2. For each bin, compute the PROPORTION (count / total) of
         reference_scores and of live_scores that fall in it. A score of
         exactly 1.0 belongs in the last bin.
      3. To avoid division by zero / log(0) for empty bins, clamp every
         proportion to a minimum of 1e-4 before using it in the ratio/log
         below.
      4. PSI = sum over bins of (live_pct - ref_pct) * ln(live_pct / ref_pct)
      5. Return the PSI value (float). Larger values mean more drift; PSI
         is 0 when the two distributions are identical.
    """
    bin_width = 1.0 / n_bins
    ref_counts = [0] * n_bins
    live_counts = [0] * n_bins

    def get_bin_index(score):
        if score >= 1.0:
            return n_bins - 1
        idx = int(score // bin_width)
        if idx >= n_bins:
            idx = n_bins - 1
        elif idx < 0:
            idx = 0
        return idx

    for s in reference_scores:
        ref_counts[get_bin_index(s)] += 1
        
    for s in live_scores:
        live_counts[get_bin_index(s)] += 1

    total_ref = len(reference_scores)
    total_live = len(live_scores)
    
    psi_value = 0.0
    for i in range(n_bins):
        ref_pct = max(ref_counts[i] / total_ref, 1e-4) if total_ref > 0 else 0.0
        live_pct = max(live_counts[i] / total_live, 1e-4) if total_live > 0 else 0.0
        psi_value += (live_pct - ref_pct) * math.log(live_pct / ref_pct) 
    return psi_value


# ---------------------------------------------------------------------------
# Part 3 — Turn a PSI value into an actionable label
# ---------------------------------------------------------------------------

def classify_drift(psi):
    """Standard PSI interpretation bands:
      psi < PSI_MODERATE_THRESHOLD           -> "none"
      PSI_MODERATE_THRESHOLD <= psi < PSI_SIGNIFICANT_THRESHOLD -> "moderate"
      psi >= PSI_SIGNIFICANT_THRESHOLD       -> "significant"

    Return one of those three strings.
    """
    if psi < PSI_MODERATE_THRESHOLD:
        return "none"
    elif psi < PSI_SIGNIFICANT_THRESHOLD:
        return "moderate"
    else:
        return "significant"


# ---------------------------------------------------------------------------
# Part 4 — Summary statistics for a score distribution (for the report)
# ---------------------------------------------------------------------------

def summarize_scores(scores):
    """Return a dict: {"count": int, "mean": float, "std": float,
    "min": float, "max": float}, all rounded to 4 decimal places except
    count. Use the `statistics` module (mean, stdev — if len(scores) < 2,
    std should be 0.0 rather than raising).
    """
    count = len(scores)
    if count == 0:
        return {"count": 0, "mean": 0.0, "std": 0.0, "min": 0.0, "max": 0.0}
        
    mean_val = statistics.mean(scores)
    min_val = min(scores)
    max_val = max(scores)
    std_val = 0.0 if count < 2 else statistics.stdev(scores)
        
    return {
        "count": count,
        "mean": round(mean_val, 4),
        "std": round(std_val, 4),
        "min": round(min_val, 4),
        "max": round(max_val, 4)
    }
