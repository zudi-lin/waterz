# waterz
Pronounced water-zed. A simple watershed and region agglomeration library for affinity graphs.

# Features in this fork
Incorporate functions from Mala_v2.zip from [http://cremi.org](CREMI.org) for better segmentation result

# Usage
```
import waterz
import numpy as np

# affinities is a [3,depth,height,width] numpy array of float32
affinities = ...
# evaluation: vi/rand
seg_gt = ...

aff_thresholds = [0.005, 0.995]
seg_thresholds = [0.1, 0.3, 0.6]

seg = waterz.(aff, seg_thresholds, merge_function='aff50_his256',                                
              aff_threshold=aff_thresholds, gt=seg_gt)
```
