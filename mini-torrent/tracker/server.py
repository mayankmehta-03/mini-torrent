from flask import Flask, request, jsonify
from threading import Lock
import time
import logging
from datetime import datetime, timedelta

app = Flask(__name__)

# Thread-safe data structures
peers = {}
peer_lock = Lock()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Tracker')

# Peer expiration time (seconds)
PEER_EXPIRY = 1800  # 30 minutes

@app.route('/announce', methods=['GET'])
def announce():
    """Handle peer announcements and return peer list"""
    try:
        # Required parameters
        peer_id = request.args.get('peer_id')
        port = int(request.args.get('port'))
        info_hash = request.args.get('info_hash')
        uploaded = int(request.args.get('uploaded', 0))
        downloaded = int(request.args.get('downloaded', 0))
        left = int(request.args.get('left', 0))

        # Validate required parameters
        if not all([peer_id, port, info_hash]):
            return jsonify({'error': 'Missing required parameters'}), 400

        # Get client IP (handling proxy cases)
        if request.headers.getlist("X-Forwarded-For"):
            ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            ip = request.remote_addr

        # Update peer information
        with peer_lock:
            if info_hash not in peers:
                peers[info_hash] = {}

            peers[info_hash][peer_id] = {
                'ip': ip,
                'port': port,
                'uploaded': uploaded,
                'downloaded': downloaded,
                'left': left,
                'last_announce': time.time()
            }

            # Remove expired peers
            current_time = time.time()
            peers[info_hash] = {
                pid: data for pid, data in peers[info_hash].items()
                if current_time - data['last_announce'] < PEER_EXPIRY
            }

            # Prepare response
            peer_list = [
                {
                    'peer_id': pid,
                    'ip': data['ip'],
                    'port': data['port']
                }
                for pid, data in peers[info_hash].items()
                if pid != peer_id  # Don't include the announcing peer
            ]

        logger.info(f"Announce from {ip}:{port} for {info_hash}")

        return jsonify({
            'interval': 300,  # Recommended announce interval (seconds)
            'complete': sum(1 for p in peers[info_hash].values() if p['left'] == 0),
            'incomplete': sum(1 for p in peers[info_hash].values() if p['left'] > 0),
            'peers': peer_list
        })

    except Exception as e:
        logger.error(f"Error in announce: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/stats', methods=['GET'])
def stats():
    """Return tracker statistics"""
    with peer_lock:
        return jsonify({
            'torrents': len(peers),
            'peers': sum(len(v) for v in peers.values()),
            'uptime': str(datetime.now() - start_time)
        })

def run_tracker(host='0.0.0.0', port=5000):
    """Run the tracker server"""
    global start_time
    start_time = datetime.now()
    
    logger.info(f"Starting tracker server on {host}:{port}")
    app.run(host=host, port=port)

if __name__ == '__main__':
    run_tracker()