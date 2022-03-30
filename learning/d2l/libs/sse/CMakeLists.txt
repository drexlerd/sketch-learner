cmake_minimum_required(VERSION 3.12)
project(sse VERSION 0.1)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(Boost 1.65 COMPONENTS program_options timer filesystem REQUIRED)

set(SOURCE_FILES
        src/fs/core/actions/action_id.cxx
        src/fs/core/actions/action_id.hxx
        src/fs/core/actions/actions.cxx
        src/fs/core/actions/actions.hxx
        src/fs/core/actions/checker.cxx
        src/fs/core/actions/checker.hxx
        src/fs/core/actions/grounding.cxx
        src/fs/core/actions/grounding.hxx
        src/fs/core/applicability/action_managers.cxx
        src/fs/core/applicability/action_managers.hxx
        src/fs/core/applicability/base.hxx
        src/fs/core/applicability/formula_interpreter.cxx
        src/fs/core/applicability/formula_interpreter.hxx
        src/fs/core/applicability/match_tree.cxx
        src/fs/core/applicability/match_tree.hxx
        src/fs/core/fstrips/language.cxx
        src/fs/core/fstrips/language.hxx
        src/fs/core/fstrips/language_info.cxx
        src/fs/core/fstrips/language_info.hxx
        src/fs/core/fstrips/loader.cxx
        src/fs/core/fstrips/loader.hxx
        src/fs/core/fstrips/operations.cxx
        src/fs/core/fstrips/operations.hxx
        src/fs/core/languages/fstrips/operations/axioms.cxx
        src/fs/core/languages/fstrips/operations/axioms.hxx
        src/fs/core/languages/fstrips/operations/basic.cxx
        src/fs/core/languages/fstrips/operations/basic.hxx
        src/fs/core/languages/fstrips/operations/binding.cxx
        src/fs/core/languages/fstrips/operations/binding.hxx
        src/fs/core/languages/fstrips/operations/conjunction.cxx
        src/fs/core/languages/fstrips/operations/conjunction.hxx
        src/fs/core/languages/fstrips/operations/interpretation.cxx
        src/fs/core/languages/fstrips/operations/interpretation.hxx
        src/fs/core/languages/fstrips/axioms.cxx
        src/fs/core/languages/fstrips/axioms.hxx
        src/fs/core/languages/fstrips/base.cxx
        src/fs/core/languages/fstrips/base.hxx
        src/fs/core/languages/fstrips/builtin.cxx
        src/fs/core/languages/fstrips/builtin.hxx
        src/fs/core/languages/fstrips/effects.cxx
        src/fs/core/languages/fstrips/effects.hxx
        src/fs/core/languages/fstrips/factory.cxx
        src/fs/core/languages/fstrips/factory.hxx
        src/fs/core/languages/fstrips/formulae.cxx
        src/fs/core/languages/fstrips/formulae.hxx
        src/fs/core/languages/fstrips/language.hxx
        src/fs/core/languages/fstrips/language_fwd.hxx
        src/fs/core/languages/fstrips/loader.cxx
        src/fs/core/languages/fstrips/loader.hxx
        src/fs/core/languages/fstrips/operations.hxx
        src/fs/core/languages/fstrips/scopes.cxx
        src/fs/core/languages/fstrips/scopes.hxx
        src/fs/core/languages/fstrips/terms.cxx
        src/fs/core/languages/fstrips/terms.hxx
        src/fs/core/search/nodes/state_space_expansion_node.hxx
        src/fs/core/models/ground_state_model.cxx
        src/fs/core/models/ground_state_model.hxx
        src/fs/core/models/utils.hxx
        src/fs/core/models/utils.cxx
        src/fs/core/models/simple_state_model.cxx
        src/fs/core/models/simple_state_model.hxx
        src/fs/core/search/algorithms/state_space_expansion.hxx
        src/fs/core/search/drivers/base.hxx
        src/fs/core/search/drivers/state_space_expansion.hxx
        src/fs/core/search/drivers/state_space_expansion.cxx
        src/fs/core/constraints/registry.hxx
        src/fs/core/constraints/registry.cxx
        src/fs/core/search/drivers/registry.cxx
        src/fs/core/search/drivers/registry.hxx
        src/fs/core/search/drivers/setups.cxx
        src/fs/core/search/drivers/setups.hxx
        src/fs/core/search/drivers/validation.cxx
        src/fs/core/search/drivers/validation.hxx
        src/fs/core/search/events.hxx
        src/fs/core/search/options.cxx
        src/fs/core/search/options.hxx
        src/fs/core/search/runner.cxx
        src/fs/core/search/runner.hxx
        src/fs/core/search/stats.hxx
        src/fs/core/search/utils.hxx
        src/fs/core/utils/printers/actions.cxx
        src/fs/core/utils/printers/actions.hxx
        src/fs/core/utils/printers/binding.cxx
        src/fs/core/utils/printers/binding.hxx
        src/fs/core/utils/printers/helper.cxx
        src/fs/core/utils/printers/helper.hxx
        src/fs/core/utils/printers/language.cxx
        src/fs/core/utils/printers/language.hxx
        src/fs/core/utils/printers/printers.cxx
        src/fs/core/utils/printers/printers.hxx
        src/fs/core/utils/printers/registry.cxx
        src/fs/core/utils/printers/registry.hxx
        src/fs/core/utils/printers/vector.hxx
        src/fs/core/utils/atom_index.cxx
        src/fs/core/utils/atom_index.hxx
        src/fs/core/utils/binding.cxx
        src/fs/core/utils/binding.hxx
        src/fs/core/utils/binding_iterator.cxx
        src/fs/core/utils/binding_iterator.hxx
        src/fs/core/utils/bitsets.hxx
        src/fs/core/utils/cartesian_iterator.cxx
        src/fs/core/utils/cartesian_iterator.hxx
        src/fs/core/utils/component_factory.hxx
        src/fs/core/utils/config.cxx
        src/fs/core/utils/config.hxx
        src/fs/core/utils/dispatcher.hxx
        src/fs/core/utils/external.hxx
        src/fs/core/utils/index.hxx
        src/fs/core/utils/lexical_cast.hxx
        src/fs/core/utils/loader.cxx
        src/fs/core/utils/loader.hxx
        src/fs/core/utils/serialize_tuple.hxx
        src/fs/core/utils/serializer.cxx
        src/fs/core/utils/serializer.hxx
        src/fs/core/utils/static.cxx
        src/fs/core/utils/static.hxx
        src/fs/core/utils/support.cxx
        src/fs/core/utils/support.hxx
        src/fs/core/utils/system.cxx
        src/fs/core/utils/system.hxx
        src/fs/core/utils/tuple_hash.hxx
        src/fs/core/utils/utils.hxx
        src/fs/core/utils/visitor.hxx
        src/fs/core/atom.cxx
        src/fs/core/atom.hxx
        src/fs/core/base.cxx
        src/fs/core/base.hxx
        src/fs/core/fs_types
        src/fs/core/problem.cxx
        src/fs/core/problem.hxx
        src/fs/core/problem_info.cxx
        src/fs/core/problem_info.hxx
        src/fs/core/state.cxx
        src/fs/core/state.hxx
        src/fs/core/validator.cxx
        src/fs/core/validator.hxx
)

set(LAPKT_SOURCE_FILES
        submodules/lapkt-base/src/lapkt/tools/bit_array.cxx
        submodules/lapkt-base/src/lapkt/tools/logging.cxx
        submodules/lapkt-base/src/lapkt/tools/bit_set.cxx
)


set(FS_ROOT ${CMAKE_CURRENT_LIST_DIR})
set(FS_SRC ${FS_ROOT}/src)
set(FS_VENDOR ${FS_ROOT}/submodules)

#MESSAGE(WARNING "Your FS_ROOT home directory is: ${FS_ROOT}" )

include_directories(${Boost_INCLUDE_DIR})
include_directories(${FS_SRC})
include_directories(${FS_VENDOR}/rapidjson/include)
include_directories(${FS_VENDOR}/lapkt-base/src)
include_directories(${FS_VENDOR}/lapkt-novelty/src)

#set(CMAKE_VERBOSE_MAKEFILE ON)

SET(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${FS_ROOT})

add_executable(solver.bin src/planners/generic/main.cxx ${SOURCE_FILES} ${LAPKT_SOURCE_FILES})
target_link_libraries(solver.bin ${Boost_LIBRARIES})

