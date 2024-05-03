import csv
import lang_ids

headers = ['Languages Name', 'Languages Ids']

file = "lang_codecs.csv"

try:
    with open(file, 'w') as csv_file:
        linker = csv.DictWriter(csv_file,  fieldnames=lang_ids.languages.keys())
        linker.writeheader()
        linker.writerow(lang_ids.languages)

except IOError:
    print("I/O Error encountered")
