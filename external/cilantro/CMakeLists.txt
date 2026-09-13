find_package(cilantro QUIET)  # e.g. -Dcilantro_DIR=<cilantro build or install dir>

if(NOT cilantro_FOUND)
include(ExternalProject)
# CILANTRO_SOURCE_DIR=<path to a cilantro checkout> builds that copy instead of cloning
if(CILANTRO_SOURCE_DIR)
    set(_cilantro_source SOURCE_DIR ${CILANTRO_SOURCE_DIR})
else()
    set(_cilantro_source GIT_REPOSITORY https://github.com/kzampog/cilantro.git GIT_TAG origin/master)
endif()
ExternalProject_Add(
    cilantro_external
    PREFIX cilantro
    ${_cilantro_source}
    CMAKE_ARGS
        -DBUILD_EXAMPLES=OFF
        -DCMAKE_INSTALL_PREFIX=<INSTALL_DIR>
        -DBUILD_SHARED_LIBS=OFF
)
ExternalProject_Get_Property(cilantro_external INSTALL_DIR)
set(cilantro_LIBRARIES
"${INSTALL_DIR}/lib/${CMAKE_STATIC_LIBRARY_PREFIX}cilantro${CMAKE_STATIC_LIBRARY_SUFFIX}"
CACHE INTERNAL "" FORCE
)
else()
    set(cilantro_LIBRARIES cilantro CACHE INTERNAL "" FORCE)  # the exported target carries its include dirs
endif()
