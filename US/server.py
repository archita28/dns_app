from flask import Flask, request, jsonify
import socket
import requests

app = Flask(__name__)

def resolve_hostname(hostname, as_ip, as_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    query_string = f"NAME:{hostname}"
    sock.sendto(query_string.encode(), (as_ip, int(as_port)))
    resp, _ = sock.recvfrom(1024)
    sock.close()
    parts = dict(part.split(':') for part in resp.decode().split(',') if ':' in part)
    return parts.get('VALUE')

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    args = request.args
    fields = ['hostname', 'fsport', 'number', 'asip', 'asport']
    if not all(field in args for field in fields):
        return "Missing parameter", 400

    host_ip = resolve_hostname(args['hostname'], args['asip'], args['asport'])
    if not host_ip:
        return "Could not resolve hostname", 404

    fib_url = f"http://{host_ip}:{args['fsport']}/fibonacci?number={args['number']}"
    resp = requests.get(fib_url)
    return (resp.text, resp.status_code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
