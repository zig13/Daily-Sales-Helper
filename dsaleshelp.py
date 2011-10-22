#-------------------------------------------------------------------------------
# Name:        Daily Sales Helper Varibles Setup Script
# Purpose:
#
# Author:      Thomas Sturges-Allard
#
# Created:     18/10/2011
# Copyright:   (c) Thomas 2011
# Licence:      Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
#			http://creativecommons.org/licenses/by-nc-sa/3.0/
#-------------------------------------------------------------------------------

import os #For checking presence of varibles.ini
dot = str(os.curdir) #Find out how the current OS likes directories to be done
sep = str(os.sep)
inifile = "%s%svaribles.ini" %(dot,sep)
repeat = 0 #Defaults which may or may not be changed later. Need to be assigned so can be tested
summary = 0
if not os.access(inifile, os.R_OK) :  #Will run setup if varibles.ini cannot be found
	print "Varibles.ini not found."
	print "Basic setting are nessasary for operation"
	print "Running varibles.ini setup script."
	print " "
	import setupvarini
	exit(0)

import ConfigParser #Config parser is used to retrieve settings and other data from varibles.ini
varibles = ConfigParser.ConfigParser() #Is a very useful module and isn't too hard to learn
varibles.read( inifile ) #Opens varibles.ini as a current configfile under the name "varibles"

print "Varibles.ini found"
print "Loading settings"
print ""

from decimal import * #Need Decimal module as am doing division calcualtions and shizzle
getcontext().prec = 8 #Just a safety in-case something before has changed it

from datetime import date
from datetime import timedelta #Allows doing maths with dates and times
aday = timedelta(days=1)
today = date.today()
yesterday = today-aday
weekday = today.isoweekday()
yweekday = yesterday.isoweekday()

if varibles.has_option ('Settings', 'roundsalesfigs') :
	round = varibles.get('Settings', 'roundsalesfigs')
else :
	round = 'false'

if varibles.get('Settings', 'usevarinifigs') == 'true' : #The recommended option which means targets and cumulative totals for the week are stored in varibles.ini
	if varibles.has_option('Cumulative', 'lastuse' ) :
		lastuse = varibles.get('Cumulative', 'lastuse' )
		if lastuse == str(yesterday) :
			askcumu = 0 #DSH was run the day before so cumu from varibles.ini is up-to-date
			cumu = Decimal(varibles.get('Cumulative', 'runtotal' ))
			if round == 'true' : #Option for people who don't want to/aren't allowed to put pennies on hard-copy
				rcumu = int(varibles.get('Cumulative', 'rougthruntotal' )) #Loads cumu based on 1506/1812 totals with pennies rounded off. Can potentially end-up quite different from accurate cumu
		
		else:
			if lastuse == str(today) :
				cumu = Decimal(varibles.get('Cumulative', 'runtotal' ))
				if round == 'true' : #See above
					rcumu = int(varibles.get('Cumulative', 'rougthruntotal' ))
				askcumu = 0
				repeat = 1 #Allows skipping some calculations as cumu has not changed
			else :
				askcumu = 1 #If DSH was not run the previous day and so cumu value is out-dated. Will ask what cumu is up to day before
	else : #In the case that dsh has not been run at all
		askcumu = 1
			
	if weekday == 7 : #if Sunday
		yesterdayt = 'Saturday' #Text is used in question for clarification
		weekstart = today - timedelta(days=7)
		summary = 1 #Will print extra information for weekly report (see end)
	if weekday == 1 : #if Monday
		yesterdayt = 'Sunday'
		cumu = Decimal(0)
		weekstart = today - timedelta(days=1)
	if weekday == 2 : #if Tuesday
		yesterdayt = 'Monday'	
		weekstart = today - timedelta(days=2)
	if weekday == 3 : #if Wednesday
		yesterdayt = 'Tuesday'
		weekstart = today - timedelta(days=3)
	if weekday == 4 : #if Thursday
		yesterdayt = 'Wednesday'
		weekstart = today - timedelta(days=4)
	if weekday == 5 : #if Friday
		yesterdayt = 'Thursday'
		weekstart = today - timedelta(days=5)
	if weekday == 6 : #if Saturday
		yesterdayt = 'Friday'
		weekstart = today - timedelta(days=6)
	if repeat == 0 : #If repeat is 1, no input is required (cumu has not changed) so this line is not nesasary
		print "Hi! I'm going to help you complete your daily sales."
	if varibles.has_section('Week Nos') == 1 : #Week Nos section converts week start to week number which is what targets are indexed under
		sweekstart = str(weekstart)
		weektype = varibles.get('Settings', 'weektype') #Weektype (Debenhams or TRIPP) must be clarified to avoid confusion. Is chosen at setup
		if varibles.has_option( 'Week Nos', sweekstart ) == 1 :
			wkno = varibles.get('Week Nos', sweekstart ) #Grabs week number using weekstart calculated earlier
			starg = varibles.get('Targets', wkno ) #Then uses week number to grab target (as a string as from config)
			targ = int(starg) #Creates a interger (whole number) version of target
			slaye = varibles.get('Last Years', wkno )
			laye = int(slaye)
			forn = "First" #Since data is availible from varibles.ini, extra/optional questions are not required so 1506 total request should begin 'first' rather than 'next'
		else :
			print "Target & Last Year values not present for this week"
			print "Beginning setup/recording of target and last year values"
			print " "
			wkno = int(raw_input("First, enter the current %s week number:" %('weektype') )) #Weektype is clarified
			targ = int(raw_input("Now, enter the target takings for this week:" ))
			laye = int(raw_input("Finally, enter last years taking for this week:" ))
			swkno = str(wkno)
			starg = str(targ)
			slaye = str(laye)
			varibles.set('Info', 'firstweek', swkno)
			varibles.set('Targets', swkno, starg0)
			varibles.set('Last Years', swkno, sly0)
			with open(inifile, 'w') as varfile : #Target/LY is written to Varibles.ini so can be accessed tommorow
					varibles.write(varfile)
			print "Target and last year values succesfully stored"
			print "Daily Sales Helper can now proceed normally"
			forn = "First"
		theweek = "week %s" %(wkno)
	else:
		print "Error: No target/last year data stored." #Without the week nos section the target can not be found
		print " "
		done = 0
		while done == 0 : #An answer MUST be given ('while' creates a loop)
			print "Choose from an option below:"
			print "1) Set usevarinifigs to False and re-run DS Helper"
			print "2) Delete varibles file and run setup"
			print "3) Exit"
			ask1 = raw_input("Please enter your choice:" )
			if (ask1 == "1") or (ask1 == "1)") or (ask1 == "s") or (ask1 == "Set") : #Gives users flexibility in what they enter
				varibles.set('Settings', 'usevarinifigs', 'false') #Disables the use of figures from varibles.ini
				with open(inifile, 'w') as varfile :
					varibles.write(varfile)
				import dailysaleshelper #Restarts daily sales helper in a bit of a bodge way
			else:
				if (ask1 == "2") or (ask1 == "2)") or (ask1 == "d") or (ask1 == "Delete") :
					print "Deleting varibles.ini"
					os.remove(inifile)
					print "Varibles.ini deleted"
					print " "
					import setupvarini
					done = 1 #Allows user to exit the loop (and exit)
				else: #Else-if chains are good practise for catching all possibilities but look messier :(
					if (ask1 == "3") or (ask1 == "3)") or (ask1 == "e") or (ask1 == "Exit") :
						done = 1
		exit (0)


