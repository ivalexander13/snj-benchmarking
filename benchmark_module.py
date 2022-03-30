from operator import gt
from pathlib import Path
import networkx as nx
import cassiopeia as cas
import pandas as pd
import pickle as pic
from tqdm import tqdm, trange
import numpy as np
import inverse_whd
import pickle
import numpy as np
import matplotlib.pyplot as plt
import numba
import os
from cassiopeia.solver.CassiopeiaSolver import CassiopeiaSolver


class BenchmarkModule:
    def __init__(
        self,
        test_name: str,
        solver: CassiopeiaSolver = cas.solver.NeighborJoiningSolver(add_root = True, dissimilarity_function=cas.solver.dissimilarity_functions.weighted_hamming_distance),  # type: ignore
        gt_trees_dir = "/data/yosef2/users/richardz/projects/CassiopeiaV2-Reproducibility/priors/states100.pkl",
        numtrees = 50,
        out_basefolder = "./benchmarking/",
        ):
        self.test_name = test_name
        self.solver = solver
        self.gt_trees_dir = gt_trees_dir
        self.numtrees = numtrees
        self.out_basefolder = out_basefolder

    def get_gt_tree(self, i):
        gt_tree_file = os.path.join(self.gt_trees_dir, f"tree{i}.pkl")
        gt_tree = pic.load(open(gt_tree_file, "rb"))

        return gt_tree

    def get_recon_tree(self, i):
        recon_file = os.path.join(self.out_basefolder, self.test_name, f"recon{i}")
        recon_tree = cas.data.CassiopeiaTree(
                tree=recon_file
            )

        return recon_tree

    def run_solver(self, i, cm, collapse_mutationless_edges) -> str:
        # Initialize output recon tree
        recon_tree = cas.data.CassiopeiaTree(
            character_matrix=cm, 
            missing_state_indicator = -1
            )
        
        # Instantiate Solver
        self.solver.solve(recon_tree, collapse_mutationless_edges = collapse_mutationless_edges)
        
        return recon_tree.get_newick()

    def get_cm(self, i):
        cm_file = os.path.join(self.gt_trees_dir, f"cm{i}.txt")
        cm = pd.read_table(cm_file, index_col = 0)
        cm = cm.replace(-2, -1)  # type: ignore

        return cm

    def reconstruct(
        self,
        overwrite=False,
        collapse_mutationless_edges=True
        ):

        pbar = trange(self.numtrees)
        for i in pbar:
            pbar.set_description(f"Reconstructing tree {i}")

            # Output File
            recon_outfile = Path(os.path.join(self.out_basefolder, self.test_name, f"recon{i}"))
            recon_outfile.parent.mkdir(parents=True, exist_ok=True)

            if not overwrite and recon_outfile.exists():
                pbar.set_description(f"Skipping reconstruction {i}")
                continue

            # Get CM
            cm = self.get_cm(i)

            # Instantiate Solver
            recon_newick = self.run_solver(i, cm, collapse_mutationless_edges)
            
            # Save
            with open(recon_outfile, "w+") as f:
                f.write(recon_newick)
                f.close()

    def evaluate(self, overwrite=False):
        # Output Files
        rf_out = Path(os.path.join(self.out_basefolder, f"{self.test_name}.rf.csv"))
        triplets_out = Path(os.path.join(self.out_basefolder, f"{self.test_name}.triplets.csv"))

        # Check overwrites
        if not overwrite and rf_out.exists() and triplets_out.exists():
            return

        # Init datframes
        triplets_df = pd.DataFrame(
            columns=[
                "NumberOfCells",
                "Priors",
                "Fitness",
                "Stressor",
                "Parameter",
                "Algorithm",
                "Replicate",
                "Depth",
                "TripletsCorrect",
            ]
        )
        RF_df = pd.DataFrame(
            columns=[
                "NumberOfCells",
                "Priors",
                "Fitness",
                "Stressor",
                "Parameter",
                "Algorithm",
                "Replicate",
                "UnNormalizedRobinsonFoulds",
                "MaxRobinsonFoulds",
                "NormalizedRobinsonFoulds",
            ]
        )

        # Main Loop
        pbar = trange(self.numtrees)
        for i in pbar:
            pbar.set_description(f"Evaluating tree {i}")

            # GT Tree
            gt_tree = self.get_gt_tree(i)

            # Recon Tree
            recon_tree = self.get_recon_tree(i)

            # Triplets
            triplet_correct = cas.critique.triplets_correct(
                gt_tree,
                recon_tree,
                number_of_trials=1000,
                min_triplets_at_depth=50,
            )[0]

            for depth in triplet_correct:
                triplets_df = triplets_df.append(
                    pd.Series(
                        [
                            400,
                            "no_priors",
                            "no_fit",
                            "char",
                            40,
                            "SNJ",
                            i,
                            depth,
                            triplet_correct[depth],
                        ],
                        index=triplets_df.columns,
                    ),
                    ignore_index=True,
                )

            # RF
            rf, rf_max = cas.critique.robinson_foulds(
                gt_tree, recon_tree
            )

            RF_df = RF_df.append(
                pd.Series(
                    [
                        400,
                        "no_priors",
                        "no_fit",
                        "char",
                        40,
                        "SNJ",
                        i,
                        rf,
                        rf_max,
                        rf / rf_max,
                    ],
                    index=RF_df.columns,
                ),
                ignore_index=True,
            )

        # Save
        triplets_df.to_csv(triplets_out)
        RF_df.to_csv(rf_out)

        return 



