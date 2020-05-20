#!/usr/bin/env python3

from collections import OrderedDict
import datetime
import os
import csv

from peewee import *

db = SqliteDatabase('inventory.db')

product_labels = OrderedDict([
    ('n', 'Product Name: '),
    ('p', 'Price: '),
    ('q', 'Quantity: '),
    ('d', 'Updated: '),
    ('id', 'ID Number: '),
])

class Product(Model):
    product_id = AutoField()
    product_name = TextField()
    product_quantity = IntegerField(default=0)
    product_price = IntegerField(default=0)
    date_updated = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

def initialize():
    """Create the database and the table."""
    db.connect()
    db.create_tables([Product], safe=True)

def add_inventory_csv():
    """Open and add inventory items from inventory.csv"""
    with open('inventory.csv', newline='') as csv_file:
        inv_reader = csv.DictReader(csv_file, delimiter=',')
        rows = list(inv_reader)
        for row in rows[1:]:
            Product.create(product_name=row['product'],
                           product_quantity=int(row['product_quantity']),
                           product_price=int(float(row['product_price'].replace('$', '')) * 100),
                           date_updated=datetime.datetime.strptime(row['date_updated'], '%m/%d/%Y')
                           )

def clear():
    os.system('cls' if os.name == 'nt' else 'clear' )

def menu_loop():
    """Show the menu"""
    entry = None
    menu = OrderedDict([
        ('a', add_item),
        ('v', view_inventory),
        ('b', create_backup),
        ('s', search_inventory),
    ])

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
    """View an item in inventory"""
    items = Product.select().order_by(Product.product_id)
    if search:
        items = items.where(Product.content.contains(search))

    for item in items:
        date = item.date_updated.strftime('%m/%d/%Y')
        clear()
        print('{}{} {}{}'.format(product_labels['n'], item.product_name, product_labels['id'], item.product_id))
        print('-' * (len(item.product_name) + len(product_labels['n']) + len(product_labels['id']) + len(item.product_id) + 1))
        print('{}${}'.format(product_labels['p'], float(item.product_price) / 100))
        print('{}{}'.format(product_labels['q'], item.product_quantity))
        print('{}{}'.format(product_labels['d'], date))

        action = input('Press enter to view next entry or [M]enu view menu  ')
        if return_to_menu(action):
            break

def search_inventory():
    """Search inventory"""
    view_inventory(input('Item contains: '))

def add_item():
    """Add an item to inventory"""
    clear()
    print('Enter and appropriate value for each field'
          'Enter [M]enu to return to the main menu'
    )
    while True:
        name = input(product_labels['n'])
        if return_to_menu(name):
            break
        try:
            price = input(product_labels['p'])
            if return_to_menu(price):
                break
            elif not isinstance(price, (int, float)):
                raise ValueError
        except ValueError:
            print('price entry must be a number')
            continue
        try:
            quantity = input(product_labels['q'])
            if return_to_menu(quantity):
                break
            elif not isinstance(quantity, (int, float)):
                raise ValueError
        except ValueError:
            print('quantity must be a number')
            continue
        Product.create(
            product_name = name,
            product_quantity = quantity,
            product_price = int(float(price) * 100)
        )
        print('Your item has been added to the inventory')

def return_to_menu(arg):
    """Checks a variable to see if it prompts a return to the menu"""
    if arg.lower() == 'm' or arg.lower() == 'menu':
        return True

def create_backup():
    """Create a backup of the inventory"""
    #write a csv file

def delete_item(item):
    """Delete an item from the inventory"""
    delete_check = input('You want to delete this item? enter [Y]es to proceed  '):
    if delete_check.lower() == 'y' or delete_check.lower() == 'yes':
        item.delete_instance()
        print('Entry deleted')

if __name__ == '__main__':
    