from nltk.tag.stanford import NERTagger
import sys, json
st = NERTagger('english.muc.7class.distsim.crf.ser.gz','stanford-ner/stanford-ner.jar') 
ret_list = st.tag(sys.argv[1:])
#temp_list = sys.argv[1:]
#print ret_list
ret_dict = {}
i = 0
cname = '' 
fname = ''
aname = ''
j = 0
l = len(ret_list)
while ( j < l): 
	#print j
	if ret_list[j][1] == 'ORGANIZATION' and i == 0 and not cname:
		cname = ret_list[j][0]
		j = j + 1
		while j<l and ret_list[j][1] == 'ORGANIZATION':
			#print "loop1"
			cname = cname + " " + ret_list[j][0]
			j = j + 1
		i = 1
	elif ret_list[j][1] == 'ORGANIZATION' and i == 1 and not fname: 
		fname = ret_list[j][0]
		j = j + 1
		while j<l and ret_list[j][1] == 'ORGANIZATION':
			#print "loop2"
			fname = fname + "  " + ret_list[j][0]
			j = j + 1
	elif ret_list[j][1] == 'PERSON': 
		aname = aname + ' ' + ret_list[j][0]
	j = j + 1

check = 0
if(not cname and not fname and not aname):
	check = 1

if check == 1:
	st = NERTagger('english.all.3class.distsim.crf.ser.gz','stanford-ner/stanford-ner.jar') 
	ret_list = st.tag(sys.argv[1:])
	#temp_list = sys.argv[1:]
	#print ret_list
	ret_dict = {}
	i = 0
	cname = '' 
	fname = ''
	aname = ''
	j = 0
	l = len(ret_list)
	while ( j < l): 
		#print j
		if ret_list[j][1] == 'ORGANIZATION' and i == 0 and not cname:
			cname = ret_list[j][0]
			j = j + 1
			while j<l and ret_list[j][1] == 'ORGANIZATION':
				#print "loop1"
				cname = cname + " " + ret_list[j][0]
				j = j + 1
			i = 1
		elif ret_list[j][1] == 'ORGANIZATION' and i == 1 and not fname: 
			fname = ret_list[j][0]
			j = j + 1
			while j<l and ret_list[j][1] == 'ORGANIZATION':
				#print "loop2"
				fname = fname + "  " + ret_list[j][0]
				j = j + 1
		elif ret_list[j][1] == 'PERSON': 
			aname = aname + ' ' + ret_list[j][0]
		j = j + 1

	check = 0
	if(not cname and not fname and not aname):
		check = 1

if check == 1:
	st = NERTagger('english.conll.4class.distsim.crf.ser.gz','stanford-ner/stanford-ner.jar') 
	ret_list = st.tag(sys.argv[1:])
	#temp_list = sys.argv[1:]
	#print ret_list
	ret_dict = {}
	i = 0
	cname = '' 
	fname = ''
	aname = ''
	j = 0
	l = len(ret_list)
	while ( j < l): 
		#print j
		if ret_list[j][1] == 'ORGANIZATION' and i == 0 and not cname:
			cname = ret_list[j][0]
			j = j + 1
			while j<l and ret_list[j][1] == 'ORGANIZATION':
				#print "loop1"
				cname = cname + " " + ret_list[j][0]
				j = j + 1
			i = 1
		elif ret_list[j][1] == 'ORGANIZATION' and i == 1 and not fname: 
			fname = ret_list[j][0]
			j = j + 1
			while j<l and ret_list[j][1] == 'ORGANIZATION':
				#print "loop2"
				fname = fname + "  " + ret_list[j][0]
				j = j + 1
		elif ret_list[j][1] == 'PERSON': 
			aname = aname + ' ' + ret_list[j][0]
		j = j + 1

	check = 0
	if(not cname and not fname and not aname):
		check = 1

#print fname.split()[0]
temp = fname.split()
if(temp ==[]):
	pass
elif(len(temp)>0):
	fname = temp[0]
result={'cname': cname.strip(), 'fname': fname.strip(), 'aname': aname.strip(),  'check': check}
print result
print json.dumps(result)

