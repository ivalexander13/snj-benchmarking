# snj-benchmarking
## Getting started
1. Install dependencies
    ```
    pip install git+https://github.com/aizeny/snj
    pip install git+https://github.com/aizeny/stdr
    ``` 
2. Check `./benchmarking/` for runs that already have a CSV output of metrics. If you just want to plot, run the cells that load CSVs and plot boxplots at the end. No need to run the lengthy loops.
## Adding an implementation to benchmark
1. Each implementation's benchmark consists of two cells:
    1. The loop that reconstructs the tree (10-20 mins)
    2. The loop that loads the reconstructed and ground truth trees (5-6 mins)
2. Copy these two cells (along with the header) and change these variables:

    **First cell:**
    - The solver. The tree `recon_tree` is a CassiopeiaTree
    - Add a `SUBDIR/` to output path: (IMPORTANT!)
        ```
        with open(out_folder + 'SUBDIR/' + "recon" + str(i), "w+") as f:
        ```
    **Second Cell:**
    - Add a suffix to the dataframes `RF` and `triplets`; so they become `RF_SUFFIX` and 'triplets_SUFFIX`
    - Like before, add a `SUBDIR/` to `recon_path`:
        ```
        recon_file_path = out_folder + 'SUBDIR/' + "recon" + str(i)
        ```
    - In the last two lines, make sure the CSVs are named appropriately.
        ```
        RF_SUFFIX.to_csv('./benchmarking/RF_SUFFIX.csv')

        triplets_SUFFIX.to_csv('./benchmarking/triplets_SUFFIX.csv')
        ```
3. Modify the Metrics Loading cells (under plotting section)
    - Add a line to load your previously saved CSV of metrics. Repeat to get both RF and triplets.
    ```
    metrics_df['RF_SUFFIX'] = pd.read_csv('./benchmarking/RF_SUFFIX.csv')['NormalizedRobinsonFoulds']

    metrics_df['triplets_SUFFIX'] = pd.read_csv('./benchmarking/triplets_SUFFIX.csv')['TripletsCorrect']
    ```
4. Modify the *two* plotting cells
    - Add a reference to the new column above in the `ax.boxplot()` function
        ```
        ax.boxplot([
            metrics_df['RF'], 
            metrics_df['RF_og'], 
            metrics_df['RF_stdr'],
            metrics_df['RF_nj'],
            metrics_df['RF_snj_neg'],
            metrics_df['RF_snj_sm'],
            metrics_df['RF_SUFFIX'], # <<<<<<<<
        ], vert = 0)
        ```
    - Add the name of the new implementation under the second argument of the `plt.yticks` function.
        ```
        plt.yticks(list(range(1, len(metrics_df.columns)//2 + 1)), [
            'SNJ Cass', 
            'SNJ Yaffe', 
            'STDR Yaffe',
            'NJ Yaffe',
            'SNJ Yaffe NEG Control',
            'SNJ Yaffe from SM',
            'SNJ SUFFIX' # <<<<<<<<<<<
        ])
        ```
