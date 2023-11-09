from functools import partial

import pandas as pd
import numpy as np

from raccoon import Raccoon

synth_table = pd.read_parquet('/Users/federico.comitani/Work/90d/synthons_avg_subsample_1k.pq')#.sample(10000)

def half_sqrt_ranges(x, num_elements=5):
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
                        'cumulative_variance' : .9,#[.75, .8, .9, .95, .99],
                        'clustering_parameter' : np.logspace(-2, 1.5, 10),
                        'n_neighbors' : np.sqrt,#partial(half_sqrt_ranges, num_elements=3),
                        'target_dimensions': 12,
                        'min_cluster_size' : 25,
                        'max_neighbors' : 100,
                        'silhouette_threshold' : -1,
                        'max_depth': 10}

rc = Raccoon(out_path='/Users/federico.comitani/Work/nimble_raccoon/tests', **rc_args)
_ = rc(synth_table)
