f = open('BLR.txt','r')
fp = open('BL2.txt','r')
fpp = open('BL3.txt','r')

fs = open('BLRf.txt','w')
fss = open('BL2f.txt','w')
fsss = open('BL3f.txt','w')

count =0
for line in f:
	if count ==0:
		count=1
		fs.write(line)
		continue
	
	temp =  "\"" + line.strip() + "\""
	fs.write(temp)
	fs.write('\n')

count =0
for line in fp:
	if count ==0:
		count=1
		fss.write(line)
		continue
	
	fss.write( "\"" + line.strip() + "\"")
	fss.write('\n')

count =0
for line in fpp:
	if count ==0:
		count=1
		fsss.write(line)
		continue
	#print type(line)
	fsss.write( "\"" + line.strip() + "\"")
	fsss.write('\n')

f.close()
fp.close()
fpp.close()
fs.close()
fss.close()
fsss.close()


	
