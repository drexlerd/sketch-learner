
#ifndef __MEMORY__
#define __MEMORY__

#include <memory>

namespace aptk {

template<typename T, typename... Args>
std::unique_ptr<T> make_unique(Args&&... args) {
    return std::unique_ptr<T>(new T(std::forward<Args>(args)...));
}

}

#endif
