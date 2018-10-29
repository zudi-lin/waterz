#include "frontend_evaluate.h"


Metrics
compare_arrays(
        std::size_t  width,
        std::size_t  height,
        std::size_t  depth,
        const uint64_t* gt_data,
        const uint64_t* segmentation_data) {

    // wrap gt array (no copy)
    volume_const_ref<uint64_t> gt(
            gt_data,
            boost::extents[width][height][depth]
    );

    // wrap segmentation array (no copy)
    volume_const_ref<uint64_t> segmentation(
            segmentation_data,
            boost::extents[width][height][depth]
    );

    auto m = compare_volumes(gt, segmentation);

    Metrics metrics;
    metrics.rand_split = std::get<0>(m);
    metrics.rand_merge = std::get<1>(m);
    metrics.voi_split  = std::get<2>(m);
    metrics.voi_merge  = std::get<3>(m);

    return metrics;
}



void
update_statistics(
        Statistics* stats,
        std::size_t  width,
        std::size_t  height,
        std::size_t  depth,
        const uint16_t* gt_data,
        const uint16_t* segmentation_data) {
    volume_const_ref<uint16_t> gt(
            gt_data,
            boost::extents[width][height][depth]
    );

    // wrap segmentation array (no copy)
    volume_const_ref<uint16_t> segmentation(
            segmentation_data,
            boost::extents[width][height][depth]
    );
    compute_stats(&(stats->total), 
    &(stats->p_ij), 
    &(stats->s_i), 
    &(stats->t_j), 
    gt,
    segmentation);
}

Metrics
compute_metrics(Statistics *stats) {
    auto m = compute_mets(&(stats->total), &(stats->p_ij), &(stats->s_i), &(stats->t_j));
    Metrics metrics;
    metrics.rand_split = std::get<0>(m);
    metrics.rand_merge = std::get<1>(m);
    metrics.voi_split  = std::get<2>(m);
    metrics.voi_merge  = std::get<3>(m);

    return metrics;
}

