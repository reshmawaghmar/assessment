# Task 2: Change the status of the ticket from 'Open' to 'Close' with a comment in Jira using API.

import requests
import base64

issue_key = 'JIRA-1234'
transition_endpoint = f'https://your-jira-instance.com/rest/api/2/issue/{issue_key}/transitions'


jira_username = 'your-jira-username'
jira_token = 'your-jira-api-token'
auth_header = f'Basic {base64.b64encode(f"{jira_username}:{jira_token}".encode()).decode()}'


response = requests.get(transition_endpoint, headers={
    'Authorization': auth_header,
    'Content-Type': 'application/json'
})


response.raise_for_status()


response_json = response.json()
close_transition_id = None
for transition in response_json['transitions']:
    if transition['to']['name'] == 'Closed':
        close_transition_id = transition['id']
        break

if not close_transition_id:
    raise Exception("Could not find 'Close' transition for issue")

transition_payload = {
    'transition': {
        'id': close_transition_id
    },
    'update': {
        'comment': [
            {
                'add': {
                    'body': 'Closing the ticket as the issue is resolved'
                }
            }
        ]
    }
}


response = requests.post(transition_endpoint, headers={
    'Authorization': auth_header,
    'Content-Type': 'application/json'
}, json=transition_payload)


response.raise_for_status()