#!/usr/bin/env python3

from collections import OrderedDict
import datetime
import os
import csv

from peewee import *
from playhouse.shortcuts import model_to_dict
# suggested by Peter Wood https://stackoverflow.com/questions/53850558/return-single-peewee-record-as-dict

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
    product_name = CharField(unique=True)
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
        for row in rows:
            try:
                Product.create(product_name=row['product_name'],
                               product_quantity=int(row['product_quantity']),
                               product_price=int(round(float(row['product_price'].replace('$', '')) * 100)),
                               date_updated=datetime.datetime.strptime(row['date_updated'], '%m/%d/%Y')
                               )
            except IntegrityError:
                inventory_item = Product.get(product_name=row['product_name'])
                inventory_item.product_quantity = int(row['product_quantity'])
                inventory_item.product_price = int(round(float(row['product_price'].replace('$', '')) * 100))
                inventory_item.date_updated = datetime.datetime.strptime(row['date_updated'], '%m/%d/%Y')
                inventory_item.save()


def clear():
    return os.system('cls' if os.name == 'nt' else 'clear')


def menu_loop():
    """Show the menu"""
    entry = None
    menu = OrderedDict([
        ('a', add_item),
        ('v', view_inventory),
        ('b', create_backup),
        ('s', search_inventory_name),
    ])

    while entry != 'q':
        clear()
        print('\n', "Inventory Menu")
        print('-' * 16, '\n')
        for key, value in menu.items():
            print('{}: {}'.format(key, value.__doc__))
        print('q: Quit', '\n')
        entry = input('What would you like to do?  ').lower().strip()

        try:
            if entry.lower() != 'q' and entry not in menu:
                clear()
                raise ValueError("That is not a valid entry")
            else:
                clear()
                menu[entry]()
        except ValueError as err:
            print(err)
            continue


def view_inventory(name_search=None):
    """View an item in inventory"""
    items = Product.select().order_by(Product.product_id)
    if name_search:
        items = items.where(Product.product_name.contains(name_search))

    else:
        while True:
            try:
                num = input('Enter Product ID: ')
                items = Product.select().order_by(Product.product_id).where(Product.product_id == num)
                if items:
                    break
                else:
                    raise ValueError('Your entry does not correspond to any item in this database')
            except ValueError as err:
                print(err)
                view_inventory()

    for item in items:
        date = item.date_updated.strftime('%m/%d/%Y')
        clear()

        print('\n', '{}'.format(item.product_name))
        print('-' * len(item.product_name))
        print('{}{}'.format(product_labels['id'], item.product_id))
        print('{}${:,.2f}'.format(product_labels['p'], float(item.product_price / 100)))
        # https://kite.com/python/answers/how-to-format-a-float-as-currency-in-python
        print('{}{}'.format(product_labels['q'], item.product_quantity))
        print('{}{}'.format(product_labels['d'], date), '\n')

        action = input('Press enter to view another entry, [D]elete to delete entry, or [M]enu view menu  ')
        if return_to_menu(action):
            menu_loop()
        elif action.lower() == 'd' or action.lower() == 'delete':
            delete_item(item)
        else:
            view_inventory()


def search_inventory_name():
    """Search inventory by name"""
    view_inventory(name_search=input('Product name contains: '))


def add_item():
    """Add an item to inventory"""

    def print_database_keys(prod_name=None, prod_quantity=None, prod_price=None):
        if prod_name is None:
            prod_name1 = ''
        else:
            prod_name1 = prod_name
        if prod_price is None:
            prod_price1 = ''
        else:
            prod_price1 = prod_price
        if prod_quantity is None:
            prod_quantity1 = ''
        else:
            prod_quantity1 = prod_quantity

        return print(f"""
            {product_labels['n']} {prod_name1}
            {product_labels['q']} {prod_quantity1}
            {product_labels['p']} {prod_price1}
        """)

    clear()
    print('Enter an appropriate value for each field'
          'Enter [M]enu to return to the main menu'
          )
    print_database_keys()

    name = input(product_labels['n'])
    if return_to_menu(name):
        menu_loop()
    clear()
    print_database_keys(name)

    while True:
        try:
            quantity = input(product_labels['q'])
            if return_to_menu(quantity):
                menu_loop()
            quantity = int(quantity)
        except ValueError:
            print('the quantity must be a whole number')
        else:
            print_database_keys(name, quantity)
            break

    while True:
        try:
            price = input(product_labels['p'])
            if return_to_menu(price):
                menu_loop()
            price = float(price)
        except ValueError:
            print('the price must be a number')
        else:
            print_database_keys(name, quantity, price)
            break

    try:
        Product.create(
            product_name=name,
            product_quantity=int(quantity),
            product_price=int(round(float(price) * 100))
        )
        print('Your item has been added to the inventory')
    except IntegrityError:
        inventory_item = Product.get(product_name=name)
        inventory_item.product_quantity = int(quantity)
        inventory_item.product_price = int(round(float(price) * 100))
        inventory_item.save()


def return_to_menu(arg):
    """Checks a variable to see if it prompts a return to the menu"""
    if arg.lower() == 'm' or arg.lower() == 'menu':
        return True


def create_backup():
    """Create a backup of the inventory as CSV"""
    dicts = [model_to_dict(item) for item in Product.select().order_by(Product.product_id)]
    for item in dicts:
        item['product_price'] = '${:,.2f}'.format(float(item['product_price']) / 100)
        item['date_updated'] = item['date_updated'].strftime('%m/%d/%Y')

    with open('backup.csv', 'a') as csv_file:
        fieldnames = ['product_id',
                      'product_name',
                      'product_price',
                      'product_quantity',
                      'date_updated']
        inventory_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        inventory_writer.writeheader()
        inventory_writer.writerows(dicts)
        clear()
        print('Inventory backup as backup.csv has been created')


def delete_item(item):
    """Delete an item from the inventory"""
    delete_check = input('You want to delete this item? enter [Y]es to proceed  ')
    if delete_check.lower() == 'y' or delete_check.lower() == 'yes':
        item.delete_instance()
        print('Entry deleted')


if __name__ == '__main__':
    initialize()
    add_inventory_csv()
    menu_loop()
