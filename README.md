# Unit-4
 Store Inventory
 
 app.py creates and operates a Sqlite3 database with the python csv module and peewee
 
 It starts the database from a csv file, cleans the data and presents it in a readable form
 The user can view the entries by searching for the product ID or by name.  The entry can be
 deleted.
 Entries can be added.  All entries are unique based on the product_name attribute of the Product Model.
 If a new entry shares a name with an existing entry name, the corresponding data is updated to the
 new values
 A CSV backup can be made.  It is written in the same format as the original CSV so that it can be
 read and cleaned by the same application.  
