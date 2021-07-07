import os, csv

path_to_files = 'kuma_shadow/files' #where sound files are stored
path_to_toc = 'kuma_shadow/file_toc.txt' #table of contents produced from toc_maker.py
path_to_history = 'kuma_shadow/history.txt' #for now, just store last played track number

toc = []
with open(path_to_toc, 'r') as f:
    linereader = csv.reader(f, delimiter=';')
    for line in linereader:
        toc.append(line)
    f.close

first_item = toc[0][0]

if os.path.exists(path_to_history):
        with open(path_to_history, 'r') as f:
            last_item = str(f.read())
            f.close
else:
    with open(path_to_history, 'w') as f:
        f.write(first_item)
        f.close

print(last_item)
