
#include <strips_state.hxx>
#include <sketch_strips_prob.hxx>
#include <unordered_set>

namespace aptk {

/**
 * Unpacked version of a state.
 * Contains information about fluents that remain constant.
 */
class SketchState {
private:
    // the parent task.
    const Sketch_STRIPS_Problem* m_problem;
    // information about init fluents
    const Bit_Set m_init_fluents_set;
    // state information
    const State* m_state;
    Bit_Set m_state_fluents_set;

public:
    SketchState(const Sketch_STRIPS_Problem* problem)
        : m_problem(problem),
          m_init_fluents_set(problem->init_fluents_set()) {
    }

    /**
     * Get state fluents combined with constant fluents
     */
    const Bit_Set& get_state_fluents_set(const State* state) {
        if (state != m_state) {
            m_state = state;
            m_state_fluents_set = m_init_fluents_set;
            for (unsigned i : state->fluent_vec()) {
                m_state_fluents_set.set(i);
            }
        }
        return m_state_fluents_set;
    }

    /**
     * Getters
     */
    const State* state() const { return m_state; }
};

}