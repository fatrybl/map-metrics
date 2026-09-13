file(GLOB ALGLIB_HEADERS "src/*.h")
file(GLOB ALGLIB_SOURCES "src/*.cpp")

file(COPY ${ALGLIB_HEADERS} DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/include/alglib)
file(COPY ${ALGLIB_SOURCES} DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/src)

add_library(alglib STATIC ${ALGLIB_SOURCES} ${ALGLIB_HEADERS})  # static everywhere: the Python module must not depend on a loose libalglib.so

target_include_directories(alglib PRIVATE ${CMAKE_CURRENT_BINARY_DIR}/include/)
target_include_directories(alglib INTERFACE ${CMAKE_CURRENT_BINARY_DIR}/include/alglib)
