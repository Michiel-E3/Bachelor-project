import matplotlib.pyplot as plt
import numpy as np

index_left = [1,2,3,5,4,5,6,7]

# select last continuous sequence
diffs = np.diff(index_left)
split_index = np.where(diffs != 1)[0]
start = split_index[-1] + 1 if len(split_index) > 0 else 0
index_left = index_left[start:]

print(index_left)