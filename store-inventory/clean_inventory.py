import csv

inventory = []

# noinspection SpellCheckingInspection
with open('inventory.csv', newline='') as csvfile:
    # noinspection SpellCheckingInspection
    invreader = csv.DictReader(csvfile, delimiter=',')
    rows = list(invreader)
    for row in rows[1:]:
        inventory.append(row)

