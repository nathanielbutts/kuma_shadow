import os

path_to_files = 'kuma_shadow/files'
path_to_toc = 'kuma_shadow/file_toc.txt'

# Create TOC and put in file_toc.txt
toc_list = []
sorted_toc = []

for file in os.listdir(path_to_files):
    toc_list.append(file)

sorted_toc = sorted(toc_list)
print(sorted_toc)

os.remove(path_to_toc)

x = 1

with open(path_to_toc,'a') as f:
    for item in sorted_toc:
        f.write(str(str(x)+';'+item+'\n'))
        x+=1
f.close