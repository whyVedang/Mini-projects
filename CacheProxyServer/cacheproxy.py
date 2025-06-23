import socket
import os
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import argparse
port=input('enter fetch port:')
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('port', type=int, help='Port number to listen on')
    args = parser.parse_args()

    Server_host = '0.0.0.0'
    Server_port = args.port

    # Create cache directory if it doesn't exist
    if not os.path.exists('cache'):
        os.makedirs('cache')

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((Server_host, Server_port))
    server_socket.listen(1)
    print(f"Cache Proxy Server listening on {Server_host}:{Server_port}")
    print("Origin server: http://127.0.0.1:8000")
    while True:
        client_connection, client_address = server_socket.accept()
        try:
            request = client_connection.recv(1024).decode()
            print(f"\n--- Request from {client_address} ---")
            print(request.split('\n')[0])  # Just show the first line

            headers = request.split('\n')
            if not headers[0]:
                continue
                
            top_header = headers[0].split()
            if len(top_header) < 2:
                continue
                
            method = top_header[0]
            filename = top_header[1]

            if filename == '/':
                filename = '/index.html'
            
            print(f"Requesting: {filename}")
            content = fetch_file(filename)

            if content:
                response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n' + content
                print("✓ Response: 200 OK")
            else:
                response = 'HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n<h1>404 File Not Found</h1>'
                print("✗ Response: 404 NOT FOUND")
                
            client_connection.sendall(response.encode())
        except Exception as e:
            print(f"Error handling request: {e}")
        except KeyboardInterrupt:
            print("\n[!] Server interrupted by user (Ctrl+C). Shutting down...")
            server_socket.close()
            client_connection.close()

def fetch_file(filename):
    file_from_cache = fetch_from_cache(filename)
    if file_from_cache:
        print('Cache HIT - serving from cache')
        return file_from_cache
    else:
        print('Cache MISS - fetching from origin server')
        file_from_server = fetch_from_server(filename)


        if file_from_server:
            save_in_cache(filename, file_from_server)
            return file_from_server
        else:
            return None

def fetch_from_cache(filename):
    try:
        # Convert filename to safe cache filename
        cache_filename = filename.replace('/', '_').replace('\\', '_')
        if cache_filename.startswith('_'):
            cache_filename = cache_filename[1:]
        
        cache_path = os.path.join('cache', cache_filename)
        
        if os.path.exists(cache_path):
            with open(cache_path, 'rb', encoding='utf-8') as f:
                content = f.read()
            return content
        return None
    except Exception as e:
        print(f"Error reading from cache: {e}")
        return None

def fetch_from_server(filename):
    try:
        url = f'http://127.0.0.1:{port}{filename}'
        print(f"Fetching: {url}")
        
        q = Request(url)
        q.add_header('User-Agent', 'CacheProxy/1.0')
        
        response = urlopen(q, timeout=10)
        content = response.read().decode('utf-8')
        print(f"✓ Successfully fetched {len(content)} bytes from origin")
        return content
        
    except HTTPError as e:
        print(f"✗ HTTP error {e.code} for {filename}: {e.reason}")
        return None
    except URLError as e:
        print(f"✗ Connection error for {filename}: {e.reason}")
        return None
    except Exception as e:
        print(f"✗ Unexpected error fetching {filename}: {e}")
        return None

def save_in_cache(filename, content):
    try:
        # Convert filename to safe cache filename
        cache_filename = filename.replace('/', '_').replace('\\', '_')
        if cache_filename.startswith('_'):
            cache_filename = cache_filename[1:]
            
        cache_path = os.path.join('cache', cache_filename)
        
        with open(cache_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Saved to cache: {cache_filename}')
        
    except Exception as e:
        print(f"Error saving to cache: {e}")

if __name__ == "__main__":
    main()