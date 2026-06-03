import numpy as np

marks = np.array([45, 78, 92, 33, 67, 88, 55, 71, 49, 83])

print("===== Marks Report =====")
print(f"Mean:   {marks.mean():.2f}")
print(f"Highest: {marks.max()}")
print(f"Lowest:  {marks.min()}")
print(f"Std Dev: {marks.std():.2f}")

passed = marks[marks >= 50]
print(f"Passed: {len(passed)} out of {len(marks)}")
print(f"Passed marks: {passed}")
