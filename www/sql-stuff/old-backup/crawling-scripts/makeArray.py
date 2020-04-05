import numpy as np

file = open ("x.txt", "r")
x = []
for item in file:
    x.append(item.rstrip("\n")) # Process the item here if you wish before appending x.append(item.split ('\s'))
a = np.array(x)
b = list(a)
print(b)