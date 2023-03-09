# Task 3: Create a UI to show the tickets from the database

import tkinter as tk
import sqlite3

db_file = 'jira_tickets.db'
table_name = 'tickets'

def fetch_tickets():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(f'SELECT Number, Name, Description, Reporter, Status, Due_Date FROM {table_name}')
    tickets = cursor.fetchall()
    conn.close()

    ticket_listbox.delete(0, tk.END)
    for ticket in tickets:
        ticket_listbox.insert(tk.END, f'Number: {ticket[0]}\nName: {ticket[1]}\nDescription: {ticket[2]}\nReporter: {ticket[3]}\nStatus: {ticket[4]}\nDue Date: {ticket[5]}')
    
window = tk.Tk()
window.title('Jira Tickets')

ticket_listbox = tk.Listbox(window, width=80, height=20)
ticket_listbox.pack(side=tk.LEFT, padx=10, pady=10)

fetch_button = tk.Button(window, text='Fetch Tickets', command=fetch_tickets)
fetch_button.pack(side=tk.TOP, padx=10, pady=10)

window.mainloop()
