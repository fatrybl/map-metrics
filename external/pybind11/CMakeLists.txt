# Prefer an installed pybind11 (e.g. -Dpybind11_DIR=$(python -c "import pybind11; print(pybind11.get_cmake_dir())")),
# fall back to fetching it.
set(CMAKE_FIND_PACKAGE_TARGETS_GLOBAL ON)  # the imported targets are used from cpp/pybind
find_package(pybind11 CONFIG QUIET)
if(NOT pybind11_FOUND)
    include(FetchContent)
    FetchContent_Declare(pybind11 GIT_REPOSITORY https://github.com/pybind/pybind11.git GIT_TAG v2.13.6)
    FetchContent_MakeAvailable(pybind11)
endif()
