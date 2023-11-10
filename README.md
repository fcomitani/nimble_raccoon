
# nimble raccoon 

A slim and fast reimplementation of [RACCOON](https://github.com/shlienlab/raccoon) 
(Resolution-Adaptive Coarse-to-fine Clusters OptimizatiON), iterative clustering library for python 3.

<!-- 
<img src="docs/figs/sps_logo.png" width=400, padding=100>
[![DOI](https://zenodo.org/badge/91130860.svg)](https://zenodo.org/badge/latestdoi/91130860)
[![PyPI version](https://badge.fury.io/py/simpsom.svg)](https://badge.fury.io/py/simpsom)
[![Documentation Status](https://readthedocs.org/projects/simpsom/badge/?version=latest)](https://simpsom.readthedocs.io/en/latest/?badge=latest)
![example workflow](https://github.com/fcomitani/simpsom/actions/workflows/pytest.yml/badge.svg)
[![codecov](https://codecov.io/gh/fcomitani/simpsom/branch/main/graph/badge.svg?token=2OHOCO0O4I)](https://codecov.io/gh/fcomitani/simpsom) 
-->

## Installation

`nimble-raccoon` can be installed with `pip` with the following command

    pip install nimble-raccoon 

## Usage

To identify clusters and build the hierarchy initialize a `Raccoon` object
with set parameters and then call it on the `input_data` object, a pandas dataframe.
    
    import numpy as np
    from functools import partial

    from nraccoon import Raccoon

    def half_sqrt_range(x: float, num_elements: int = 5) -> np.ndarray:
        """ Return a list of integers from sqrt(x)/2 to sqrt(x) with
            num_elements elements.
            
        :param x: integer.
        :param num_elements: number of elements in the list.
        :return: list of integers.
        """

        sq = np.sqrt(x)
        return np.linspace(sq/2, sq, num_elements, dtype=int)

    rc_args={'metric': 'cosine',
            'scale' : False,
            'cumulative_variance' : [.75, .8, .9, .95, .99],
            'clustering_parameter' : np.logspace(-2, 1.5, 10),
            'n_neighbors' : partial(half_sqrt_range, num_elements=3),
            'target_dimensions': 12,
            'min_cluster_size' : 25,
            'max_neighbors' : 100,
            'silhouette_threshold' :0.,
            'max_depth': 5}

    rc = Raccoon(out_path='./rc_output', **rc_args)
    rc_labels, rc_tree = rc(input_table)

Available parameters are:

- `metric`: the distance metric, currently only `cosine` and `euclidean` can be set as metrics.
- `scale`:  scale features at every iteration.
- `cumulative_variance`: the limit of cumulative variance for low-information
    features removal with tSVD. Can be a single `float` or a `list` of `float`
- `clustering_parameter`: the range of resolutions for the Louvain clustering 
    algorithm. Can be a single `float` or a `list` of `float`
- `n_neighbors`: the number of nearest neighbors to use across the search.
    Can be a single `int` or a `list` of `int`. Can also be a function, in which case this will be applied to the input set size,
    adapting this parameter at each iteration.
- `target_dimensions`: the dimensionality of the target space after 
    applying UMAP.
- `min_cluster_size`: minimum size of clusters, if a cluster is identified
    with size below this threshold, it will not be further split.
- `max_neighbors`: maximum number of neighbors, useful when `n_neighbors` is
    dynamic and population dependent avoiding excessively costly operations for large datasets.
- `silhouette_threshold`: minimum silhouette score value to reach for a 
    partition to be accepted.
- `max_depth`: maximum depth of the clusters hierarchy.

The output will be a one-hot-encoded dataframe with samples as rows and cluster labels as columns, and an anytree object with information on the
hierarchical relationship among clusters.
This information will also be automatically saved to disk in the `out_path` folder.

## Citation

If you are using this library for your work, please cite the original RACCOON publication.

> Comitani, F., Nash, J.O., Cohen-Gogo, S. et al. Diagnostic classification of childhood cancer using multiscale transcriptomics. Nat Med 29, 656–666 (2023). https://doi.org/10.1038/s41591-023-02221-x

## Contributions

Contributions are always welcome. If you would like to help us improve this library please fork the main branch and make sure pytest pass after your changes. 