f = open('fname.txt', 'r')
fp = open('lname.txt','r')
fpp = open('firm.txt','r')
listf = []
listaf = []
listal = []
bigdaddy =[]

for line in f:
	listaf.append("\"" + line.strip() + "\"")
f.close()

for line in fp:
	listal.append("\"" + line.strip() + "\"")
fp.close()

for line in fpp:
	listf.append("\"" + line.strip() + "\"")
fpp.close()

for i in range(0,len(listf)):
	bigdaddy.append([listf[i], listaf[i], listal[i]])

		
fp = open('testff.txt','w')

for line in bigdaddy:
	fp.write(line[0] + ',' + line[1] + ',' + line[2])
	fp.write('\n')

fp.close()
