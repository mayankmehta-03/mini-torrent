import os
import hashlib
import bencodepy  # Changed from 'bencode' to 'bencodepy'
import socket
import threading
import requests
from urllib.parse import urlencode
import random
import time
from collections import defaultdict

class Peer:
    def __init__(self, peer_id=None, port=6881):
        self.peer_id = peer_id or self.generate_peer_id()
        self.port = port
        self.shared_files = {}
        self.active_downloads = {}
        self.connections = defaultdict(dict)
        self.server_socket = None
        
    def generate_peer_id(self):
        return '-PC0001-' + ''.join([str(random.randint(0,9)) for _ in range(12)])
    
    def create_torrent(self, file_path, tracker_url, piece_size=256*1024):
        """Create a torrent file for sharing"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        file_info = {}
        file_info['name'] = os.path.basename(file_path)
        file_info['length'] = os.path.getsize(file_path)
        
        with open(file_path, 'rb') as f:
            pieces = []
            while True:
                piece = f.read(piece_size)
                if not piece:
                    break
                pieces.append(hashlib.sha1(piece).digest())
            file_info['pieces'] = b''.join(pieces)
            file_info['piece length'] = piece_size
        
        torrent = {
            'announce': tracker_url,
            'info': file_info
        }
        
        torrent_path = f"{file_info['name']}.torrent"
        with open(torrent_path, 'wb') as f:
            f.write(bencodepy.encode(torrent))  # Changed to bencodepy.encode
            
        self.shared_files[file_path] = {
            'torrent_path': torrent_path,
            'downloaded': file_info['length'],
            'uploaded': 0
        }
        
        return torrent_path
    
    def start_server(self):
        """Start listening for peer connections"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', self.port))
        self.server_socket.listen(5)
        
        while True:
            conn, addr = self.server_socket.accept()
            threading.Thread(
                target=self.handle_connection,
                args=(conn, addr),
                daemon=True
            ).start()
    
    def handle_connection(self, conn, addr):
        """Handle incoming peer connection"""
        ip, port = addr
        conn_id = f"{ip}:{port}"
        self.connections[conn_id]['conn'] = conn
        
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                    
                # Process message
                try:
                    decoded = bencodepy.decode(data)  # Changed to bencodepy.decode
                    self.process_message(decoded, conn_id)
                except Exception as e:
                    print(f"Error decoding message: {e}")
                
        except ConnectionError:
            print(f"Connection closed by {conn_id}")
        finally:
            conn.close()
            self.connections.pop(conn_id, None)
    
    def process_message(self, message, conn_id):
        """Process incoming protocol messages"""
        # Add your message handling logic here
        pass
    
    def start_download(self, torrent_path):
        """Start downloading a file from torrent"""
        if not os.path.exists(torrent_path):
            raise FileNotFoundError(f"Torrent file not found: {torrent_path}")
            
        # Parse torrent file
        with open(torrent_path, 'rb') as f:
            torrent_data = bencodepy.decode(f.read())  # Changed to bencodepy.decode
        
        info_hash = hashlib.sha1(bencodepy.encode(torrent_data['info'])).digest()  # Changed
        file_name = torrent_data['info']['name']
        file_length = torrent_data['info']['length']
        
        # Contact tracker
        peers = self.announce_to_tracker(torrent_data['announce'], info_hash)
        
        # Start download
        download_id = f"{info_hash.hex()[:8]}-{file_name}"
        self.active_downloads[download_id] = {
            'file_name': file_name,
            'length': file_length,
            'progress': 0,
            'peers': peers,
            'info_hash': info_hash
        }
        
        # Connect to peers and start downloading
        threading.Thread(
            target=self.download_from_peers,
            args=(download_id,),
            daemon=True
        ).start()
    
    def announce_to_tracker(self, tracker_url, info_hash):
        """Announce to tracker and get peer list"""
        params = {
            'peer_id': self.peer_id,
            'port': self.port,
            'uploaded': 0,
            'downloaded': 0,
            'left': 0,
            'compact': 1,
            'info_hash': info_hash
        }
        
        try:
            response = requests.get(f"{tracker_url}?{urlencode(params)}", timeout=5)
            return response.json().get('peers', [])
        except Exception as e:
            print(f"Tracker error: {e}")
            return []
    
    def download_from_peers(self, download_id):
        """Download file pieces from peers"""
        download = self.active_downloads.get(download_id)
        if not download:
            return
            
        # Implement actual download logic
        print(f"Starting download: {download['file_name']}")
        
        # Simulation of download progress
        for i in range(1, 101):
            time.sleep(0.1)
            download['progress'] = i
            if download_id not in self.active_downloads:
                break
            print(f"Download {download_id}: {i}% complete")