import csv

Csv_Data = [["TICKER", "Company_Name", "Sector", "Industry"]]

def Extract_Company_Industry_Sector():
		try:
			for index in ['amex.csv', 'nyse.csv', 'nasdaq.csv']:
				with open(index, 'r') as csvfile:
					read_csv = csv.reader(csvfile, delimiter = ',')
					count =0
					for row in read_csv:
						if count == 0:
							count+=1
							continue
						Csv_Data.append([row[0],row[1],row[6],row[7]])
			
			with open('comapny_list.csv', 'w') as fp:
				csv_write = csv.writer(fp, delimiter= ',')
				csv_write.writerows(Csv_Data)
		except Exception, e:
			print str(e)

Extract_Company_Industry_Sector()