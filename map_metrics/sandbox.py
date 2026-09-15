from pathlib import Path

import numpy as np
import open3d as o3d
from map_metrics.metrics import mom
from map_metrics.config import LidarConfig

def read_binary(file: Path) -> tuple[float, ...]:
    """Reads binary data from a file.

    Args:
        file: path to the binary file.

    Returns:
        data: binary data as floats.
    """
    with open(file, "rb") as f:
        data = np.fromfile(f, np.float32)
        return tuple(data)

def load_bin_pcd(bin_file_path: str) -> o3d.geometry.PointCloud:
    """Load a binary file with points data and creates a point cloud.

    Args:
        bin_file_path: path to the binary file.

    Returns:
        a point cloud.
    """
    p = Path(bin_file_path)
    data = read_binary(p)
    points = np.array(data).reshape((-1, 4))
    points = points[:, :3]
    cloud = o3d.geometry.PointCloud()
    cloud.points = o3d.utility.Vector3dVector(points)
    return cloud


def visualize_point_cloud_with_subsets(pcd, planes):
    """
    Visualize the entire point cloud in grey and three subsets of points with RGB colors.

    Parameters:
    - pcd: open3d.geometry.PointCloud object
    - planes: List of numpy arrays [subset1, subset2, subset3]
      Each subset should have shape (N, 3), where N is the number of points in the subset.
    """
    # Visualize the entire point cloud in grey color
    pcd_visual = pcd
    pcd_visual.paint_uniform_color([0.5, 0.5, 0.5])  # Set point cloud to grey color

    # Define colors for the subsets (RGB colors for the planes)
    subset_colors = [
        np.array([1, 0, 0]),  # Red for subset 1
        np.array([0, 1, 0]),  # Green for subset 2
        np.array([0, 0, 1]),  # Blue for subset 3
    ]

    # Create point clouds for the subsets
    subset_pcds = []
    for i, plane in enumerate(planes):
        subset = o3d.geometry.PointCloud()
        # Ensure the numpy array is converted to the appropriate Open3D format
        subset.points = o3d.utility.Vector3dVector(plane)
        # Set the color of the subset
        subset.paint_uniform_color(subset_colors[i])
        subset_pcds.append(subset)

    # Combine the original point cloud with the subsets
    vis = o3d.visualization.Visualizer()
    vis.create_window()

    # Add the original point cloud (grey) to the visualizer
    vis.add_geometry(pcd_visual)

    # Add each of the subset point clouds (colored)
    for subset in subset_pcds:
        vis.add_geometry(subset)

    # Run the visualization
    vis.run()
    vis.destroy_window()


# Example Usage
if __name__ == "__main__":
    config = LidarConfig()

    bin_file_path1 = "/home/mark/Desktop/PhD/map-metrics/tests/data/lidar/pcs/000000.bin"
    # bin_file_path1 = "/media/mark/New Volume/datasets/kaist/urban-26/sensor_data/VLP_right/1544581170343974000.bin"
    # bin_file_path2 = "/media/mark/New Volume/datasets/kaist/urban-26/sensor_data/VLP_left/1544581170279399000.bin"
    pcd1 = load_bin_pcd(bin_file_path1)
    # pcd2 = load_bin_pcd(bin_file_path2)
    pcd = pcd1

    # o3d.visualization.draw_geometries([pcd])

    # subsets, _, _ = extract_orthogonal_subsets(pcd, config)
    mom = mom([pcd], [np.eye(4)], config=config)

    # print(mom([pcd1], [np.eye(4)], config=config))

    # visualize_point_cloud_with_subsets(pcd, subsets)
