from libc.stdint cimport uint64_t, uint16_t
from libcpp.map cimport map
import numpy as np
cimport numpy as np

def evaluate_total_volume(
        np.ndarray[uint64_t, ndim=3] segmentation,
        np.ndarray[uint64_t, ndim=3] gt):

    for d in range(3):
        assert segmentation.shape[d] == gt.shape[d], (
            "Shapes in dim %d do not match"%d)
    shape = segmentation.shape

    # the C++ part assumes contiguous memory, make sure we have it (and do 
    # nothing, if we do)
    if not segmentation.flags['C_CONTIGUOUS']:
        print("Creating memory-contiguous segmentation arrray (avoid this by passing C_CONTIGUOUS arrays)")
        segmentation = np.ascontiguousarray(segmentation)
    if gt is not None and not gt.flags['C_CONTIGUOUS']:
        print("Creating memory-contiguous ground-truth arrray (avoid this by passing C_CONTIGUOUS arrays)")
        gt = np.ascontiguousarray(gt)

    cdef uint64_t* segmentation_data
    cdef uint64_t* gt_data

    segmentation_data = &segmentation[0, 0, 0]
    gt_data = &gt[0, 0, 0]

    return compare_arrays(
        shape[0], shape[1], shape[2],
        gt_data,
        segmentation_data)


def compute_statistics_for_volume_init(
        np.ndarray[uint16_t, ndim=3] segmentation,
        np.ndarray[uint16_t, ndim=3] gt):

    for d in range(3):
        assert segmentation.shape[d] == gt.shape[d], (
            "Shapes in dim %d do not match"%d)
    shape = segmentation.shape

    # the C++ part assumes contiguous memory, make sure we have it (and do 
    # nothing, if we do)
    if not segmentation.flags['C_CONTIGUOUS']:
        print("Creating memory-contiguous segmentation arrray (avoid this by passing C_CONTIGUOUS arrays)")
        segmentation = np.ascontiguousarray(segmentation)
    if gt is not None and not gt.flags['C_CONTIGUOUS']:
        print("Creating memory-contiguous ground-truth arrray (avoid this by passing C_CONTIGUOUS arrays)")
        gt = np.ascontiguousarray(gt)

    cdef uint16_t* segmentation_data
    cdef uint16_t* gt_data

    segmentation_data = &segmentation[0, 0, 0]
    gt_data = &gt[0, 0, 0]

    return compute_statistics(
        shape[0], shape[1], shape[2],
        gt_data,
        segmentation_data)

def compute_statistics_for_volume(Statistics stats,
        np.ndarray[uint16_t, ndim=3] segmentation,
        np.ndarray[uint16_t, ndim=3] gt):

    for d in range(3):
        assert segmentation.shape[d] == gt.shape[d], (
            "Shapes in dim %d do not match"%d)
    shape = segmentation.shape

    # the C++ part assumes contiguous memory, make sure we have it (and do 
    # nothing, if we do)
    if not segmentation.flags['C_CONTIGUOUS']:
        print("Creating memory-contiguous segmentation arrray (avoid this by passing C_CONTIGUOUS arrays)")
        segmentation = np.ascontiguousarray(segmentation)
    if gt is not None and not gt.flags['C_CONTIGUOUS']:
        print("Creating memory-contiguous ground-truth arrray (avoid this by passing C_CONTIGUOUS arrays)")
        gt = np.ascontiguousarray(gt)

    cdef uint16_t* segmentation_data
    cdef uint16_t* gt_data

    segmentation_data = &segmentation[0, 0, 0]
    gt_data = &gt[0, 0, 0]

    return compute_statistics(
        stats, shape[0], shape[1], shape[2],
        gt_data,
        segmentation_data)

def compute_final_metrics(Statistics stats):
    return compute_metrics(stats);


cdef extern from "frontend_evaluate.h":

    struct Metrics:
        double voi_split
        double voi_merge
        double rand_split
        double rand_merge
    
    struct Statistics:
        double total;
        map[uint16_t, map[uint16_t, double]] p_ij;
        map[uint16_t, double] s_i;
        map[uint16_t, double] t_j;

    Metrics compare_arrays(
            size_t          width,
            size_t          height,
            size_t          depth,
            const uint64_t* gt_data,
            const uint64_t* segmentation_data);

    Statistics compute_statistics(
            size_t  width,
            size_t  height,
            size_t  depth,
            const uint16_t* gt_data,
            const uint16_t* segmentation_data);

    Statistics compute_statistics(
            Statistics& stats,
            size_t  width,
            size_t  height,
            size_t  depth,
            const uint16_t* gt_data,
            const uint16_t* segmentation_data);

    Metrics compute_metrics(Statistics& stats);