else:
	if varibles.get('Settings', 'usevarinifigs') == 'false' : #For people who don't trust computers...
		print "Hi! I'm going to help you complete your daily sales." #Users have to enter cumu, targets and last year every run
		theweek = "the week"
		if weekday == 1 :
			yesterdayt = 'Sunday'
			cumu = Decimal(0)
			rcumu = 0
			targ = int( raw_input( "First, what is the target for the week?" ))
		else:
			cumu = Decimal( raw_input( "First, what are the cumulative takings for the week so far?" ))
			if round == 'true' : #Only need to ask this if they want rounded figures
				rcumu = int( raw_input( "Next, what are the ROUGTH cumulative takings for the week so far?" ))
			askcumu = 0
			targ = int ( raw_input( "Next, what is the target for the week?" ))
			if weekday == 2 :
				yesterdayt = 'Monday'
			if weekday == 3 :
				yesterdayt = 'Tuesday'
			if weekday == 4 :
				yesterdayt = 'Wednesday'
			if weekday == 5 :
				yesterdayt = 'Thursday'
			if weekday == 6 :
				yesterdayt = "Friday"
			if weekday == 7 :
				yesterdayt = 'Saturday'	
				summary = 1
		
		laye = int( raw_input( "Next, what is the last year figure for the week?"))
		forn = "Next" #Users have already inputed data at this stage so the next question will start 'Next' rather than 'First'
		print " "

			
	else:
		print "Settings are corrupt/missing"
		fail = raw_input("Please delete your varibles.ini file and retry." )
		exit (0)
if askcumu == 1 :
	forn = 'Next' #Again, this optional question means that the correct prefix to the 1506 total question is next rather than first
	print ""
	print "Daily Sales Helper was not run yesterday :( "
	print "Cumulative data is therefore incorrect"
	cumu = Decimal(raw_input( "Please enter the cumulative takings for the week so far." ))
	if round == 'true' :
		rcumu = int( raw_input( "Next, what are the ROUGTH (no pennies) cumulative takings for the week so far?" ))
