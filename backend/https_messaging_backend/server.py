import ssl
import logging
import eventlet
eventlet.monkey_patch()  # Important: patch before other imports

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from eventlet import wsgi
# The correct import for SSL in eventlet
from eventlet.green import ssl as eventlet_ssl

# Enable logging for debugging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# Configure SocketIO with eventlet
socketio = SocketIO(
    app,
    async_mode='eventlet',
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True
)

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('status', {'message': 'Connected to server'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(data):
    sender = data.get('sender', 'anonymous')
    message = data.get('message', '')
    emit('receive_message', {'sender': sender, 'message': message}, broadcast=True)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Create SSL context with modified configuration
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.verify_mode = ssl.CERT_NONE
    context.check_hostname = False
    
    try:
        # Load certificates with error handling
        context.load_cert_chain(
            certfile='cert.pem',
            keyfile='key.pem'
        )
    except Exception as e:
        print(f"Failed to load certificates: {e}")
        exit(1)

    # Configure SSL context
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
    context.set_ciphers('ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384')
    
    try:
        # Create a listening socket
        sock = eventlet.listen(('localhost', 5000))
        
        # Wrap the socket with SSL
        ssl_sock = eventlet_ssl.wrap_socket(
            sock,
            certfile='cert.pem',
            keyfile='key.pem',
            server_side=True,
            ssl_version=ssl.PROTOCOL_TLSv1_2
        )
        
        # Run the server
        wsgi.server(ssl_sock, app)
    except Exception as e:
        print(f"Server error: {e}")
        raise