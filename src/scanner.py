#!/bin/env python

import sys, getopt, re, os
import sqlite3

def main():
	db = "data.db"
	conn = sqlite3.connect(os.path.expanduser(db))

	print ""
	print "Main menu"
	print "========="
	print ""
	print "To add a new user press u"
	print "To add a new item press i"
	print "To checkout an item press c"
	print "To exit press q"
	print ""
	print "What would you like to do?"

	key=raw_input().lower()

	if key == "u":
		add_user(conn)
	elif key == "i":
		add_item(conn)
	elif key == "c":
		checkout(conn)
	elif key == "q":
		return
	else:
		print "Invalid key" 

	main()
	

def add_item(conn):
	sys.stdout.write("Please scan new item:")
	item_id = raw_input();
	sys.stdout.write("Please enter item name:")
	item_name = raw_input();
	sys.stdout.write("Please enter item family:")
	item_family = raw_input().lower();

	sqlcmd = "INSERT INTO items values \
			(\"%s\",\"%s\",\"%s\");"\
			% (item_id, item_name,item_family)

	try:
		c=conn.cursor()
		c.execute(sqlcmd)
		conn.commit();

		print "%s added" %  (item_name)

	except sqlite3.Error, e:
    
		if conn:
			conn.rollback()

		print "WARNING!"
		print "This item already exists in the database!"
		print "Ensure that a unique barcode is in use!"

	return
	

def add_user(conn):
	sys.stdout.write("Please scan new ID:")
	user_id = raw_input();
	sys.stdout.write("Please enter first name:")
	fname = raw_input();
	sys.stdout.write("Please enter last name:")
	lname = raw_input();
	sys.stdout.write("Please enter email:")
	contact = raw_input();
	sys.stdout.write("\n");

	sqlcmd = "INSERT INTO users values \
			(\"%s\",\"%s\",\"%s\",1,\"%s\");" \
			% (user_id, fname, lname, contact)

	try:
		c=conn.cursor()
		c.execute(sqlcmd)
		conn.commit();

		print "%s added" %  (fname)

	except sqlite3.Error, e:
    
		if conn:
			conn.rollback()

		print "WARNING!"
		print "This user already has an account"

	return

def checkout(conn):
	sys.stdout.write("Please scan ID:")
	user_id = raw_input();
	c = conn.cursor();
	sqlcmd = "SELECT * FROM users where id=\"%s\";" % (user_id)
	c.execute(sqlcmd);

	if len(c.fetchall()) == 0:
		print ("User not found")
	else:
		print ("User found")

	return

if  __name__ == '__main__':
	print "Welcome to the checkout software"
	main()

