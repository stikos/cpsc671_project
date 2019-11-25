import csv
with open('pattern_data/results_larissa_5.csv', 'r') as csv_file:
     input_data = csv.reader(csv_file)
     count = 0
     for row in input_data:
         print(tuple(list(row[0], row[1:])))
         count += 1
         if count >5: break

