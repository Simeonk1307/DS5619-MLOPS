# NOTES.md — Week 11: Model Compression Benchmark

**Student ID used with `generate_for_student.py`:**
<!-- paste the --student-id value you used -->
112301031


## pruned_dense_fp32 vs. pruned_sparse_coo

<!-- Compare pruned_dense_fp32 and pruned_sparse_coo in your report — same
     weights, same accuracy, very different size_bytes. Explain why in your
     own words (tie it to the lecture's pruning pitfall). -->
as the same pruned weights weights are used accuracy is also same

pruned_dense_fp32 stores all 256 slots hence 256*4 1024 size_bytes

pruned_sparse_coo stores only 77 non-zero weights with 4 byte value and index hence 77*8 616 size_bytes

pruning saves space only if you use sparse format otherwise there will be no saving and it will beat dense only if the size_bytes is lesser in sparse


## The 0.95-sparsity experiment

<!-- Try editing PRUNE_SPARSITY in src/run_pipeline.py to 0.95 and re-run —
     what happens to accuracy, and why does that make sense given only 40
     of the 256 weights are actually informative? -->

```
(.venv) (base) simeonk1307@fedora:~/Documents/Projects/DS5619-MLOPS/week11-model-compression$ python src/run_pipeline.py
label                  size_bytes   ratio  accuracy  latency_ms
baseline_fp32                1024   1.00x   100.00%      1.8248
pruned_dense_fp32            1024   1.00x    82.67%      1.9236
pruned_sparse_coo             104   9.85x    82.67%      1.9236
quantized_int8                256   4.00x    99.33%      1.9038

Wrote /var/home/simeonk1307/Documents/Projects/DS5619-MLOPS/week11-model-compression/compression_report.json
(.venv) (base) simeonk1307@fedora:~/Documents/Projects/DS5619-MLOPS/week11-model-compression$ python src/run_pipeline.py
label                  size_bytes   ratio  accuracy  latency_ms
baseline_fp32                1024   1.00x   100.00%      1.7889
pruned_dense_fp32            1024   1.00x    99.33%      1.8853
pruned_sparse_coo             616   1.66x    99.33%      1.8853
quantized_int8                256   4.00x    99.33%      1.8633

Wrote /var/home/simeonk1307/Documents/Projects/DS5619-MLOPS/week11-model-compression/compression_report.json
```


Accuracy decreases on increasing the PRUNE_SPARSITY to 0.95

0.95*256 = 243 means only 13 are informative
40 are truly informative so by over compression we are losing the other 27 informative weights also hence a drop in the loss

true threshold will be 1-40/256 ~ 84%
