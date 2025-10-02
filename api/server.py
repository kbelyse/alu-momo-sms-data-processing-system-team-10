import json
import base64
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import xml.etree.ElementTree as ET
from datetime import datetime

# Load and parse XML data
def load_transactions():
    """Parse XML file and convert to list of dictionaries"""
    try:
        tree = ET.parse('../data/modified_sms_v2.xml')
        root = tree.getroot()
        
        transactions = []
        for idx, sms in enumerate(root.findall('sms'), start=1):
            transaction = {
                'id': idx,
                'protocol': sms.get('protocol'),
                'address': sms.get('address'),
                'date': sms.get('date'),
                'type': sms.get('type'),
                'subject': sms.get('subject'),
                'body': sms.get('body'),
                'toa': sms.get('toa'),
                'sc_toa': sms.get('sc_toa'),
                'service_center': sms.get('service_center'),
                'read': sms.get('read'),
                'status': sms.get('status'),
                'locked': sms.get('locked'),
                'date_sent': sms.get('date_sent'),
                'readable_date': sms.get('readable_date'),
                'contact_name': sms.get('contact_name')
            }
            transactions.append(transaction)
        
        return transactions
    except Exception as e:
        print(f"Error loading transactions: {e}")
        return []

# Initialize transactions
TRANSACTIONS = load_transactions()
NEXT_ID = len(TRANSACTIONS) + 1

# Authentication credentials (Basic Auth)
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

