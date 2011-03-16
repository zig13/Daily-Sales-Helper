#26 weeks in a year
import os
if os.access('/Scripts/varibles.ini', os.R_OK) :
	print "Varibles.ini already exists"
	print "To stop/exit this script, type 'exit'"
	print "To view/edit the exisiting file, type 'view'"
	print "To delete the existing file and create a new one, type 'delete'"
	ask1 = raw_input("Please enter your choice:" )
	if ask1 == "exit" :
		print "Exiting"
		exit(0)
	else :
		if ask1 == "view" :
			print "Opening varibles.ini for viewing and editing"
			os.startfile(os.path.normpath("/Scripts/varibles.ini"))
			exit(0)
		else :
			if ask1 == "delete" :
				print "Deleting varibles.ini"
				os.remove('/Scripts/varibles.ini')
				print "Varibles.ini deleted"
				print " "
			else:
				douche = raw_input("You're such a douche" )
				exit(0)

print "This script will create a file called 'varibles.ini' in your script folder which will be used to store:"
print "1) Your personal settings"
print "2) A running total for the week (i.e cumulative sales)"
print "3) Target and last year values (optional)"
print " "
print "First, we're going to create the Settings section"

import ConfigParser
varibles = ConfigParser.RawConfigParser()
varibles.add_section('Settings')

set1 = raw_input("Do you want to use target and last year values from the varibles.ini file?" )
if (set1 == 'yes') or (set1 == 'true') or (set1 == '1') or (set1 == 'sure') :
	varibles.set('Settings', 'usevarinifigs', 'true')
else :
	if (set1 == 'no') or (set1 == 'false') or (set1 == '0') :
		varibles.set('Settings', 'usevarinifigs', 'false')
	else :
		print "Input not regognised"
		varibles.set('Settings', 'usevarinifigs', 'true')
		print "Option set to defualt (true)"
set2 = raw_input("Do you want two sets of data to be presented, one of which is generated from rounded values?" )
if (set1 == 'yes') or (set1 == 'true') or (set1 == '1') or (set1 == 'sure') or (set1 == 'Jane'):
	varibles.set('Settings', 'roundsalesfigs', 'true')
else :
	if (set1 == 'no') or (set1 == 'false') or (set1 == '0') :
		varibles.set('Settings', 'roundsalesfigs', 'false')
	else :
		print "Input not regognised"
		varibles.set('Settings', 'roundsalesfigs', 'false')
		print "Option set to defualt (true)"
		
varibles.add_section('Cumulative')
varibles.set('Cumulative', 'runtotal', '0')
if varibles.get('Settings', 'roundsalesfigs') == 'true' :
	varibles.set('Cumulative', 'rougthruntotal', '0')
	
with open('/Scripts/varibles.ini', 'w') as varfile :
	varibles.write(varfile)
	
print "Settings succesfully set"	
	
if varibles.get('Settings', 'usevarinifigs') == 'true' :
	import datetime
	print "Beginning setup/recording of target and last year values"
	varibles.add_section('Targets')
	varibles.add_section('Last Years')
	varibles.add_section('Info')
	wkno = int(raw_input("First, enter the current TRIPP week number:" ))
	targ0 = int(raw_input("Now, enter the target takings for this week:" ))
	ly0 = int(raw_input("Next, enter last years taking for this week:" ))
	varibles.set('Info', 'firstweek', wkno)
	varibles.set('Targets', str(wkno), targ0)
	varibles.set('Last Years', str(wkno), ly0)
	x = wkno
	from datetime import date
	from datetime import timedelta
	today = date.today()
	yesterday = today - timedelta(days=1)
	weekday = yesterday.isoweekday()
	if weekday == 7 : #if Sunday
		weekstart = yesterday
	if weekday == 1 : #if Monday
		weekstart = yesterday - timedelta(days=1)
	if weekday == 2 : #if Tuesday	
		weekstart = yesterday - timedelta(days=2)
	if weekday == 3 : #if Wednesday
		weekstart = yesterday - timedelta(days=3)
	if weekday == 4 : #if Thursday
		weekstart = yesterday - timedelta(days=4)
	if weekday == 5 : #if Friday
		weekstart = yesterday - timedelta(days=5)
	if weekday == 6 : #if Saturday
		weekstart = yesterday - timedelta(days=6)

	d = weekstart	
	ds = str(d)
	xs = str(x)
	varibles.add_section('Week Starts')
	varibles.set('Week Starts', xs, d)
	targ = str(5)
	ly = str(5)
	import types 
	import operator
	while targ.isdigit() and ly.isdigit() :
		x += 1
		xs = str(x)
		d += timedelta(days=7)
		ds = str(d)
		targ = raw_input("Please enter the target value for week %s (starting %s):" %(x, d))
		if targ.isdigit() :
			ly = raw_input("Please enter the last year value for week %s (starting %s):" %(x, d))
			if ly.isdigit() :
				varibles.set('Week Starts', xs, ds)
				varibles.set('Targets', xs, targ)
				varibles.set('Last Years', xs, ly)
	varibles.set('Info', 'lastweek', xs)
	ldate = d + timedelta(days=6)
	varibles.set('Info', 'lastdate', ldate)
	with open('/Scripts/varibles.ini', 'w') as varfile :
					varibles.write(varfile)