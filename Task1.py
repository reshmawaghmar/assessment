# Fetch all tickets from Jira API with pagination and save that in the database table. You should save as many fields as you can in database but these are the minimum required.
# Number
# Name
# Description
# Reporter
# Status
# Due Date if any

import requests
import sqlite3

JIRA_API_URL = 'https://your-jira-instance.com/rest/api/2/search'

DATABASE_FILE = 'jira.db'

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            number TEXT PRIMARY KEY,
            name TEXT,
            description TEXT,
            reporter TEXT,
            status TEXT,
            due_date TEXT
        )
    ''')
    conn.commit()

def insert_ticket(conn, ticket):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tickets (
            number, name, description, reporter, status, due_date
        ) VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        ticket['key'],
        ticket['fields']['summary'],
        ticket['fields']['description'],
        ticket['fields']['reporter']['name'],
        ticket['fields']['status']['name'],
        ticket['fields']['duedate']
    ))
    conn.commit()

conn = sqlite3.connect(DATABASE_FILE)

create_table(conn)

start_at = 0
total = -1

while start_at < total or total == -1:
    response = requests.get(JIRA_API_URL, params={
        'startAt': start_at,
        'maxResults': 100,
        'fields': 'key,summary,description,reporter,status,duedate'
    })

    response.raise_for_status()

    
    response_json = response.json()
    start_at = response_json['startAt'] + len(response_json['issues'])
    total = response_json['total']

    
    for ticket in response_json['issues']:
        insert_ticket(conn, ticket)


conn.close()
