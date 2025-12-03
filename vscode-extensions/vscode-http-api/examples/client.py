#!/usr/bin/env python3

import requests

URL = 'http://127.0.0.1:8765'
API_KEY = ''  # Set if configured in settings

headers = {'Content-Type': 'application/json'}
if API_KEY:
    headers['x-api-key'] = API_KEY

# Example: open a file
resp = requests.post(URL + '/open', headers=headers, json={'path': '/path/to/file.txt'})
print('open =>', resp.status_code, resp.text)

# Example: edit a file
resp = requests.post(URL + '/edit', headers=headers, json={'path': '/path/to/file.txt', 'content': 'Hello world from HTTP API\n'})
print('edit =>', resp.status_code, resp.text)

# Example: run a command
resp = requests.post(URL + '/run', headers=headers, json={'command': 'workbench.action.files.save'})
print('run =>', resp.status_code, resp.text)

# Example: commit
resp = requests.post(URL + '/commit', headers=headers, json={'message': 'Commit from HTTP API'})
print('commit =>', resp.status_code, resp.text)

# Example: read
resp = requests.get(URL + '/read', headers=headers, params={'path': '/path/to/file.txt'})
print('read =>', resp.status_code, resp.text)

# Example: list
resp = requests.get(URL + '/list', headers=headers, params={'path': '/path/to'})
print('list =>', resp.status_code, resp.text)

# Example: create
resp = requests.post(URL + '/create', headers=headers, json={'path': '/path/to/newfile.txt', 'content': 'Hello \n'})
print('create =>', resp.status_code, resp.text)

# Example: delete
resp = requests.post(URL + '/delete', headers=headers, json={'path': '/path/to/newfile.txt'})
print('delete =>', resp.status_code, resp.text)

# Example: settings update
resp = requests.post(URL + '/settings', headers=headers, json={'vscodeHttpApi.autoCommit': True})
print('settings =>', resp.status_code, resp.text)

# Example: exec (requires allowExec = true)
resp = requests.post(URL + '/exec', headers=headers, json={'command': 'echo', 'args': ['hello from exec']})
print('exec =>', resp.status_code, resp.text)

# Example: list installed extensions
resp = requests.get(URL + '/extensions', headers=headers)
print('extensions =>', resp.status_code, resp.text)

# Example: enable experimental settings for installed extensions
resp = requests.post(URL + '/extensions/experimental', headers=headers, json={'enable': True})
print('extensions experimental =>', resp.status_code, resp.text)