if repeat == 0 :
	t1506t = Decimal(raw_input("%s, what were total sales on %s for 1506 (concessions)?" %(forn, yesterdayt))) #forn is used here as it is possible users have had to input data before this
	t1812t = Decimal(raw_input("Next, what were total sales on %s for 1812 (TRIPP)?" %(yesterdayt)))
	print ""
	print "Calculating..."
	#Actual calculations start here if DSH has not been run yet today
	total = Decimal(t1506t+t1812t) #Decimal module used to calculate decimals properly. Capitalisation of the 'D' is nessasary
	cumu = Decimal(cumu+total) #Adding day total to running total
	if round == 'true' :
		rt1506t = int(t1506t.quantize(Decimal("0"))) #Rounding off of pennies before any calculations
		rt1812t = int(t1812t.quantize(Decimal("0")))
		rtotal = rt1506t+rt1812t
		rcumu = rcumu + rtotal
dtarg = Decimal(targ) #Making decimal so can be involved in calculations with real decimals
dlaye = Decimal(laye)
if round == 'false' :
	remtarg = Decimal(dtarg-cumu)
	remlaye = Decimal(dlaye-cumu)
else :
	remtarg = targ-rcumu
	remlaye = laye-rcumu
dperctarg = 100/dtarg*cumu
perctarg = int(dperctarg.quantize(Decimal("0")))
dperclaye = 100/dlaye*cumu
perclaye = int(dperclaye.quantize(Decimal("0")))

if round == 'true' : #Percentages are calculated again using rounded values as over time rounding can result in significant difference in cumu
	rperctarg = Decimal((100/dtarg*rcumu)).quantize(Decimal("0"))
	rperclaye = Decimal((100/dlaye*rcumu)).quantize(Decimal("0"))
	print "Accurate Daily Sales Information for e-mail:"
if repeat == 0 :
	print "Total for %s is *%s*" %(yesterdayt, total) #I added asterisks around figures to make them clearer. Feel free to remove them :P
print "Cumulative totals for %s are *%s*" %(theweek, cumu)
if round == 'false' : #Remaining target/last year is only calculated for hard-copy
	if targ > cumu : #Wording changes once target is reached
		print "There is *%s* left of the target to achieve" %(remtarg)
	else :
		print "The target has been exceeded by *%s*" %(abs(remtarg))
	if laye > cumu : #Wording changes once last year value is reached
		print "You are *%s* off achieiving last year's total for the week" %(remlaye)
	else :
		print "Last year's total for the week has been exceeded by %s" %(abs(remlaye))
if summary == 0 :
	print "You have achieved *%s* percent of your target for the week" %(perctarg)
	print "You have achieved *%s* percent of last year's total for the week" %(perclaye)

if round == 'true' :
	print "" #Give it a bit of space...
	print ""
	print "Rounded-off Information for Hard-copy:" #My manager doesn't like to have the pennies on our hard copy
	if repeat == 0 :
		print "Total for %s is *%s*" %(yesterdayt, rtotal)
	print "Cumulative totals for %s are *%s*" %(theweek, rcumu)
	if targ > cumu :
		print "There is *%s* left of the target to achieve" %(remtarg)
		print "You are *%s* off achieiving last year's total for the week" %(remlaye)
	else :
		print "The target has been exceeded by *%s*" %(abs(remtarg))
		print "Last year's total for the week has been exceeded by *%s*" %(abs(remlaye))
	if summary == 0 :
		print "You have achieved *%s* percent of your target for the week" %(rperctarg)
		print "You have achieved *%s* percent of last year's total for the week" %(rperclaye)
	
if summary == 1 : #The weekly report which is completed on the Sunday, requires percentages as =/- target (100%)
	print ""
	print ""
	print "Week Sumary:"
	print "Total sales for the week is "+str(cumu) #An alternative way of combining strings and varibles that I learnt after completing everything else
	vstarg = perctarg-100
	vslaye = perclaye-100
	if vstarg > 0 : #Direction (positive or negative) of cumu vs target
		targdir = "+" 
	else :
		targdir = "-"
	if vslaye > 0 : #Direction (positive or negative) of cumu vs last year value
		layedir = "+" 
	else :
		layedir = "-"
	print "Week ended %s%s vs target and %s%s vs last year" %(targdir,vstarg,layedir,vslaye)
if varibles.get('Settings', 'usevarinifigs') == 'true' :
	if repeat == 0 :
		varibles.set('Cumulative','runtotal', str(cumu))
		if round == 'true' :
			varibles.set('Cumulative','rougthruntotal', str(rcumu))
		varibles.set('Cumulative','lastuse', str(today))
		with open(inifile, 'w') as varfile :
			varibles.write(varfile)

raw_input("Press enter to quit") #So can simply be double clicked on and will not disapear when finished