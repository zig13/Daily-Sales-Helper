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

import os
dot = str(os.curdir)
sep = str(os.sep)
inifile = "%s%svaribles.ini" %(dot,sep)
if os.access(inifile, os.R_OK) :
	print "Varibles.ini already exists"
	print "To stop/exit this script, type 'exit'"
	print "To view/edit the exisiting file, type 'view'"
	print "To delete the existing file and create a new one, type 'delete'"
	ask1 = raw_input("Please enter your choice:" )
	if (ask1 == "exit") or (ask1 == "e") :
		print "Exiting"
		exit(0)
	else :
		if (ask1 == "view") or (ask1 == "v") :
			print "Opening varibles.ini for viewing and editing"
			os.startfile(os.path.normpath(inifile))
			exit(0)
		else :
			if (ask1 == "delete") or (ask1 == "d") :
				print "Deleting varibles.ini"
				os.remove(inifile)
				print "Varibles.ini deleted"
				print " "
			else:
				douche = raw_input("You're such a douche" )
				exit(0)

print "This script will create a file called 'varibles.ini' which will be used to store:"
print "1) Your personal settings"
print "2) A running total for the week (i.e cumulative sales)"
print "3) Target and last year values (optional)"
print " "
print "First, we're going to create the Settings section"

import ConfigParser
varibles = ConfigParser.RawConfigParser()
varibles.add_section('Settings')

set1 = raw_input("Do you want to use target and last year values from the varibles.ini file? (recommended)" )
if (set1 == 'yes') or (set1 == 'true') or (set1 == '1') or (set1 == 'sure') or (set1 == 'ja') :
	varibles.set('Settings', 'usevarinifigs', 'true')
else :
	if (set1 == 'no') or (set1 == 'false') or (set1 == '0') or (set1 == 'nein'):
		varibles.set('Settings', 'usevarinifigs', 'false')
	else :
		print "Input not regognised"
		varibles.set('Settings', 'usevarinifigs', 'true')
		print "Option set to defualt (true)"
set2 = raw_input("Do you want two sets of data to be presented, one of which is generated from rounded values?" )
if (set2 == 'yes') or (set2 == 'true') or (set2 == '1') or (set2 == 'sure') or (set2 == 'Jane') or (set2 == "y") :
	varibles.set('Settings', 'roundsalesfigs', 'true')
else :
	if (set2 == 'no') or (set2 == 'false') or (set2 == '0') :
		varibles.set('Settings', 'roundsalesfigs', 'false')
	else :
		print "Input not regognised"
		varibles.set('Settings', 'roundsalesfigs', 'false')
		print "Option set to defualt (true)"
		
varibles.add_section('Cumulative')
varibles.set('Cumulative', 'runtotal', '0')
if varibles.get('Settings', 'roundsalesfigs') == 'true' :
	varibles.set('Cumulative', 'rougthruntotal', '0')
	
with open(inifile, 'w') as varfile :
	varibles.write(varfile)
	
print "Settings succesfully set"
print " "	
	
if varibles.get('Settings', 'usevarinifigs') == 'true' :
	import datetime
	print "Beginning setup/recording of target and last year values"
	varibles.add_section('Targets')
	varibles.add_section('Last Years')
	varibles.add_section('Info')
	tord = raw_input("Firstly, do you want to use TRIPP or Debenhams week numbers?" )
	if (tord == 'TRIPP') or (tord == 'tripp') or (tord == 't') :
		weektype = "TRIPP"
		varibles.set('Settings', 'weektype', 'TRIPP')
	else :
		if (tord == 'Debenhams') or (tord == 'Debs') or (tord == 'debs') or (tord == 'd'):
			weektype = "Debenhams"
		else :
			print "Input not recognised"
			weektype = "Debenhams"
			print "Option set to defualt (Debenhams)"
	varibles.set('Settings', 'weektype', weektype )
	with open(inifile, 'w') as varfile :
		varibles.write(varfile)
	wkno = int(raw_input("Now, enter the current %s week number:" %(weektype) ))
	targ0 = int(raw_input("Next, enter the target takings for this week:" ))
	ly0 = int(raw_input("Finally, enter last years taking for this week:" ))
	swkno = str(wkno)
	starg0 = str(targ0)
	sly0 = str(ly0)
	varibles.set('Info', 'firstweek', swkno)
	varibles.set('Targets', swkno, starg0)
	varibles.set('Last Years', swkno, sly0)
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
	xs = str(wkno)
	varibles.add_section('Week Starts')
	varibles.add_section('Week Nos')
	varibles.set('Week Starts', xs, d)
	varibles.set('Week Nos', ds, xs)
	targ = str(5)
	ly = str(5)
	print " "
	print "You will now be asked for target and last year values for subsequent weeks."
	print "To stop providing figures and save those previously answered, answer with any letter(s)."
	print " "
	import types 
	import operator
	while targ.isdigit() and ly.isdigit() :
		wkno += 1
		xs = str(wkno)
		d += timedelta(days=7)
		ds = str(d)
		targ = raw_input("Please enter the target value for week %s (starting %s):" %(wkno, d))
		if targ.isdigit() :
			ly = raw_input("Please enter the last year value for week %s (starting %s):" %(xs, d))
			if ly.isdigit() :
				varibles.set('Week Starts', xs, ds)
				varibles.set('Week Nos', ds, xs)
				varibles.set('Targets', xs, targ)
				varibles.set('Last Years', xs, ly)
	varibles.set('Info', 'lastweek', xs)
	ldate = d + timedelta(days=6)
	varibles.set('Info', 'lastdate', ldate)
	with open(inifile, 'w') as varfile :
		varibles.write(varfile)
	print "Targets and Last Year Values succesfully set"
	print " "
run = raw_input("Do you want to run the Daily Sales Helper now?" )
if (run == 'yes') or (run == 'true') or (run == 'y') or (run == 'sure') or (run == '1') :
	print ""
	import dailysaleshelper.py