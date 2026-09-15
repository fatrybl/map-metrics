// Copyright (c) 2022, Arthur Saliou, Anastasiia Kornilova
//
//  Licensed under the Apache License, Version 2.0 (the "License");
//  you may not use this file except in compliance with the License.
//  You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License.
//
//
//  Created on: May 20, 2022
//       Author: Arthur Saliou
//               arthur.salio@gmail.com
//
#include "metrics_core.h"

#include <algorithm>
#include <cmath>
#include <limits>
#include <numeric>

namespace map_metrics {
double baseMetricEstimator(MapTree const& map_tree, double (*point_statistic)(Eigen::Matrix3Xd const& points),
                           int min_component_size) {
  // fork: every point's statistic comes from an on-demand neighbourhood, computed in parallel and summed in point
  // order afterwards, so the result does not depend on the thread count. A statistic that is not finite (the entropy
  // of a degenerate neighbourhood) is skipped, and a map without any valid neighbourhood scores 0, as in the Python
  // map-metrics.
  const Eigen::Index point_count = map_tree.size();
  std::vector<double> point_statistics(point_count, std::numeric_limits<double>::quiet_NaN());

  #pragma omp parallel for schedule(dynamic, 256)
  for (Eigen::Index i = 0; i < point_count; ++i) {
    const std::vector<Eigen::Index> neighbour_list = map_tree.getMapPointNeighbours(i);
    bool enough_neighbours = neighbour_list.size() > min_component_size;
    if (enough_neighbours) {
      point_statistics[i] = point_statistic(map_tree.getMapPoints(neighbour_list));
    }
  }

  double sum = 0.0;
  Eigen::Index valid_count = 0;
  for (double statistic : point_statistics) {
    if (std::isfinite(statistic)) {
      sum += statistic;
      ++valid_count;
    }
  }

  return valid_count == 0 ? 0.0 : sum / static_cast<double>(valid_count);
}

double orthogonalEstimator(MapTree const& map_tree, double (*point_statistic)(Eigen::Matrix3Xd const& points),
                           int min_component_size, std::vector<Eigen::Matrix3Xd> const& orthogonal_subset) {
  std::vector<double> metric_statistic;
  for (auto const& orthogonal_component : orthogonal_subset) {
    std::vector<double> component_metric_statistic;

    for (auto const& neighbour_list : map_tree.getNeighboursByComponent(orthogonal_component)) {
      bool enough_neighbours = neighbour_list.size() > min_component_size;
      if (enough_neighbours) {
        component_metric_statistic.push_back(point_statistic(map_tree.getMapPoints(neighbour_list)));
      }
    }
    if (component_metric_statistic.empty()) continue;
    std::sort(component_metric_statistic.begin(), component_metric_statistic.end());
    double component_statistic_median = (component_metric_statistic.size() % 2 == 0
                                             ? (component_metric_statistic[component_metric_statistic.size() / 2 - 1] +
                                                component_metric_statistic[component_metric_statistic.size() / 2]) /
                                                   2.0
                                             : component_metric_statistic[component_metric_statistic.size() / 2]);
    metric_statistic.push_back(component_statistic_median);
  }

  return std::accumulate(metric_statistic.begin(), metric_statistic.end(), 0.0);
}
}  // namespace map_metrics