class APIHandler(BaseHTTPRequestHandler):
    
    def _set_headers(self, status_code=200, content_type='application/json'):
        """Set response headers"""
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def _authenticate(self):
        """Check Basic Authentication"""
        auth_header = self.headers.get('Authorization')
        
        if not auth_header:
            return False
        
        try:
            # Extract credentials from Authorization header
            auth_type, credentials = auth_header.split(' ')
            if auth_type.lower() != 'basic':
                return False
            
            # Decode base64 credentials
            decoded = base64.b64decode(credentials).decode('utf-8')
            username, password = decoded.split(':')
            
            # Validate credentials
            return username == VALID_USERNAME and password == VALID_PASSWORD
        except:
            return False
    
    def _send_unauthorized(self):
        """Send 401 Unauthorized response"""
        self._set_headers(401)
        response = {
            'error': 'Unauthorized',
            'message': 'Invalid or missing credentials'
        }
        self.wfile.write(json.dumps(response).encode())
    
    def _send_response(self, data, status_code=200):
        """Send JSON response"""
        self._set_headers(status_code)
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def _send_error(self, status_code, message):
        """Send error response"""
        self._set_headers(status_code)
        response = {
            'error': True,
            'message': message
        }
        self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        """Handle preflight requests"""
        self._set_headers(204)
    
    def do_GET(self):
        """Handle GET requests"""
        # Check authentication
        if not self._authenticate():
            self._send_unauthorized()
            return
        
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        
        # GET /transactions - List all transactions
        if path_parts[0] == 'transactions' and len(path_parts) == 1:
            self._send_response({
                'success': True,
                'count': len(TRANSACTIONS),
                'data': TRANSACTIONS
            })
        
        # GET /transactions/{id} - Get specific transaction
        elif path_parts[0] == 'transactions' and len(path_parts) == 2:
            try:
                transaction_id = int(path_parts[1])
                transaction = next((t for t in TRANSACTIONS if t['id'] == transaction_id), None)
                
                if transaction:
                    self._send_response({
                        'success': True,
                        'data': transaction
                    })
                else:
                    self._send_error(404, f'Transaction with ID {transaction_id} not found')
            except ValueError:
                self._send_error(400, 'Invalid transaction ID')
        
        else:
            self._send_error(404, 'Endpoint not found')
    
    def do_POST(self):
        """Handle POST requests"""
        global NEXT_ID
        
        # Check authentication
        if not self._authenticate():
            self._send_unauthorized()
            return
        
        parsed_path = urlparse(self.path)
        
        # POST /transactions - Create new transaction
        if parsed_path.path == '/transactions':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                new_transaction = json.loads(post_data.decode())
                
                # Assign new ID
                new_transaction['id'] = NEXT_ID
                NEXT_ID += 1
                
                # Add to transactions list
                TRANSACTIONS.append(new_transaction)
                
                self._send_response({
                    'success': True,
                    'message': 'Transaction created successfully',
                    'data': new_transaction
                }, 201)
            except json.JSONDecodeError:
                self._send_error(400, 'Invalid JSON data')
            except Exception as e:
                self._send_error(500, f'Server error: {str(e)}')
        else:
            self._send_error(404, 'Endpoint not found')
    
    def do_PUT(self):
        """Handle PUT requests"""
        # Check authentication
        if not self._authenticate():
            self._send_unauthorized()
            return
        
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        
        # PUT /transactions/{id} - Update transaction
        if path_parts[0] == 'transactions' and len(path_parts) == 2:
            try:
                transaction_id = int(path_parts[1])
                
                # Find transaction
                transaction_index = next((i for i, t in enumerate(TRANSACTIONS) if t['id'] == transaction_id), None)
                
                if transaction_index is None:
                    self._send_error(404, f'Transaction with ID {transaction_id} not found')
                    return
                
                # Read update data
                content_length = int(self.headers['Content-Length'])
                put_data = self.rfile.read(content_length)
                update_data = json.loads(put_data.decode())
                
                # Update transaction (keep the same ID)
                update_data['id'] = transaction_id
                TRANSACTIONS[transaction_index] = update_data
                
                self._send_response({
                    'success': True,
                    'message': 'Transaction updated successfully',
                    'data': update_data
                })
            except ValueError:
                self._send_error(400, 'Invalid transaction ID')
            except json.JSONDecodeError:
                self._send_error(400, 'Invalid JSON data')
            except Exception as e:
                self._send_error(500, f'Server error: {str(e)}')
        else:
            self._send_error(404, 'Endpoint not found')
    
    def do_DELETE(self):
        """Handle DELETE requests"""
        # Check authentication
        if not self._authenticate():
            self._send_unauthorized()
            return
        
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        
        # DELETE /transactions/{id} - Delete transaction
        if path_parts[0] == 'transactions' and len(path_parts) == 2:
            try:
                transaction_id = int(path_parts[1])
                
                # Find and remove transaction
                transaction = next((t for t in TRANSACTIONS if t['id'] == transaction_id), None)
                
                if transaction:
                    TRANSACTIONS.remove(transaction)
                    self._send_response({
                        'success': True,
                        'message': f'Transaction {transaction_id} deleted successfully'
                    })
                else:
                    self._send_error(404, f'Transaction with ID {transaction_id} not found')
            except ValueError:
                self._send_error(400, 'Invalid transaction ID')
        else:
            self._send_error(404, 'Endpoint not found')
    
    def log_message(self, format, *args):
        """Custom logging"""
        print(f"{self.address_string()} - [{self.log_date_time_string()}] {format % args}")

def run_server(port=8000):
    """Start the HTTP server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, APIHandler)
    print(f'Starting server on port {port}...')
    print(f'Server running at http://localhost:{port}/')
    print(f'\nAuthentication credentials:')
    print(f'Username: {VALID_USERNAME}')
    print(f'Password: {VALID_PASSWORD}')
    print(f'\nAvailable endpoints:')
    print(f'  GET    /transactions')
    print(f'  GET    /transactions/{{id}}')
    print(f'  POST   /transactions')
    print(f'  PUT    /transactions/{{id}}')
    print(f'  DELETE /transactions/{{id}}')
    print(f'\nPress Ctrl+C to stop the server')
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nShutting down server...')
        httpd.shutdown()

if __name__ == '__main__':
    run_server()