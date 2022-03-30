# snj-benchmarking
## Getting started
1. Install dependencies
    ```
    pip install git+https://github.com/aizeny/snj
    pip install git+https://github.com/aizeny/stdr
    ``` 
2. Check `./benchmarking/` for runs that already have a CSV output of metrics. If you just want to plot, run the cells that load CSVs and plot boxplots at the end. No need to run the lengthy loops.
## Adding an implementation to benchmark
1. Each new test requires this cell to be run. The `BenchmarkModule` class contains most of the code required to run vanilla cassiopeia solvers.
```python
nj_plain = BenchmarkModule(
    test_name = "nj_plain",
    gt_trees_dir = in_folder,
    numtrees = 50,
    out_basefolder = out_folder,
)

nj_plain.reconstruct(overwrite=False)
nj_plain.evaluate(overwrite=False)
```
2. Since the tests you add are probably not vanilla, you will have to edit some methods by creating a subclass of `BenchmarkModule` and using that to run instead. The `benchmark_module.py` file contains the source code for the class, which you can override. The most common method to override is `run_solver`, but you might also need to override `__init__` and `get_cm`. 
3. For example, loading my simulated trees (as opposed to Richard's) involves getting the ground truth character matrix from each ground truth tree (Richard has a cm.txt for each tree). Therefore I would just override my `get_cm` method with this:
```python
class GroundTruthCMBM(BenchmarkModule):
    def get_cm(self, i):
        gt_tree = self.get_gt_tree(i)
        cm = gt_tree.character_matrix

        return cm
```
and use it this way:
```python
nj_plain_2 = GroundTruthCMBM(
    test_name = "nj_plain_2",
    gt_trees_dir = in_folder_2,
    numtrees = 50,
    out_basefolder = out_folder,
)

nj_plain_2.reconstruct(overwrite=True)
nj_plain_2.evaluate(overwrite=True)
```
