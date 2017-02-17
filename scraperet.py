#cut -d' ' -f1 --complement BrokerFileFRom\ Reuters.txt  > BrokerReutersParsed.txt
#mongoimport --db ssad --collection firm --type csv --headerline --upsert --upsertFields FirmName --file ./BL2.txt
# Command to get the job done with unneccesary whitespaces hence need to strip() 

f = open('BL2.txt', 'r')
list = []

def inlist(string):
	for i in list:
		if string.strip() == i:
			return True

	return False

for line in f:
        if(not(inlist(line.strip()))):
		list.append(line.strip())

	else: 
		continue

f.close()

fp = open('test.txt','w')

for line in list:
	fp.write(line)
	fp.write('\n')

fp.close()
			

