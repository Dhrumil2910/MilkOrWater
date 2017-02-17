# Common Interface to access the different parsing scripts
import os
dict = {1:'Benzinga.py', 2:'Briefing.py', 3:'Gainers_Today.py', 4:'TheStreet.py', 5:'FlyOntheWall.py', 6:'dividend_v2.py', 7:'street_insider_v2' }  

def gateway():
	while(1==1):
		print "Please Select an Integer Option\n"
		print "1:Benzinga\n"
		print "2:Briefing\n"
		print "3:Gainers_Today\n"
		print "4:The_Street\n"
		print "5:Fly_On_The_Wall\n"
		print "6:Dividend_Daily\n"
		print "7:Street_Insider\n"
		print "0:Exit\n"
		user_input =  raw_input()
		try:
			user_input = int(user_input)
			if(user_input==0):
				break
			elif(user_input >= 1 and user_input <= 7):
				os.system('Python' + ' ' + dict[user_input])
			else:
				print "Please Select a Correct Option\n"
			
		except ValueError:
			print "Please Input an integer\n"
			continue

gateway()