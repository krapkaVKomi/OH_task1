import csv

lines = []
words_of_line = []

with open("doc.csv", 'r') as file:
  csvreader = csv.reader(file)
  for row in csvreader:
    lines.append(row[0])

for line in lines:
  words = line.strip() \
    .replace('\t', '') \
    .replace('.', '') \
    .replace(',', '') \
    .replace('!', '') \
    .replace('?', '') \
    .replace(';', '') \
    .replace('\n', '') \
    .replace('  ', ' ').split(' ')
  print(line)
  print(words)



