import json
import sqlite3
import os
from datetime import datetime

# Load Balena config
with open('/Volumes/resin-boot/config.json', 'r') as f:
    config = json.load(f)

# Connect to ghostlink db (copied to home)
db_path = os.path.expanduser('~/ghostlink.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create additional tables for deeper ingestion
cursor.execute('''
CREATE TABLE IF NOT EXISTS devices (
    id INTEGER PRIMARY KEY,
    device_id INTEGER,
    uuid TEXT,
    device_type TEXT,
    application_name TEXT,
    application_id INTEGER,
    user_id INTEGER,
    username TEXT,
    registered_at INTEGER,
    ingested_at TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY,
    path TEXT,
    hash TEXT,
    size INTEGER,
    ingested_at TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS configs (
    id INTEGER PRIMARY KEY,
    key TEXT,
    value TEXT,
    source TEXT,
    ingested_at TEXT
)
''')

# Insert device metadata
device_data = {
    'device_id': config.get('deviceId'),
    'uuid': config.get('uuid'),
    'device_type': config.get('deviceType'),
    'application_name': config.get('applicationName'),
    'application_id': config.get('applicationId'),
    'user_id': config.get('userId'),
    'username': config.get('username'),
    'registered_at': config.get('registered_at'),
    'ingested_at': datetime.now().isoformat()
}

cursor.execute('''
INSERT INTO devices (device_id, uuid, device_type, application_name, application_id, user_id, username, registered_at, ingested_at)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', tuple(device_data.values()))

print("Inserted device metadata")

# Extract and insert API keys (as before)
keys_to_ingest = [
    ('deviceApiKey', 'device'),
    ('mixpanelToken', 'analytics'),
    ('uuid', 'uuid')
]

for key_name, perm in keys_to_ingest:
    if key_name in config and config[key_name]:
        key_value = config[key_name]
        user_id = config.get('username', 'unknown')
        created_at = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT OR IGNORE INTO api_keys (key, user_id, permissions, created_at)
            VALUES (?, ?, ?, ?)
        ''', (key_value, user_id, perm, created_at))
        print(f"Inserted {key_name}")

# Ingest OS release info
with open('/Volumes/resin-boot/os-release', 'r') as f:
    os_release = {}
    for line in f:
        if '=' in line:
            key, value = line.strip().split('=', 1)
            os_release[key] = value.strip('"')

for key, value in os_release.items():
    cursor.execute('''
        INSERT INTO configs (key, value, source, ingested_at)
        VALUES (?, ?, ?, ?)
    ''', (key, value, 'os-release', datetime.now().isoformat()))

print("Inserted OS release configs")

# Ingest active config.txt settings
with open('/Volumes/resin-boot/config.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            cursor.execute('''
                INSERT INTO configs (key, value, source, ingested_at)
                VALUES (?, ?, ?, ?)
            ''', (key.strip(), value.strip(), 'config.txt', datetime.now().isoformat()))

print("Inserted config.txt settings")

# Ingest file hashes from fingerprint
with open('/Volumes/resin-boot/resinos.fingerprint', 'r') as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 2:
            hash_val, path = parts
            # Get file size if exists
            full_path = '/Volumes/resin-boot' + path
            size = os.path.getsize(full_path) if os.path.exists(full_path) else 0
            cursor.execute('''
                INSERT INTO files (path, hash, size, ingested_at)
                VALUES (?, ?, ?, ?)
            ''', (path, hash_val, size, datetime.now().isoformat()))

print("Inserted file hashes")

# Ingest device-type.json options
with open('/Volumes/resin-boot/device-type.json', 'r') as f:
    device_type = json.load(f)

for key, value in device_type.items():
    if isinstance(value, (str, int, bool)):
        cursor.execute('''
            INSERT INTO configs (key, value, source, ingested_at)
            VALUES (?, ?, ?, ?)
        ''', (key, str(value), 'device-type.json', datetime.now().isoformat()))

print("Inserted device-type configs")

conn.commit()
conn.close()

print("Deep ingestion complete.")