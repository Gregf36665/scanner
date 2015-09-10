#!/bin/env python
"""
This file contains functions to manipulate the db
"""

import sys, getopt, re, os
import sqlite3

class Scanner:
	"""
	Scanner includes all of the functions required to manipulate the database
	"""

	def __init__(self,db):
		"""
		Create a new scanner interface
		:param db: The path of the database
		"""
		self.db = db
		self.conn = sqlite3.connect(os.path.expanduser(self.db))
		self.c=self.conn.cursor()
		
	def add_item(self,item_id, item_name,item_family):
		"""
		Add in a new item to the items table
		:param item_id: the unique ID of the item
		:param item_name: the name of the item
		:param family: the type of item

		:return Was the insert sucsessful
		"""
		sqlcmd = "INSERT INTO items values \
				(\"%s\",\"%s\",\"%s\");"\
				% (item_id, item_name,item_family)

		try:
			self.c.execute(sqlcmd)
			self.conn.commit();
			return True;

		except sqlite3.Error, e:
		
			self.conn.rollback()
			return False;

		return

	def add_user(self,user_id,fname,lname,contact):
		"""
		Add a new user into the user table
		:param user_id: the unique ID of the user
		:param fname: the user's first name
		:param lname: the user's last name
		:param contact: the email address of the user
		:return Was the insert sucsessful
		"""

		sqlcmd = "INSERT INTO users values \
				(\"%s\",\"%s\",\"%s\",1,\"%s\");" \
				% (user_id, fname, lname, contact)

		try:
			self.c.execute(sqlcmd)
			self.conn.commit()
			return True

		except sqlite3.Error, e:
		
			self.conn.rollback()
			return False

	def checkout(self,user_id,items):
		"""
		Checkout items
		This method assumes that all of the item ids are good
		Also it assumes that the user is good too (Not disabled)

		:param user_id: the unique ID of the user, it must be in the table
		:param items: a tuple of all item IDs the user wants to check out
		"""

		for item in item_id:
			self.log_out(conn,item, user_id)

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

	def item_lookup(self, item):
		"""
		See if an item exists in the items table
		
		:param item: The item ID to look up

		:return Does the item exist
		"""
		sqlcmd = "SELECT * FROM items where id=\'%s\';" % (item)
		c.execute(sqlcmd)
		if len(c.fetchall()) == 0:
			return False
		else:
			return True

	def user_lookup(conn,user):
		"""
		See if a user exists and is active

		:param user: the user ID to lookup

		:return 
		0 = Active
		1 = Doesn't exits
		2 = Inactive
		""" 
		c = conn.cursor()
		sqlcmd = "SELECT * FROM users where id=\"%s\";" % (user)
		c.execute(sqlcmd)
		response = c.fetchall()
		if len(response) == 0:
			return 1
		elif response[0][3] == 0:
			return 2
		else:
			return 0

if  __name__ == '__main__':
		s = Scanner("data.db")

