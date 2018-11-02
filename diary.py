from collections import OrderedDict
import sys
import datetime
import os 

from peewee import *

db = SqliteDatabase('diary.db')

class Entry(Model):
    content = TextField()
    timestamp = DateTimeField(default = datetime.datetime.now)
    
    class Meta:
        database = db
        
def initialize():
    """Create the database and the table if they don't exist."""
    db.connect()
    db.create_tables([Entry], safe = True)
    
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def menu_loop():
    """Show the menu for the diary"""
    choice = None
    
    while choice != 'q':
        clear()
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()
        
        if choice in menu:
            clear()
            menu[choice]()
                  
                  
def add_entry():
    """Add entries within the diary."""
    print("Enter your entry. Press crtl+d when finished.")
    data = sys.stdin.read().strip()
    
    if data:
        if input('Save entry? [Yn] ').lower() != 'n':
            Entry.create(content = data)
            print("Saved successfully.")
                 

def view_entries(search_query=None):
    """View the previous entries within."""
    entries = Entry.select().order_by(Entry.timestamp.desc())
    
    if search_query:
        entries = entries.where(Entry.content.contains(search_query))
        if search_query != entries:
            print("You're search word could not be found. "
                   "Please enter a new phrase.")
            return search_entries()
        
    for entry in entries:
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        clear()
        print(timestamp)
        print('='*len(timestamp))
        print(entry.content)
        print('\n\n'+'='*len(timestamp))
        print('N) next entry')
        print('q) return to main menu')
        print('d) delete entry')
              
        next_action = input('Action: [Ndq] ').lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'd':
              delete_entry(entry)
              
def search_entries():
    """Search saved entries for a specific string"""
    view_entries(input('Search query: '))

def delete_entry(entry):
    """Delete an entry from the diary"""
    if input("Are you sure? [yN] ").lower() == 'y':
        entry.delete_instance()
        print("Entry deleted!")
    
menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', search_entries),
    ])


if __name__ == "__main__":
    initialize()
    menu_loop()
