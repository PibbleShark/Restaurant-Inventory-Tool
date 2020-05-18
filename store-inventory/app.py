#!/usr/bin/env python3

from collections import OrderedDict
import datetime
import sys
import os

from peewee import *

db = SqliteDatabase('inventory.db')

menu = OrderedDict([
    ('a', add_item),
    ('v', view_inventory),
    ('b', create_backup),
    ('s', search_inventory),
])

#read CSV file
#clean it probably using regex

#function to add inventory.csv to database



class Product(Model):
    product_id = #peewee's buit in primary_key function
    product_name = #name of the product
    product_quantity = #quantity as int
    product_price = #price in cents as int
    date_updated = #datetime when product was updated

    class Meta:
        database = db

def initialize():
    """Create the database and the table."""
    db.connect()
    db.create_tables([Product], safe=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear' )

def menu_loop():
    """Show the menu"""
    entry = None

    while entry != 'q':
        clear()
        print("enter 'q' to quit.")
        for key, value in menu.items():
            print('{}: {}'.format(key, value.__doc__))
        entry = input('What would you like to do?  ').lower().strip()

        try:
            if entry not in menu:
                clear()
                raise ValueError("That is not a valid entry")
            else:
                clear()
                menu[entry]()
        except ValueError as err:
            print(err)
            continue

def view_inventory(search=None):
    """View an Item in Inventory"""

def search_inventory():
    """Search Inventory"""
    #adding a search for empty fields

def add_item():
    """Add an Item to Inventory"""
    #create an inventory item according to dict keys
    #do not require all fields

def create_backup():
    """Create a Backup of the Inventory"""
    #create a backup CSV



if __name__ == '__main__':

    #run database menu


