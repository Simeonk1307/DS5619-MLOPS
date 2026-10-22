## What was done

Implemented in `compression2.py` (pure Python, no dependencies):

| Function | Purpose |
|---|---|
| `model_size_bytes` | `len(weights) * dtype_bytes` |
| `prune_weights` | Magnitude pruning: zero the `int(sparsity * n)` smallest-`|w|` weights; returns a new list |
| `sparse_coo_size_bytes` | `nonzero_count * (value_bytes + index_bytes)` |
| `quantize_int8` | Symmetric INT8: `scale = max|w| / 127`, `q = clamp(round(w / scale), -127, 127)`; all-zero input gives `scale = 1.0` |
| `benchmark_model` | Returns size, accuracy, and average latency (ms per pass) |

`run_pipeline.py` benchmarks four variants on 256 weights and 300 eval examples.

## Results (sparsity = 0.7)

| Variant | Size (bytes) | Accuracy | Ratio vs baseline |
|---|---|---|---|
| baseline_fp32 | 1024 | 1.0000 | 1.00 |
| pruned_dense_fp32 | 1024 | 0.9933 | 1.00 |
| pruned_sparse_coo | 616 | 0.9933 | 1.66 |
| quantized_int8 | 256 | 0.9933 | 4.00 |

- Dense pruning saves nothing: zeros still take 4 bytes each.
- COO stores 77 non-zeros at 8 bytes each (value + index) = 616 bytes. It beats dense only below 128 non-zeros (sparsity above 50%).
- Latency is about 1.7 to 1.8 ms in all rows. The Python loop still visits all 256 entries, so size shrinks but speed does not.

## Issues faced

1. **12 of 13 tests failed with `AttributeError: module 'compression' has no attribute ...`.**
   Cause: Python 3.14 ships a standard-library package named `compression`. `import compression` loaded that empty package instead of the project file.
   Check: `compression.__file__` pointed to `.../python3.14/compression/__init__.py`.
2. **Pipeline test still failed after the unit tests passed.**
   Cause: the test runs `run_pipeline.py` in a separate process (copied `src/` and `data/` to a temp folder), which hit the same name clash.
3. **Fix:** renamed the module to `compression2.py` and updated every `import compression as comp` to `import compression2 as comp` in `src/run_pipeline.py` and `tests/test_smoke.py`. A unique name cannot be shadowed by the standard library.
4. **Minor:** `py` is not a command on Fedora; used `python3`.

