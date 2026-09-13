"""numpy front end for the C++ map-metrics module (build/cpp/pybind/pybind*.so), with the
same signatures as map_metrics.metrics in the Python package: clouds as (N, 3) arrays, poses
as 4x4 arrays, config = (min_knn, knn_rad, max_nn, min_clust_size); LIDAR = (5, 1.0, 30, 5),
DEPTH = (5, 0.2, 30, 5). MOM extracts the orthogonal subsets from the first cloud, as the
Python implementation does, and scores neighbourhoods of more than 3 points."""
import glob
import os
import sys

import numpy as np

sys.path.insert(0, glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "build", "cpp", "pybind"))[0])
import pybind as _mm  # noqa: E402

LIDAR = (5, 1.0, 30, 5)
DEPTH = (5, 0.2, 30, 5)


def _map(clouds, poses):
    pts = [np.ascontiguousarray(np.asarray(c, dtype=np.float64)[:, :3].T) for c in clouds]
    return _mm.cloud_utils.aggregate_map(pts, [np.asarray(p, dtype=np.float64) for p in poses]), pts


def mme(clouds, poses, config=LIDAR):
    map_pts, _ = _map(clouds, poses)
    return _mm.metrics.MME(_mm.map_tree.MapTree(map_pts, config[1]), config[0])


def mpv(clouds, poses, config=LIDAR):
    map_pts, _ = _map(clouds, poses)
    return _mm.metrics.MPV(_mm.map_tree.MapTree(map_pts, config[1]), config[0])


def orthogonal_subsets(cloud, config=LIDAR):
    pts = np.ascontiguousarray(np.asarray(cloud, dtype=np.float64)[:, :3].T)
    return _mm.cloud_utils.find_orthogonal_subset(pts, _mm.config.Config(*config))


def mom(clouds, poses, config=LIDAR, orth_list=None):
    map_pts, pts = _map(clouds, poses)
    if orth_list is None:
        orth_list = _mm.cloud_utils.find_orthogonal_subset(pts[0], _mm.config.Config(*config))
    return _mm.metrics.MOM(_mm.map_tree.MapTree(map_pts, config[1]), 3, orth_list)
