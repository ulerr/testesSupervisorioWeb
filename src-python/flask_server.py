import os
from flask import Flask, send_from_directory, send_file

def create_server():
    app = Flask(__name__)
    
    DIST_DIR = os.path.join(os.path.dirname(__file__), 'dist')
    
    @app.route('/')
    def serve_index():
        #serve o arquivo index.html principal
        return send_file(os.path.join(DIST_DIR, 'index.html'))
    
    @app.route('/<path:path>')
    def serve_static(path):
        # serve arquivos estáticos da pasta dist
        file_path = os.path.join(DIST_DIR, path)
        
        # se o arquivo existe, serve ele
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return send_from_directory(DIST_DIR, path)
        
        # se não existe, serve o index.html
        print("Arquivo não encontrado, servindo index.html para SPA routing")
        return send_file(os.path.join(DIST_DIR, 'index.html'))
    
    return app

def run_flask_server(host='127.0.0.1', port=8080, debug=False):
    app = create_server()
    app.run(host=host, port=port, debug=debug, use_reloader=False)
