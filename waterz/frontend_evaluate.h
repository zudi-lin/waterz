#ifndef C_EVALUATE_H
#define C_EVALUATE_H

#include "backend/types.hpp"
#include "evaluate.hpp"

struct Metrics {

    double voi_split;
    double voi_merge;
    double rand_split;
    double rand_merge;
};

struct Statistics {
    double total;
    std::map<uint16_t, std::map<uint16_t, double>> p_ij;
    std::map<uint16_t, double> s_i;
    std::map<uint16_t, double> t_j;
    Statistics(): total(0), p_ij(std::map<uint16_t, std::map<uint16_t, double>>()),
        s_i(std::map<uint16_t, double>()), t_j(std::map<uint16_t, double>()) {}
};

inline Statistics get_stats() {
    return Statistics();
}

// inline void* dealloc_stats(Statistics* pointer) {
//     delete pointer;
// }


Metrics
compare_arrays(
        std::size_t  width,
        std::size_t  height,
        std::size_t  depth,
        const uint64_t* gt_data,
        const uint64_t* segmentation_data);


void
update_statistics(
        Statistics* stats,
        std::size_t  width,
        std::size_t  height,
        std::size_t  depth,
        const uint16_t* gt_data,
        const uint16_t* segmentation_data);


Metrics
compute_metrics(Statistics* stats);


#endif
