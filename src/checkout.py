#!/bin/env python

import sys, getopt, re, os
import sqlite3
from Tkinter import *

root = Tk()

def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()


def create_mainMenu():
	menubar = Menu(root)
	filemenu = Menu(menubar, tearoff=0)
	filemenu.add_command(label="New", command=donothing)
	filemenu.add_command(label="Open", command=donothing)
	filemenu.add_command(label="Save", command=donothing)
	filemenu.add_command(label="Save as...", command=donothing)
	filemenu.add_command(label="Close", command=donothing)

	filemenu.add_separator()

	filemenu.add_command(label="Exit", command=root.quit)
	menubar.add_cascade(label="File", menu=filemenu)
	editmenu = Menu(menubar, tearoff=0)
	editmenu.add_command(label="Undo", command=donothing)

	editmenu.add_separator()

	editmenu.add_command(label="Cut", command=donothing)
	editmenu.add_command(label="Copy", command=donothing)
	editmenu.add_command(label="Paste", command=donothing)
	editmenu.add_command(label="Delete", command=donothing)
	editmenu.add_command(label="Select All", command=donothing)

	menubar.add_cascade(label="Edit", menu=editmenu)
	helpmenu = Menu(menubar, tearoff=0)
	helpmenu.add_command(label="Help Index", command=donothing)
	helpmenu.add_command(label="About...", command=donothing)
	menubar.add_cascade(label="Help", menu=helpmenu)

	root.config(menu=menubar)
	root.mainloop()
	
def main():
	db = "data.db"
	conn = sqlite3.connect(os.path.expanduser(db))
	
	create_mainMenu();
	key=raw_input().lower()

	if key == "u":
		add_user(conn)
	elif key == "i":
		add_item(conn)
	elif key == "c":
		checkout(conn)
	elif key == "r":
		checkin(conn)
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
	user_id = raw_input()
	
	if not user_lookup(conn,user_id):
		return
	
	print ("Please scan items");
	item_id = []
	raw = raw_input();
	while (raw != "END"):
		if item_lookup(conn,raw):
			item_id.append(raw)
		
		raw = raw_input()
		

	for item in item_id:
		log_out(conn,item, user_id)

	return

def checkin(conn):
	print ("Please scan items")
	raw = raw_input()
	while (raw != "END"):
		if item_lookup(conn,raw):
			log_in(conn,raw)

		raw = raw_input()

	return

#Update the transactions table to include the movement
def log_out(conn,item, user):
	c=conn.cursor()
	sqlcmd = "INSERT INTO transactions values \
			(null, date(\"now\"), time(\"now\",\
			\"localtime\"), \"%s\", \"%s\",\
			 null, null, date(\"now\",\"+3 days\"));" % (user, item)
	c.execute(sqlcmd)
	conn.commit()

#Update the transactions table to include the return of the item
def log_in(conn,item):
	c=conn.cursor()
	sqlcmd = "UPDATE transactions SET \
				return_date=date('now'), \
				return_time=time('now','localtime') \
				where item_id=\'%s\' \
				AND return_date IS NULL;" \
				% (item)
	c.execute(sqlcmd)
	conn.commit()

def item_lookup(conn, item):
	c = conn.cursor()
	sqlcmd = "SELECT * FROM items where id=\'%s\';" % (item)
	c.execute(sqlcmd)
	if len(c.fetchall()) == 0:
		print ("Item not found")
		return False
	else:
		return True

def user_lookup(conn,user):
	c = conn.cursor()
	sqlcmd = "SELECT * FROM users where id=\"%s\";" % (user)
	c.execute(sqlcmd)
	response = c.fetchall()
	if len(response) == 0:
		print ("User not found")
		return False
	elif response[0][3] == 0:
		print ("This user is barred from checking out items")
		return False
	else:
		return True

if  __name__ == '__main__':
	print "Welcome to the checkout software"
	main()

