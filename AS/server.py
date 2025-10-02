import socket
import json
import os

DB_FILE = 'records.json'
PORT = 53533

# Load or initialize database
if os.path.isfile(DB_FILE):
    with open(DB_FILE) as f:
        records = json.load(f)
else:
    records = {}

def save():
    with open(DB_FILE, 'w') as f:
        json.dump(records, f)

def handle_registration(data):
    try:
        fields = dict(part.split(':') for part in data.decode().split(',') if ':' in part)
        records[fields['NAME']] = (fields['VALUE'], fields['TTL'])
        save()
        return b'OK'
    except Exception:
        return b'ERR'

def handle_query(data):
    try:
        fields = dict(part.split(':') for part in data.decode().split(',') if ':' in part)
        res = records.get(fields['NAME'], None)
        if res:
            ip, ttl = res
            return f"VALUE:{ip},TTL:{ttl}".encode()
        else:
            return b'NOTFOUND'
    except Exception:
        return b'ERR'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', PORT))
print(f'AS listening on UDP port {PORT}')

while True:
    buf, addr = sock.recvfrom(1024)
    reply = handle_registration(buf) if buf.decode().startswith("TYPE:A") else handle_query(buf)
    sock.sendto(reply, addr)
