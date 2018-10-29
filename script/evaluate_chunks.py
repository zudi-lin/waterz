import numpy as np 
import waterz

a = (np.random.rand(100, 1000, 1000) * 255).astype(np.uint16)
b = (np.random.rand(100, 1000, 1000) * 255).astype(np.uint16)

num_chunks = 5
stat = waterz.initialize_stats()
for i in range(num_chunks):
    stat = waterz.update_statistics_using_volume(stat, a[i * num_chunks: (i + 1) * num_chunks], b[i * num_chunks: (i + 1) * num_chunks])
print waterz.compute_final_metrics(stat)

a = a.astype(np.uint64)
b = b.astype(np.uint64)
print waterz.evaluate_total_volume(a, b)
