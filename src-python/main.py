import webview 
import os
import threading
from flask_server import run_flask_server
import time
import window_manager

DEV = os.getenv("DEV") == "1"
VITE_PORT = 5173
FLASK_PORT = 8080

def start_flask_thread():
    run_flask_server(
        host='127.0.0.1', 
        port=FLASK_PORT, 
        debug=DEV
    )

if __name__ == '__main__':
    if DEV:
        PORT = VITE_PORT
        print(f"Modo de desenvolvimento - Vite server na porta {VITE_PORT}")
    else:
        PORT = FLASK_PORT
        # inicia o flask em uma thread separada
        flask_thread = threading.Thread(target=start_flask_thread, daemon=True)
        flask_thread.start()
        
    