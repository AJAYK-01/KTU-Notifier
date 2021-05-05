import csv
with open('testdata.csv', 'r') as file:
    reader = csv.reader(file)
    with open('testdatafinal.csv','w') as file:
        write = csv.writer(file)
        newreader=[]
        for j,row in enumerate(reader):
            if(j==0):
                continue
            try:
                if(row[3]==""):
                    row[3]=row[1]
                row[3].replace('"','')
                newreader.append(row[3:4])
            except:
                print("error",j)
        write.writerows(newreader)

        



        
