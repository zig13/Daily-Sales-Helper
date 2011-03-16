import ConfigParser
import os
import operator
varibles = ConfigParser.RawConfigParser()
varibles.read(['/Scripts/varibles.ini'])
if operator.not_(os.access('/Scripts/varibles.ini', os.R_OK)) :
	print "Varibles file missing"
	if operator.not_(os.access("/Scripts\setupvarini.py", os.F_OK)) :
		print "Varibles file setup script missing or corrupt"
		fail = int(raw_input("Press enter to exit script" ))
		sys.exit(n)		
	else :
		print "Running varibles file setup script"
		import setupvarini
		varibles.read(['/Scripts/varibles.ini'])
		if operator.not_(varibles.has_section("Cumulative")) :
			print "Varibles file setup failed"
			fail = int(raw_input("Press enter to exit script" ))
			sys.exit(n)
		else :
			print "Varibles file created succesfully"
else :
	varibles.read(['/Scripts/varibles.ini'])
	if operator.not_(varibles.has_section('Cumulative')) :
		print "Varibles file incomplete or corrupt"
		if operator.not_(os.access("/Scripts/setupvarini.py", os.F_OK)) :
			print "Varibles file setup script missing or corrupt"
			fail = int(raw_input("Press enter to exit script" ))
			sys.exit(n)		
		else :
			print "Running varibles file setup script"
			import setupvarini
			varibles.read(['/Scripts/varibles.ini'])
			if operator.not_(varibles.has_section("Cumulative")) :
				print "Varibles file setup failed"
				fail = int(raw_input("Press enter to exit script" ))
				sys.exit(n)
			else :
				print "Varibles file created succesfully"
print "Hi! I'm going to help you complete your daily sales"
