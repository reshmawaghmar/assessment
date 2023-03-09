import tkinter as tk
import sqlite3
import requests

jira_endpoint = 'https://your-jira-url.com/rest/api/2/search'
jira_username = 'your-jira-username'
jira_password = 'your-jira-password'

db_file = 'jira_tickets.db'
table_name = 'tickets'


def fetch_new_tickets():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(f'SELECT MAX(Number) FROM {table_name}')
    last_ticket_number = cursor.fetchone()[0]
    if last_ticket_number is None:
        last_ticket_number = 0
    
    
    response = requests.get(jira_endpoint, auth=(jira_username, jira_password), params={'jql': f'project=YOUR_PROJECT AND issuetype=YOUR_ISSUE_TYPE AND status!=Closed AND status!=Resolved AND status!=Cancelled AND number>{last_ticket_number}', 'maxResults': 100})
    response.raise_for_status()
    tickets_data = response.json()['issues']
    
    
    for ticket_data in tickets_data:
        ticket_number = ticket_data['key']
        ticket_name = ticket_data['fields']['summary']
        ticket_description = ticket_data['fields']['description']
        ticket_reporter = ticket_data['fields']['reporter']['displayName']
        ticket_status = ticket_data['fields']['status']['name']
        ticket_due_date = ticket_data['fields']['duedate']
        cursor.execute(f'INSERT INTO {table_name} (Number, Name, Description, Reporter, Status, Due_Date) VALUES (?, ?, ?, ?, ?, ?)', (ticket_number, ticket_name, ticket_description, ticket_reporter, ticket_status, ticket_due_date))
    conn.commit()
    conn.close()
    
    
    fetch_tickets()


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


