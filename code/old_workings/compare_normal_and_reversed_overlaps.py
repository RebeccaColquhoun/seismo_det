import os
reversed_long = os.listdir('/Users/rebecca/Documents/PhD/Research/Frequency/seismo_det/figures/overlaps_reversed/hypocentral')
normal_long = os.listdir('/Users/rebecca/Documents/PhD/Research/Frequency/seismo_det/figures/overlaps/hypocentral')

files = {}
for fn in normal_long:
    files[fn[:-19]] = [fn[-19:-4], None]
for fn in reversed_long:
    if fn[:-19] in files:
        files[fn[:-19]][1] = fn[-19:-4]

count = 0
for key in files.keys():
    if files[key][0] != files[key][1]:
        count += 1
        print(key, files[key])

print(count)
print(len(normal_long))