import json
import csv
  
with open('testdata.json') as json_file:
    data = json.load(json_file)
  


data_file = open('testdata.csv', 'w')
  
# create the csv writer object
csv_writer = csv.writer(data_file)
  
# Counter variable used for writing 
# headers to the CSV file
count = 0

print(len(data))  

for column in data:
    if count == 0:
  
        # Writing headers of CSV file
        header = column.keys()
        csv_writer.writerow(header)
        count += 1
  
    # Writing data of CSV file
    print(len(column.values()))
    csv_writer.writerow(column.values())
  
data_file.close()