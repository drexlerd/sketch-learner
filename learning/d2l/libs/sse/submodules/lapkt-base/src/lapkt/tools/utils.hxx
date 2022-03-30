
#pragma once

#include <cassert>
#include <algorithm>
#include <vector>

namespace lapkt { namespace utils {

//! Compute intersection and set differences at the same time
template <typename T>
void intersection_and_set_diff(const std::vector<T>& A, const std::vector<T>& B,
                               std::vector<T>& inters, std::vector<T>& AminusB, std::vector<T>& BminusA)  {
	
	assert(std::is_sorted(A.begin(), A.end()));
	assert(std::is_sorted(B.begin(), B.end()));
	
	// Compute intersection and set differences in one pass
	unsigned i = 0, j = 0;
	unsigned a_sz = A.size(), b_sz = B.size();
	while(i < a_sz && j < b_sz) {
		const auto& a_i = A[i];
		const auto& b_j = B[j];
		
		if (a_i < b_j) {
			AminusB.push_back(a_i);
			++i;
		} else if (b_j < a_i) {
			BminusA.push_back(b_j);
			++j;
		} else { // b_j == a_i
			inters.push_back(a_i);
			++i;
			++j;
		}
	}
	
	assert(i == a_sz || j == b_sz); // i.e. at most one of the two below loops will actually do something
	while (i < a_sz) AminusB.push_back(A[i++]);
	while (j < b_sz) BminusA.push_back(B[j++]);
}

} } // namespaces

