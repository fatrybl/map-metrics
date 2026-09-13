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
#include "metrics.h"

#include <pybind11/eigen.h>  // the MOM default argument is a std::vector<Eigen::Matrix3Xd>
#include <pybind11/stl.h>

#include <map_metrics/metrics.h>

namespace map_metrics {
void pybindMetrics(py::module& m) {
  py::module m_metrics = m.def_submodule("metrics", "Map Metrics (MME, MPV, MOM)");

  m_metrics.def("MME", &MME, "Mean Map Entropy map metric", py::arg("map_tree"), py::arg("min_component_size"));
  m_metrics.def("MPV", &MPV, "Mean Map Variance map metric", py::arg("map_tree"), py::arg("min_component_size"));
  m_metrics.def("MOM", &MOM, "Mutually Orthogonal Metric map metric", py::arg("map_tree"),
                py::arg("min_component_size"), py::arg("orthogonal_subset") = std::vector<Eigen::Matrix3Xd>());
}
}  // namespace map_metrics