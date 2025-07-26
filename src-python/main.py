import webview 
import os
import threading
from flask_server import run_flask_server
import time
from window_manager import WindowManager

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
        
        # espera o servidor iniciar
        time.sleep(2)
    
    # cria o gerenciador de janelas
    window_manager = WindowManager(port=PORT)
    
    supervisorio = window_manager.open_supervisorio()
    admin = window_manager.open_admin()
        
    print("Janelas abertas:", window_manager.list_open_windows())
    print("Aplicação iniciada. Feche a janela de admin para encerrar.")

    window_manager.wait_for_windows()