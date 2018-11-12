import waterz
import numpy as np

aff = np.random.random((3,5,5,5)).astype(np.float32)
seg_gt = None

aff_thresholds = [0.005, 0.995]
seg_thresholds = [0.1, 0.3, 0.6]

seg = waterz.waterz(aff, seg_thresholds, merge_function='aff50_his256', aff_threshold=aff_thresholds, gt=seg_gt)
