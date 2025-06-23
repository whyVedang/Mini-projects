import socket
import argparse
import sys  # IMPORTANT: Add this import

parser = argparse.ArgumentParser()
parser.add_argument('port')
args = parser.parse_args()

# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = int(args.port)

# Initialize socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)

print('Origin Server listening on port %s ... ' % SERVER_PORT)
sys.stdout.flush()  # Force initial output

try:
    while True:
        # Wait for client connection
        client_connection, client_address = server_socket.accept()
        
        try:
            # Get the client request
            request = client_connection.recv(1024).decode()
            print(f"\n--- Request from {client_address} ---")
            sys.stdout.flush()  # FLUSH AFTER PRINT
            
            if request.strip():
                print(request.split('\n')[0])
                sys.stdout.flush()  # FLUSH AFTER PRINT
                
                headers = request.split('\n')
                if headers[0].strip():
                    request_parts = headers[0].split()
                    if len(request_parts) < 2:
                        continue
                    
                    filename = request_parts[1]
                    print(f"Requested file: {filename}")
                    sys.stdout.flush()  # FLUSH AFTER PRINT

                    if filename == '/':
                        filename = '/index.html'
                    else:
                        filename = filename.lstrip('/')

                    try:
                        with open(filename, 'r', encoding='utf-8') as fin:
                            content = fin.read()
                        
                        response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n' + content
                        print(f"✓ Serving {filename} ({len(content)} bytes)")
                        sys.stdout.flush()  # FLUSH AFTER PRINT

                    except IOError:
                        response = 'HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n<h1>404 File Not Found</h1>'
                        print(f"✗ File not found: {filename}")
                        sys.stdout.flush()  # FLUSH AFTER PRINT

                    client_connection.sendall(response.encode('utf-8'))
                    
        except Exception as e:
            print(f"Error handling request: {e}")
            sys.stdout.flush()  # FLUSH AFTER PRINT
            
        finally:
            client_connection.close()
            
except KeyboardInterrupt:
    print("\nShutting down server...")
    sys.stdout.flush()
finally:
    server_socket.close()
