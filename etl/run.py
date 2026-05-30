"""
server.py  -  MoMo Transactions REST API
              Plain Python http.server - no third-party web frameworks.

Endpoints
---------
GET    /transactions        list all transactions
GET    /transactions/{id}   single record
POST   /transactions        create a new record
PUT    /transactions/{id}   update a record
DELETE /transactions/{id}   delete a record



Run:  python server.py
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import base64
import sys
import os
import re
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, os.path.dirname(__file__))
from parse_xml import parse_xml

XML_PATH = os.path.join(os.path.dirname(__file__), 'modified_sms_v2.xml')

print(f"[boot] Parsing {XML_PATH} ...", flush=True)
TRANSACTIONS = parse_xml(XML_PATH)
NEXT_ID = max(tx['id'] for tx in TRANSACTIONS) + 1 if TRANSACTIONS else 1
print(f"[boot] Loaded {len(TRANSACTIONS)} transactions.", flush=True)





def _send_json(handler, status, payload):
    body = json.dumps(payload, indent=2).encode('utf-8')
    handler.send_response(status)
    handler.send_header('Content-Type', 'application/json')
    handler.send_header('Content-Length', str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _send_unauth(handler):
    handler.send_response(401)
    handler.send_header('WWW-Authenticate', 'Basic realm="MoMo API"')
    handler.send_header('Content-Type', 'application/json')
    handler.end_headers()
    handler.wfile.write(b'{"error": "Unauthorized: invalid or missing credentials"}')


def _read_body(handler):
    length = int(handler.headers.get('Content-Length', 0))
    if length == 0:
        return {}
    raw = handler.rfile.read(length)
    try:
        return json.loads(raw.decode('utf-8'))
    except json.JSONDecodeError:
        return None


class MoMoHandler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        pass

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Authorization, Content-Type')
        self.end_headers()

    def do_GET(self):

        parsed = urlparse(self.path)
        path = parsed.path.rstrip('/')
        qs = parse_qs(parsed.query)

        # GET /transactions
        if path == '/transactions':
            results = list(TRANSACTIONS)
            total = len(results)
            limit = int(qs.get('limit', [50])[0])
            offset = int(qs.get('offset', [0])[0])
            page = results[offset: offset + limit]
            _send_json(self, 200, {
                'total': total,
                'limit': limit,
                'offset': offset,
                'count': len(page),
                'data': page,
            })
            return

        # GET /transactions/{id}
        m = re.fullmatch(r'/transactions/(\d+)', path)
        if m:
            tid = int(m.group(1))
            tx = next((t for t in TRANSACTIONS if t['id'] == tid), None)
            if tx is None:
                _send_json(self, 404, {'error': f'Transaction {tid} not found'})
            else:
                _send_json(self, 200, tx)
            return

        _send_json(self, 404, {'error': 'Endpoint not found'})

    def do_POST(self):
        global NEXT_ID


        path = urlparse(self.path).path.rstrip('/')

        if path != '/transactions':
            _send_json(self, 404, {'error': 'Endpoint not found'})
            return

        data = _read_body(self)
        if data is None:
            _send_json(self, 400, {'error': 'Invalid JSON body'})
            return

        new_tx = {
            'id':           NEXT_ID,
            'address':      data.get('address', 'M-Money'),
            'date':         data.get('date'),
            'readable_date': data.get('readable_date'),
            'body':         data.get('body', ''),
            'type':         data.get('type'),
            'read':         data.get('read', '1'),
        }

        TRANSACTIONS.append(new_tx)
        NEXT_ID += 1

        _send_json(self, 201, new_tx)

    def do_PUT(self):

        path = urlparse(self.path).path.rstrip('/')
        m = re.fullmatch(r'/transactions/(\d+)', path)
        if not m:
            _send_json(self, 404, {'error': 'Endpoint not found'})
            return

        tid = int(m.group(1))
        tx = next((t for t in TRANSACTIONS if t['id'] == tid), None)
        if tx is None:
            _send_json(self, 404, {'error': f'Transaction {tid} not found'})
            return

        data = _read_body(self)
        if data is None:
            _send_json(self, 400, {'error': 'Invalid JSON body'})
            return

        for field in ['address', 'date', 'readable_date', 'body', 'type', 'read']:
            if field in data:
                tx[field] = data[field]

        _send_json(self, 200, tx)

    def do_DELETE(self):

        path = urlparse(self.path).path.rstrip('/')
        m = re.fullmatch(r'/transactions/(\d+)', path)
        if not m:
            _send_json(self, 404, {'error': 'Endpoint not found'})
            return

        tid = int(m.group(1))
        tx = next((t for t in TRANSACTIONS if t['id'] == tid), None)
        if tx is None:
            _send_json(self, 404, {'error': f'Transaction {tid} not found'})
            return

        TRANSACTIONS.remove(tx)
        _send_json(self, 200, {'message': f'Transaction {tid} deleted successfully'})


def run(port):
    server = HTTPServer(('0.0.0.0', port), MoMoHandler)
    print(f"[server] MoMo API running on http://localhost:{port}")
    print(f"[server] Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n[server] Shutting down.')


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run(3030)