from flask import Flask, request, jsonify
import socket

app = Flask(__name__)

def register_with_as(hostname, ip, as_ip, as_port):
    msg = f"TYPE:A,NAME:{hostname},VALUE:{ip},TTL:10"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(msg.encode(), (as_ip, int(as_port)))
    resp, _ = sock.recvfrom(1024)
    sock.close()
    return resp.decode()

@app.route('/register', methods=['PUT'])
def register():
    data = request.get_json()
    required = ['hostname', 'ip', 'asip', 'asport']
    if not all(k in data for k in required):
        return "Missing field", 400
    result = register_with_as(data['hostname'], data['ip'], data['asip'], data['asport'])
    return ("Registered", 201) if result == "OK" else ("Failed", 500)

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    num = request.args.get('number', None)
    if not num or not str(num).isdigit():
        return "Invalid input", 400

    n = int(num)
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return jsonify({'number': n, 'fibonacci': a}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
