f = open('firmsId-firms.txt', 'r')
fp = open('firmsId-AnalystNames.txt','r')
listf = []
lista = []
bigdaddy = []

for line in f:
	temp = line.split(",",1)
	for i in temp:
		bigdaddy.append("\"" + i.strip() + "\"")
	listf.append(bigdaddy)
	bigdaddy = []

f.close()

for line in fp:
	temp = line.split(",",2)
	for i in temp:
		bigdaddy.append("\"" + i.strip() + "\"")
	if(len(bigdaddy)>2):
		kempker = bigdaddy[1]
		bigdaddy[1] = bigdaddy[2]
		bigdaddy[2] = kempker
	lista.append(bigdaddy)
	bigdaddy = []

fp.close()

for line in listf:
	for headache in lista:
		if (line[0] == headache[0]):
			headache[0] = line[1]

#fp = open('testf.txt','w')

#for line in listf:
#	fp.write(line[0] + ',' + line[1])
	#fp.write('\n')

#fp.close()
			
fp = open('testff.txt','w')

for line in lista:
	fp.write(line[0] + ',' + line[1] + ',' + line[2])
	fp.write('\n')

fp.close()
