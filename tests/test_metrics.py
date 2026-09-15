import pytest
from pathlib import Path
import numpy as np
import open3d as o3d
import os

from map_metrics.config import DepthConfig
from map_metrics.metrics import mme, mpv, mom
from map_metrics.utils.orthogonal import read_orthogonal_subset

@pytest.fixture
def data_dir(request):
    return Path(request.fspath).parent / "data"

@pytest.fixture
def depth_trajectories(data_dir):
    ts_folder = data_dir / "depth/poses"
    ts_names = sorted(os.listdir(ts_folder))
    trajectories = []
    for name in ts_names:
        trajectories.append(np.loadtxt(ts_folder / name, usecols=range(4)))
    return trajectories

@pytest.fixture
def depth_pointclouds(data_dir):
    pcs_folder = data_dir / "depth/pcs"
    pc_names = sorted(os.listdir(pcs_folder))
    pcs = []
    for name in pc_names:
        file_str = str(pcs_folder / name)
        pcs.append(o3d.io.read_point_cloud(file_str))
    return pcs

@pytest.fixture
def depth_orthsubset(data_dir, depth_trajectories):
    orth_list_name = data_dir / "depth/orth_subset/orth-0091.npy"
    orth_tj_name = data_dir / "depth/poses/pose-0091.txt"

    orth_list = read_orthogonal_subset(
        orth_subset_name=orth_list_name,
        orth_pose_name=orth_tj_name,
        ts=depth_trajectories,
    )
    return orth_list

@pytest.mark.parametrize(
    "config, metric, expected",
    [
        (DepthConfig, mme, -3.614438706),
        (DepthConfig, mpv, 0.003242216),
    ],
)
def test_basic_metrics(depth_pointclouds, depth_trajectories, config, metric, expected):
    actual_result = metric(pcs=depth_pointclouds, ts=depth_trajectories, config=config)
    assert abs(actual_result - expected) < 1e-3

def test_mom(depth_pointclouds, depth_trajectories, depth_orthsubset):
    actual_result = mom(
        depth_pointclouds, depth_trajectories, depth_orthsubset, config=DepthConfig
    )
    assert abs(actual_result - 0.006183082) < 1e-3